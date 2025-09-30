from typing import Annotated, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import base64
import glob
from pydantic import BaseModel, Field
from langgraph.graph import MessagesState, StateGraph, add_messages, START, END
import requests
from sqlalchemy import func
from models import MatchRanking, engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

to_ranking_score = {
    1: 16,
    2: 12,
    3: 10,
    4: 8,
    5: 6,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
}

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Prompts
IMAGE_PARSING_PROMPT = """
以下图片为游戏结果图。你需要从中提取每个战队的结算信息。图片位置对应的信息解释：
1. 前三名队伍的排名信息会以"1ST","2ND","3RD"的形式展示在最左侧。
2. 每个队伍结算框左上角的数字为队伍编号,**不是**排名,请注意！！
3. 除了前三名外，每个队伍的排名均显示在该队伍结算框的左上角的上方，是一个数字
4. 队伍结算框的左侧一列为选手名，右侧一列为每个选手对应的淘汰数
注意事项：
1. 确保你生成的数据覆盖了全部图片里的队伍
2. **不要**捏造数据！！
3. 如何区分除前三名外的排名和队伍编号？（即“队伍结算框左上角”和“队伍结算框的左上角的上方，是一个数字”）
3.1 队伍编号，即队伍结算框左上角，是一个带背景颜色的类方形区域，里面是一个数字
3.2 排名，即队伍结算框的左上角的上方，是一个数字，它出现在3.1所述“队伍结算框”的正上方，是一个不带背景的灰色数字
4. 在提取信息时，你需要严格按照第3点所述的规则，提取队伍的排名信息
5. 你需要在结束后，基于注意事项，重新核查信息是否正确和符合规范
"""


class TieBreakStats(TypedDict):
    wwcd_count: int
    stage_total_kill: int
    stage_max_single_match_pts: int
    stage_max_single_match_kill: int
    last_match_total_pts: int
    last_match_total_kill: int
    last_match_place_pts: int


# Pydantic models for structured output
class PlayerResult(BaseModel):
    player_name: str = Field(description="The name of the player")
    elims: int = Field(description="The number of eliminations the player has")


class TeamResult(BaseModel):
    team_name: str = Field(description="The name of the team")
    ranking: int = Field(description="The ranking of the team in the game")
    total_elims: int = Field(
        description="The total number of eliminations the team has, equals the sum of the eliminations of all players"
    )
    players: list[PlayerResult] = Field(
        description="The list of player results in the team"
    )
    final_ranking: int = Field(
        description="The final ranking of the team, ALWAYS keep it unset", default=0
    )
    tiebreak_stats: TieBreakStats = Field(
        description="The tiebreak stats of the team, ALWAYS keep it unset",
        default_factory=TieBreakStats,
    )


class GameResult(BaseModel):
    teams: list[TeamResult] = Field(description="The list of team results in the game")


class DataError(BaseModel):
    error_type: int = Field(
        description="The type of error. 1: final ranking error, 2: ingame ranking error, 3: total elims error"
    )
    team: str = Field(description="name of the team that error occurs to")
    original_data: str | int = Field(description="The original data from api")
    correct_data: str | int = Field(description="The correct data from game client")


class ErrorList(BaseModel):
    errors: list[DataError] = Field(description="The list of errors")


# Graph State model
class State(MessagesState):
    game_id: str
    stage: int
    error_list: ErrorList


llm = ChatOpenAI(model="openai/gpt-4.1-mini")
llm_generating_game_result = llm.with_structured_output(GameResult)


# tool functions
def get_tiebreak_stats(session: Session, team_name: str, stage: int) -> dict:
    """
    获取比较同分情况所需的队伍数据，规则如下：
    在所有回合结束后，若出现平分，将根据以下顺序决定排名。

    1) 比较同分队伍的总获胜数
    2) 比较同分队伍的当前阶段的总淘汰数
    3) 比较同分队伍的当前阶段的单局最高积分
    4) 比较同分队伍的当前阶段的单局最高淘汰
    5) 比较同分队伍最后一场比赛的总积分
    6) 比较同分队伍最后一场比赛的总淘汰数
    7) 比较同分队伍最后一场比赛的生存排名

    """
    # session = SessionLocal()
    try:
        if not team_name or stage is None:
            raise ValueError("team_name 和 stage 不能为空")
        # 获取队伍的胜场数(吃鸡)
        wwcd_count = (
            session.query(MatchRanking)
            .filter(
                MatchRanking.team_name == team_name,
                MatchRanking.stage == stage,
                MatchRanking.ingame_rank == 1,
            )
            .count()
        )
        # 获取队伍的当前阶段的总淘汰数
        # stage_total_kill = (
        #     session.query(StageRanking.total_kill_pts)
        #     .filter(StageRanking.team_name == team_name, StageRanking.stage == stage)
        #     .scalar()
        # )
        stage_total_kill = (
            session.query(
                func.coalesce(func.sum(MatchRanking.kill_pts).label("stage_kill"), 0)
            )
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .scalar()
        )
        # 获取队伍的当前阶段的单局最高积分
        stage_max_single_match_pts = (
            session.query(MatchRanking.total_pts)
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .order_by(MatchRanking.total_pts.desc())
            .limit(1)
            .scalar()
        )
        # 获取队伍的当前阶段的单局最高淘汰
        stage_max_single_match_kill = (
            session.query(MatchRanking.kill_pts)
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .order_by(MatchRanking.kill_pts.desc())
            .limit(1)
            .scalar()
        )
        # 获取队伍的最后一场比赛的总积分
        last_match_total_pts = (
            session.query(MatchRanking.total_pts)
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .order_by(MatchRanking.created_at.desc())
            .limit(1)
            .scalar()
        )
        # 获取队伍的最后一场比赛的总淘汰数
        last_match_total_kill = (
            session.query(MatchRanking.kill_pts)
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .order_by(MatchRanking.created_at.desc())
            .limit(1)
            .scalar()
        )
        # 获取队伍的最后一场比赛的生存排名
        last_match_place_pts = (
            session.query(MatchRanking.place_pts)
            .filter(MatchRanking.team_name == team_name, MatchRanking.stage == stage)
            .order_by(MatchRanking.created_at.desc())
            .limit(1)
            .scalar()
        )
        return {
            "wwcd_count": wwcd_count or 0,
            "stage_total_kill": stage_total_kill or 0,
            "stage_max_single_match_pts": stage_max_single_match_pts or 0,
            "stage_max_single_match_kill": stage_max_single_match_kill or 0,
            "last_match_total_pts": last_match_total_pts or 0,
            "last_match_total_kill": last_match_total_kill or 0,
            "last_match_place_pts": last_match_place_pts or 0,
        }
    except Exception as e:
        print(f"获取同分队伍数据失败: {e}")
        return {}


# Methods for the nodes of the graph
def parse_game_result_image(state: State):
    # 在 ./images 文件夹中查找匹配 {game_id}_rank_{number} 模式的图片
    pattern_base = f"./images/{state['game_id']}_rank_*"
    exts = [".jpg", ".jpeg", ".png"]
    image_files = []
    for ext in exts:
        image_files.extend(glob.glob(pattern_base + ext))

    if not image_files:
        raise FileNotFoundError(
            f"未找到匹配模式 {pattern_base}(.jpg/.jpeg/.png) 的图片文件"
        )

    # 按文件名排序，确保一致的处理顺序
    image_files.sort()

    # 准备 content 列表，先添加文本提示
    content = [
        {
            "type": "text",
            "text": IMAGE_PARSING_PROMPT,
        }
    ]

    # 为每张图片添加 image 内容
    for image_file in image_files:
        with open(image_file, "rb") as f:
            image_content = f.read()
            image_data = base64.b64encode(image_content).decode("utf-8")
            content.append(
                {
                    "type": "image",
                    "source_type": "base64",
                    "data": image_data,
                    "mime_type": "image/jpeg",
                }
            )

    response = llm_generating_game_result.invoke(
        [
            {
                "role": "user",
                "content": content,
            }
        ]
    )
    return {
        "messages": [
            HumanMessage(content=IMAGE_PARSING_PROMPT),
            AIMessage(content=response.model_dump_json()),
        ],
    }


def compare(state: State):
    # 判断最后一条message是不是AI，如果不是，直接报错
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError("The last message is not an AIMessage")

    # 把AIMessage的json字符串内容解析为pydantic对象
    game_result = GameResult.model_validate_json(last_message.content)

    # 获取API数据
    api_result = requests.get("http://139.196.72.70:8111/match_ranking").json()["data"]

    # 比较
    for index, team_result in enumerate(game_result.teams):
        session = SessionLocal()
        team_result.final_ranking = index + 1
        team_result.tiebreak_stats = get_tiebreak_stats(
            session, team_result.team_name, state["stage"]
        )
        session.close()

    game_result.teams.sort(
        key=lambda x: (
            to_ranking_score.get(x.ranking, 0) + x.total_elims,
            x.tiebreak_stats["wwcd_count"],
            x.total_elims,
            # x.tiebreak_stats["stage_total_kill"],
            x.tiebreak_stats["stage_max_single_match_pts"],
            x.tiebreak_stats["stage_max_single_match_kill"],
            x.tiebreak_stats["last_match_total_pts"],
            x.tiebreak_stats["last_match_total_kill"],
            x.tiebreak_stats["last_match_place_pts"],
        ),
        reverse=True,
    )

    # print(game_result)

    error_list = ErrorList(errors=[])
    for index, team_result in enumerate(game_result.teams):
        team_name = api_result[index]["team_name"]
        if team_result.team_name != api_result[index]["team_name"]:
            error_list.errors.append(
                DataError(
                    error_type=1,
                    team=team_name,
                    original_data=api_result[index]["rank"],
                    correct_data=next(
                        team_result.final_ranking
                        for team_result in game_result.teams
                        if team_result.team_name == team_name
                    ),
                )
            )
            api_team_data = next(
                team for team in api_result if team["team_name"] == team_result.team_name
            )
            if team_result.ranking != api_team_data["ingame_rank"]:
                error_list.errors.append(
                    DataError(
                        error_type=2,
                        team=team_name,
                        original_data=api_team_data["ingame_rank"],
                        correct_data=team_result.ranking,
                    )
                )
            if team_result.total_elims != api_team_data["kill_pts"]:
                error_list.errors.append(
                    DataError(
                        error_type=3,
                        team=team_name,
                        original_data=api_team_data["kill_pts"],
                        correct_data=team_result.total_elims,
                    )
                )
        else:
            if team_result.ranking != api_result[index]["ingame_rank"]:
                error_list.errors.append(
                    DataError(
                        error_type=2,
                        team=team_name,
                        original_data=api_result[index]["ingame_rank"],
                        correct_data=team_result.ranking,
                    )
                )
            if team_result.total_elims != api_result[index]["kill_pts"]:
                error_list.errors.append(
                    DataError(
                        error_type=3,
                        team=team_name,
                        original_data=api_result[index]["kill_pts"],
                        correct_data=team_result.total_elims,
                    )
                )
    print("error_list:", error_list)
    return {"error_list": error_list}


graph_builder = StateGraph(State)
graph_builder.add_node("parser", parse_game_result_image)
graph_builder.add_node("compare", compare)
graph_builder.add_edge(START, "parser")
graph_builder.add_edge("parser", "compare")
graph_builder.add_edge("compare", END)

graph = graph_builder.compile()

# result = graph.invoke({"game_id": "1", "stage": 6})
# print(result["error_list"])

def check(game_id: str, stage: int):
    result = graph.invoke({"game_id": game_id, "stage": stage})
    return result["error_list"]


