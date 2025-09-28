from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    Float,
    Integer,
    DateTime,
    JSON,
    UniqueConstraint,
    create_engine,
    null,
    text,
    func,
)
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

db_url=os.getenv("DATABASE_URL")
db_username = os.getenv("DATABASE_USERNAME")
db_password = os.getenv("DATABASE_PASSWORD")

Base = declarative_base()


class Match(Base):
    __tablename__ = "match"

    war_id = Column(String(255), primary_key=True, comment="指定战场id（本场游戏id）")
    week = Column(Integer, nullable=False, default=0, comment="比赛周")
    day = Column(Integer, nullable=False, default=0, comment="周比赛日")
    rnd = Column(Integer, nullable=False, default=0, comment="本赛季第几个RD")
    match = Column(Integer, nullable=False, default=0, comment="RD的第几场")
    game_num = Column(Integer, nullable=False, default=0, comment="整个赛季第几场比赛")
    stage = Column(Integer, nullable=False, default=0, comment="赛段")
    description = Column(String(255), nullable=True, comment="比赛描述")
    winner = Column(String(255), default="", comment="吃鸡队伍名(team_name)")
    mvp = Column(String(255), default="", comment="本场MVP选手名")
    custom_room_name = Column(String(255), default="", comment="自定义房间名字")
    circle_level = Column(Integer, nullable=False, default=0, comment="圈数")
    circle_pos_x = Column(Float, nullable=False, default=0, comment="毒圈中心x坐标")
    circle_pos_y = Column(Float, nullable=False, default=0, comment="毒圈中心y坐标")
    circle_radius = Column(Float, nullable=False, default=0, comment="毒圈半径")
    airline_start_pos_x = Column(
        Float, nullable=False, default=0, comment="航线初始坐标x"
    )
    airline_start_pos_y = Column(
        Float, nullable=False, default=0, comment="航线初始坐标y"
    )
    airline_end_pos_x = Column(
        Float, nullable=False, default=0, comment="航线终止坐标x"
    )
    airline_end_pos_y = Column(
        Float, nullable=False, default=0, comment="航线终止坐标y"
    )
    status = Column(Integer, nullable=False, default=1, comment="1:进行中, 2:已结束")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerRealtimeStats(Base):
    """
    liveState 正常0；小肠肠1（倒地）；死亡2
    state 正常0；虚弱1；小肠肠2 死亡3
    """

    __tablename__ = "player_realtime_stats"
    __table_args__ = (
        UniqueConstraint("war_id", "uid", name="uix_player_realtime_stats_war_uid"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    war_id = Column(String(255), nullable=False, comment="指定战场id")
    uid = Column(String(255), nullable=False, comment="玩家pid")
    player_name = Column(String(255), nullable=False, default="", comment="选手名")
    team_id = Column(String(255), nullable=False, default="", comment="队伍id")
    team_code = Column(Integer, nullable=False, default=0, comment="队伍code")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    nickname = Column(String(255), default="", comment="玩家昵称")
    is_firing = Column(Integer, nullable=False, default=False, comment="是否正在开火")
    state = Column(
        Integer,
        nullable=False,
        default=0,
        comment="玩家当前状态（正常、倒地、可复活、不可复活）",
    )
    is_coin_picked = Column(
        Integer, nullable=False, default=False, comment="复活币是否被拾取"
    )
    pos_x = Column(
        Float, nullable=False, default=0, comment="选手位置x 坐标（单位厘米）"
    )
    pos_y = Column(
        Float, nullable=False, default=0, comment="选手位置y 坐标（单位厘米）"
    )
    pos_z = Column(
        Float, nullable=False, default=0, comment="选手位置z 坐标（单位厘米）"
    )
    health = Column(Float, nullable=False, default=0, comment="血量")
    live_state = Column(
        Integer, nullable=False, default=0, comment="存活状态（存活、倒地、死亡）"
    )
    air_drop = Column(Integer, nullable=False, default=0, comment="拾取空投数量")
    max_kill_distance = Column(
        Integer, nullable=False, default=0, comment="最远击杀距离（单位米）"
    )
    damage = Column(Float, nullable=False, default=0, comment="造成伤害")
    in_damage = Column(Float, nullable=False, default=0, comment="受到伤害")
    head_shot = Column(Integer, nullable=False, default=0, comment="爆头击杀数")
    heal = Column(Float, nullable=False, default=0, comment="治疗量")
    vehicle_kill = Column(Integer, nullable=False, default=0, comment="载具击杀数")
    skill_card = Column(
        Integer, nullable=False, default=0, comment="当前使用的身份卡ID"
    )
    skill_card_1 = Column(Integer, nullable=False, default=0, comment="冥王")
    skill_card_2 = Column(Integer, nullable=False, default=0, comment="海王")
    skill_card_3 = Column(Integer, nullable=False, default=0, comment="神王")
    skill_card_4 = Column(Integer, nullable=False, default=0, comment="军师")
    skill_card_5 = Column(Integer, nullable=False, default=0, comment="武圣")
    skill_card_6 = Column(Integer, nullable=False, default=0, comment="枭雄")
    skill_card_7 = Column(Integer, nullable=False, default=0, comment="影武者")
    skill_card_8 = Column(Integer, nullable=False, default=0, comment="甜心")
    skill_card_9 = Column(Integer, nullable=False, default=0, comment="球球")
    skill_card_10 = Column(Integer, nullable=False, default=0, comment="飞翼")
    skill_card_11 = Column(Integer, nullable=False, default=0, comment="迪迦")
    skill_card_12 = Column(Integer, nullable=False, default=0, comment="泽塔")
    skill_card_13 = Column(Integer, nullable=False, default=0, comment="彩虹王子")
    skill_card_14 = Column(Integer, nullable=False, default=0, comment="咸鱼")
    skill_card_15 = Column(Integer, nullable=False, default=0, comment="狼王")
    skill_card_16 = Column(Integer, nullable=False, default=0, comment="雪女")
    skill_card_17 = Column(Integer, nullable=False, default=0, comment="猫猫")
    skill_card_18 = Column(Integer, nullable=False, default=0, comment="唐老板")
    skill_card_19 = Column(Integer, nullable=False, default=0, comment="幽灵船长")
    skill_card_20 = Column(Integer, nullable=False, default=0, comment="爆炸小丑")
    skill_card_21 = Column(Integer, nullable=False, default=0, comment="太阳神")
    skill_card_22 = Column(Integer, nullable=False, default=0, comment="魔法师")
    survive = Column(Float, nullable=False, default=0, comment="生存时长（秒）")
    drive_distance = Column(Float, nullable=False, default=0, comment="驾驶距离")
    march_distance = Column(Float, nullable=False, default=0, comment="步行距离")
    assists = Column(Integer, nullable=False, default=0, comment="助攻数")
    is_out_circle = Column(Integer, nullable=False, default=False, comment="是否在圈外")
    rescue = Column(Integer, nullable=False, default=0, comment="救援次数")
    cur_weapon = Column(String(255), default="", comment="当前武器")
    hook = Column(Integer, nullable=False, default=0, comment="钩爪使用次数")
    big = Column(Integer, nullable=False, default=0, comment="大招次数")
    fire_damage = Column(Float, nullable=False, default=0, comment="火焰伤害")
    fire = Column(Integer, nullable=False, default=0, comment="火焰使用次数")
    cannon = Column(Integer, nullable=False, default=0, comment="大炮使用次数")
    worm_hole = Column(Integer, nullable=False, default=0, comment="虫洞次数")
    heal_bomb_heal = Column(Float, nullable=False, default=0, comment="治疗炸弹治疗量")
    heal_bomb = Column(Integer, nullable=False, default=0, comment="治疗炸弹次数")
    shelter = Column(Integer, nullable=False, default=0, comment="护盾次数")
    cloud_bomb = Column(Integer, nullable=False, default=0, comment="烟雾弹次数")
    bomb_damage = Column(Float, nullable=False, default=0, comment="炸弹伤害")
    bomb = Column(Integer, nullable=False, default=0, comment="炸弹次数")
    bomb_kill = Column(Integer, nullable=False, default=0, comment="炸弹击杀数")
    fire_kill = Column(Integer, nullable=False, default=0, comment="火焰击杀数")
    bomb_max_damage = Column(
        Float, nullable=False, default=0, comment="单颗炸弹最大伤害"
    )
    bomb_max = Column(Integer, nullable=False, default=0, comment="单局最多使用炸弹数")
    bomb_max_kill = Column(
        Integer, nullable=False, default=0, comment="单局炸弹最多击杀数"
    )
    pick_sword_num = Column(Integer, nullable=False, default=0, comment="拾取宝剑次数")
    sword_kill = Column(Integer, nullable=False, default=0, comment="宝剑击杀数")
    mecha_damage = Column(Float, nullable=False, default=0, comment="机甲伤害")
    mecha_kill = Column(Integer, nullable=False, default=0, comment="机甲击杀数")
    mecha_distance = Column(Float, nullable=False, default=0, comment="机甲移动距离")
    dragon_damage = Column(Float, nullable=False, default=0, comment="龙形态伤害")
    dragon_distance = Column(Float, nullable=False, default=0, comment="龙形态移动距离")
    dragon_kill = Column(Integer, nullable=False, default=0, comment="龙形态击杀数")
    sword_damage = Column(Float, nullable=False, default=0, comment="宝剑伤害")
    helmet_level = Column(Integer, nullable=False, default=0, comment="头盔等级")
    vest_level = Column(Integer, nullable=False, default=0, comment="防弹衣等级")
    bag_level = Column(Integer, nullable=False, default=0, comment="背包等级")
    xcc_distance = Column(Float, nullable=False, default=0, comment="滑板车距离")
    xcc = Column(Integer, nullable=False, default=0, comment="滑板车使用次数")
    hit_weak = Column(Integer, nullable=False, default=0, comment="击倒数")
    total_kill = Column(Integer, nullable=False, default=0, comment="总击杀数")
    move_distance = Column(Integer, nullable=False, default=0, comment="移动距离")
    bullet_total_num = Column(
        Integer, nullable=False, default=0, comment="总射击子弹数"
    )
    hit_bullet_num = Column(Integer, nullable=False, default=0, comment="命中子弹数")
    hit_head_bullet_num = Column(
        Integer, nullable=False, default=0, comment="爆头子弹数"
    )
    trexking_distance = Column(
        Integer, nullable=False, default=0, comment="霸王龙骑行距离"
    )
    peterosaur_distance = Column(
        Integer, nullable=False, default=0, comment="翼龙骑行距离"
    )
    triceratop_distance = Column(
        Integer, nullable=False, default=0, comment="三角龙骑行距离"
    )
    raptors_distance = Column(
        Integer, nullable=False, default=0, comment="迅猛龙骑行距离"
    )
    trexking_damage = Column(
        Integer, nullable=False, default=0, comment="霸王龙造成伤害"
    )
    trexking_kill = Column(Integer, nullable=False, default=0, comment="霸王龙击杀")
    use_resurrection_num = Column(
        Integer, nullable=False, default=0, comment="使用复活币次数"
    )
    lost_role_rank = Column(Integer, nullable=False, default=0, comment="排名")
    max_hit_down_distance = Column(
        Float, nullable=False, default=0, comment="最大击倒距离"
    )
    all_gun_damage = Column(JSON, comment="各武器伤害详情")
    be_used_dragon_num = Column(
        Integer, nullable=False, default=0, comment="被使用龙形态次数"
    )
    be_used_trexking_num = Column(
        Integer, nullable=False, default=0, comment="被使用霸王龙次数"
    )
    crit_rate = Column(Float, nullable=False, default=0, comment="暴击率")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamRealtimeStats(Base):
    __tablename__ = "team_realtime_stats"
    __table_args__ = (
        UniqueConstraint(
            "war_id", "team_name", name="uix_team_realtime_stats_war_team"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    war_id = Column(String(255), nullable=False, comment="指定战场id")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    team_id = Column(String(255), nullable=False, default="", comment="队伍id")
    team_code = Column(Integer, nullable=False, default=0, comment="队伍code")
    is_alive = Column(
        Integer, nullable=False, default=0, comment="队伍是否存活，1存活，0被淘汰"
    )
    rank = Column(Integer, nullable=False, default=0, comment="队伍排名")
    team_kill = Column(Integer, nullable=False, default=0, comment="队伍总击杀")
    team_hit_weak = Column(Integer, nullable=False, default=0, comment="队伍总击倒")
    team_damage = Column(Float, nullable=False, default=0, comment="队伍总伤害")
    cannon = Column(Integer, nullable=False, default=0, comment="传送大炮使用次数")
    team_move_distance = Column(
        Integer, nullable=False, default=0, comment="队伍移动距离"
    )
    team_assists = Column(Integer, nullable=False, default=0, comment="队伍助攻")
    skill_card_1 = Column(Integer, nullable=False, default=0, comment="技能卡1")
    skill_card_2 = Column(Integer, nullable=False, default=0, comment="技能卡2")
    skill_card_3 = Column(Integer, nullable=False, default=0, comment="技能卡3")
    skill_card_4 = Column(Integer, nullable=False, default=0, comment="技能卡4")
    skill_card_5 = Column(Integer, nullable=False, default=0, comment="技能卡5")
    skill_card_6 = Column(Integer, nullable=False, default=0, comment="技能卡6")
    skill_card_7 = Column(Integer, nullable=False, default=0, comment="技能卡7")
    skill_card_8 = Column(Integer, nullable=False, default=0, comment="技能卡8")
    skill_card_9 = Column(Integer, nullable=False, default=0, comment="技能卡9")
    skill_card_10 = Column(Integer, nullable=False, default=0, comment="技能卡10")
    skill_card_11 = Column(Integer, nullable=False, default=0, comment="技能卡11")
    skill_card_12 = Column(Integer, nullable=False, default=0, comment="技能卡12")
    skill_card_13 = Column(Integer, nullable=False, default=0, comment="技能卡13")
    skill_card_14 = Column(Integer, nullable=False, default=0, comment="技能卡14")
    skill_card_15 = Column(Integer, nullable=False, default=0, comment="技能卡15")
    skill_card_16 = Column(Integer, nullable=False, default=0, comment="技能卡16")
    skill_card_17 = Column(Integer, nullable=False, default=0, comment="技能卡17")
    skill_card_18 = Column(Integer, nullable=False, default=0, comment="技能卡18")
    skill_card_19 = Column(Integer, nullable=False, default=0, comment="技能卡19")
    skill_card_20 = Column(Integer, nullable=False, default=0, comment="技能卡20")
    skill_card_21 = Column(Integer, nullable=False, default=0, comment="技能卡21")
    skill_card_22 = Column(Integer, nullable=False, default=0, comment="技能卡22")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerResultStats(Base):
    __tablename__ = "player_result_stats"
    __table_args__ = (
        UniqueConstraint("war_id", "uid", name="uix_player_result_stats_war_uid"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    war_id = Column(String(255), nullable=False, comment="指定战场id")
    uid = Column(BigInteger, nullable=False, comment="玩家pid")
    player_name = Column(String(255), nullable=False, default="", comment="选手名")
    team_id = Column(String(255), nullable=False, default="", comment="队伍id")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    nickname = Column(String(255), default="", comment="玩家昵称")
    is_firing = Column(Integer, nullable=False, default=False, comment="是否正在开火")
    state = Column(
        Integer,
        nullable=False,
        default=0,
        comment="玩家当前状态（正常、倒地、可复活、不可复活）",
    )
    is_coin_picked = Column(
        Integer, nullable=False, default=False, comment="复活币是否被拾取"
    )
    pos_x = Column(
        Float, nullable=False, default=0, comment="选手位置x 坐标（单位厘米）"
    )
    pos_y = Column(
        Float, nullable=False, default=0, comment="选手位置y 坐标（单位厘米）"
    )
    pos_z = Column(
        Float, nullable=False, default=0, comment="选手位置z 坐标（单位厘米）"
    )
    health = Column(Float, nullable=False, default=0, comment="血量")
    live_state = Column(
        Integer, nullable=False, default=0, comment="存活状态（存活、倒地、死亡）"
    )
    air_drop = Column(Integer, nullable=False, default=0, comment="拾取空投数量")
    max_kill_distance = Column(
        Integer, nullable=False, default=0, comment="最远击杀距离（单位米）"
    )
    damage = Column(Float, nullable=False, default=0, comment="造成伤害")
    in_damage = Column(Float, nullable=False, default=0, comment="受到伤害")
    head_shot = Column(Integer, nullable=False, default=0, comment="爆头击杀数")
    heal = Column(Float, nullable=False, default=0, comment="治疗量")
    vehicle_kill = Column(Integer, nullable=False, default=0, comment="载具击杀数")
    skill_card = Column(
        Integer, nullable=False, default=0, comment="当前使用的身份卡ID"
    )
    skill_card_1 = Column(Integer, nullable=False, default=0, comment="冥王")
    skill_card_2 = Column(Integer, nullable=False, default=0, comment="海王")
    skill_card_3 = Column(Integer, nullable=False, default=0, comment="神王")
    skill_card_4 = Column(Integer, nullable=False, default=0, comment="军师")
    skill_card_5 = Column(Integer, nullable=False, default=0, comment="武圣")
    skill_card_6 = Column(Integer, nullable=False, default=0, comment="枭雄")
    skill_card_7 = Column(Integer, nullable=False, default=0, comment="影武者")
    skill_card_8 = Column(Integer, nullable=False, default=0, comment="甜心")
    skill_card_9 = Column(Integer, nullable=False, default=0, comment="球球")
    skill_card_10 = Column(Integer, nullable=False, default=0, comment="飞翼")
    skill_card_11 = Column(Integer, nullable=False, default=0, comment="迪迦")
    skill_card_12 = Column(Integer, nullable=False, default=0, comment="泽塔")
    skill_card_13 = Column(Integer, nullable=False, default=0, comment="彩虹王子")
    skill_card_14 = Column(Integer, nullable=False, default=0, comment="咸鱼")
    skill_card_15 = Column(Integer, nullable=False, default=0, comment="狼王")
    skill_card_16 = Column(Integer, nullable=False, default=0, comment="雪女")
    skill_card_17 = Column(Integer, nullable=False, default=0, comment="猫猫")
    skill_card_18 = Column(Integer, nullable=False, default=0, comment="唐老板")
    skill_card_19 = Column(Integer, nullable=False, default=0, comment="幽灵船长")
    skill_card_20 = Column(Integer, nullable=False, default=0, comment="爆炸小丑")
    skill_card_21 = Column(Integer, nullable=False, default=0, comment="太阳神")
    skill_card_22 = Column(Integer, nullable=False, default=0, comment="魔法师")
    survive = Column(Float, nullable=False, default=0, comment="生存时长（秒）")
    drive_distance = Column(Float, nullable=False, default=0, comment="驾驶距离")
    march_distance = Column(Float, nullable=False, default=0, comment="步行距离")
    assists = Column(Integer, nullable=False, default=0, comment="助攻数")
    is_out_circle = Column(Integer, nullable=False, default=False, comment="是否在圈外")
    rescue = Column(Integer, nullable=False, default=0, comment="救援次数")
    cur_weapon = Column(String(255), default="", comment="当前武器")
    hook = Column(Integer, nullable=False, default=0, comment="钩爪使用次数")
    big = Column(Integer, nullable=False, default=0, comment="大招次数")
    fire_damage = Column(Float, nullable=False, default=0, comment="火焰伤害")
    fire = Column(Integer, nullable=False, default=0, comment="火焰使用次数")
    cannon = Column(Integer, nullable=False, default=0, comment="大炮使用次数")
    worm_hole = Column(Integer, nullable=False, default=0, comment="虫洞次数")
    heal_bomb_heal = Column(Float, nullable=False, default=0, comment="治疗炸弹治疗量")
    heal_bomb = Column(Integer, nullable=False, default=0, comment="治疗炸弹次数")
    shelter = Column(Integer, nullable=False, default=0, comment="护盾次数")
    cloud_bomb = Column(Integer, nullable=False, default=0, comment="烟雾弹次数")
    bomb_damage = Column(Float, nullable=False, default=0, comment="炸弹伤害")
    bomb = Column(Integer, nullable=False, default=0, comment="炸弹次数")
    bomb_kill = Column(Integer, nullable=False, default=0, comment="炸弹击杀数")
    fire_kill = Column(Integer, nullable=False, default=0, comment="火焰击杀数")
    bomb_max_damage = Column(
        Float, nullable=False, default=0, comment="单颗炸弹最大伤害"
    )
    bomb_max = Column(Integer, nullable=False, default=0, comment="单局最多使用炸弹数")
    bomb_max_kill = Column(
        Integer, nullable=False, default=0, comment="单局炸弹最多击杀数"
    )
    pick_sword_num = Column(Integer, nullable=False, default=0, comment="拾取宝剑次数")
    sword_kill = Column(Integer, nullable=False, default=0, comment="宝剑击杀数")
    mecha_damage = Column(Float, nullable=False, default=0, comment="机甲伤害")
    mecha_kill = Column(Integer, nullable=False, default=0, comment="机甲击杀数")
    mecha_distance = Column(Float, nullable=False, default=0, comment="机甲移动距离")
    dragon_damage = Column(Float, nullable=False, default=0, comment="龙形态伤害")
    dragon_distance = Column(Float, nullable=False, default=0, comment="龙形态移动距离")
    dragon_kill = Column(Integer, nullable=False, default=0, comment="龙形态击杀数")
    sword_damage = Column(Float, nullable=False, default=0, comment="宝剑伤害")
    helmet_level = Column(Integer, nullable=False, default=0, comment="头盔等级")
    vest_level = Column(Integer, nullable=False, default=0, comment="防弹衣等级")
    bag_level = Column(Integer, nullable=False, default=0, comment="背包等级")
    xcc_distance = Column(Float, nullable=False, default=0, comment="滑板车距离")
    xcc = Column(Integer, nullable=False, default=0, comment="滑板车使用次数")
    hit_weak = Column(Integer, nullable=False, default=0, comment="击倒数")
    total_kill = Column(Integer, nullable=False, default=0, comment="总击杀数")
    move_distance = Column(Integer, nullable=False, default=0, comment="移动距离")
    bullet_total_num = Column(
        Integer, nullable=False, default=0, comment="总射击子弹数"
    )
    hit_bullet_num = Column(Integer, nullable=False, default=0, comment="命中子弹数")
    hit_head_bullet_num = Column(
        Integer, nullable=False, default=0, comment="爆头子弹数"
    )
    trexking_distance = Column(
        Integer, nullable=False, default=0, comment="霸王龙骑行距离"
    )
    peterosaur_distance = Column(
        Integer, nullable=False, default=0, comment="翼龙骑行距离"
    )
    triceratop_distance = Column(
        Integer, nullable=False, default=0, comment="三角龙骑行距离"
    )
    raptors_distance = Column(
        Integer, nullable=False, default=0, comment="迅猛龙骑行距离"
    )
    trexking_damage = Column(
        Integer, nullable=False, default=0, comment="霸王龙造成伤害"
    )
    trexking_kill = Column(Integer, nullable=False, default=0, comment="霸王龙击杀")
    use_resurrection_num = Column(
        Integer, nullable=False, default=0, comment="使用复活币次数"
    )
    lost_role_rank = Column(Integer, nullable=False, default=0, comment="排名")
    max_hit_down_distance = Column(
        Float, nullable=False, default=0, comment="最大击倒距离"
    )
    all_gun_damage = Column(JSON, comment="各武器伤害详情")
    be_used_dragon_num = Column(
        Integer, nullable=False, default=0, comment="被使用龙形态次数"
    )
    be_used_trexking_num = Column(
        Integer, nullable=False, default=0, comment="被使用霸王龙次数"
    )
    crit_rate = Column(Float, nullable=False, default=0, comment="暴击率")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamResultStats(Base):
    __tablename__ = "team_result_stats"
    __table_args__ = (
        UniqueConstraint("war_id", "team_name", name="uix_team_result_stats_war_team"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    war_id = Column(String(255), nullable=False, comment="指定战场id")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    team_id = Column(String(255), nullable=False, default="", comment="队伍id")
    team_code = Column(Integer, nullable=False, default=0, comment="队伍code")
    is_alive = Column(
        Integer, nullable=False, default=0, comment="队伍是否存活，1存活，0被淘汰"
    )
    rank = Column(Integer, nullable=False, default=0, comment="队伍排名")
    team_kill = Column(Integer, nullable=False, default=0, comment="队伍总击杀")
    team_hit_weak = Column(Integer, nullable=False, default=0, comment="队伍总击倒")
    team_damage = Column(Float, nullable=False, default=0, comment="队伍总伤害")
    cannon = Column(Integer, nullable=False, default=0, comment="传送大炮使用次数")
    team_move_distance = Column(
        Integer, nullable=False, default=0, comment="队伍移动距离"
    )
    team_assists = Column(Integer, nullable=False, default=0, comment="队伍助攻")
    skill_card_1 = Column(Integer, nullable=False, default=0, comment="技能卡1")
    skill_card_2 = Column(Integer, nullable=False, default=0, comment="技能卡2")
    skill_card_3 = Column(Integer, nullable=False, default=0, comment="技能卡3")
    skill_card_4 = Column(Integer, nullable=False, default=0, comment="技能卡4")
    skill_card_5 = Column(Integer, nullable=False, default=0, comment="技能卡5")
    skill_card_6 = Column(Integer, nullable=False, default=0, comment="技能卡6")
    skill_card_7 = Column(Integer, nullable=False, default=0, comment="技能卡7")
    skill_card_8 = Column(Integer, nullable=False, default=0, comment="技能卡8")
    skill_card_9 = Column(Integer, nullable=False, default=0, comment="技能卡9")
    skill_card_10 = Column(Integer, nullable=False, default=0, comment="技能卡10")
    skill_card_11 = Column(Integer, nullable=False, default=0, comment="技能卡11")
    skill_card_12 = Column(Integer, nullable=False, default=0, comment="技能卡12")
    skill_card_13 = Column(Integer, nullable=False, default=0, comment="技能卡13")
    skill_card_14 = Column(Integer, nullable=False, default=0, comment="技能卡14")
    skill_card_15 = Column(Integer, nullable=False, default=0, comment="技能卡15")
    skill_card_16 = Column(Integer, nullable=False, default=0, comment="技能卡16")
    skill_card_17 = Column(Integer, nullable=False, default=0, comment="技能卡17")
    skill_card_18 = Column(Integer, nullable=False, default=0, comment="技能卡18")
    skill_card_19 = Column(Integer, nullable=False, default=0, comment="技能卡19")
    skill_card_20 = Column(Integer, nullable=False, default=0, comment="技能卡20")
    skill_card_21 = Column(Integer, nullable=False, default=0, comment="技能卡21")
    skill_card_22 = Column(Integer, nullable=False, default=0, comment="技能卡22")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class MatchRanking(Base):
    __tablename__ = "match_ranking"
    __table_args__ = (
        UniqueConstraint("war_id", "team_name", name="uix_match_ranking_war_team"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    war_id = Column(String(255), nullable=False, comment="指定战场id")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    stage = Column(Integer, nullable=False, default=0, comment="赛段")
    rank = Column(Integer, nullable=False, default=0, comment="排名")
    ingame_rank = Column(Integer, nullable=False, default=0, comment="游戏内排名")
    kill_pts = Column(Integer, nullable=False, default=0, comment="击杀分")
    place_pts = Column(Integer, nullable=False, default=0, comment="排名分")
    total_pts = Column(Integer, nullable=False, default=0, comment="总分")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class StageRanking(Base):
    __tablename__ = "stage_ranking"
    __table_args__ = (
        UniqueConstraint("stage", "team_name", name="uix_stage_ranking_stage_team"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    stage = Column(Integer, nullable=False, default=0, comment="赛段")
    rank = Column(Integer, nullable=False, default=0, comment="排名")
    total_kill_pts = Column(Integer, nullable=False, default=0, comment="总击杀分")
    total_place_pts = Column(Integer, nullable=False, default=0, comment="总排名分")
    stage_total_pts = Column(Integer, nullable=False, default=0, comment="赛段总分")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class Team(Base):
    __tablename__ = "team"

    team_code = Column(Integer, primary_key=True, comment="队伍代码")
    team_id = Column(String(255), nullable=False, default="", comment="队伍ID")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名称")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class Player(Base):
    __tablename__ = "player"

    uid = Column(String(255), primary_key=True, comment="玩家uid")
    uid_36 = Column(String(255), nullable=False, default="0", comment="玩家36进制UID")
    player_name = Column(String(255), nullable=False, default="", comment="选手名")
    team_id = Column(String(255), nullable=False, default=0, comment="队伍id")
    team_code = Column(Integer, nullable=False, default=0, comment="队伍code")
    team_name = Column(String(255), nullable=False, default="", comment="队伍名")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamHeadtoHead(Base):
    __tablename__ = "team_headtohead"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    team_name_1 = Column(String(255), nullable=False, comment="队伍名1")
    team_name_2 = Column(String(255), nullable=False, comment="队伍名2")
    is_select = Column(Integer, nullable=False, default=0, comment="是否选择")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerHeadtoHead(Base):
    __tablename__ = "player_headtohead"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    player_name_1 = Column(String(255), nullable=False, comment="选手名1")
    player_name_2 = Column(String(255), nullable=False, comment="选手名2")
    is_select = Column(Integer, nullable=False, default=0, comment="是否选择")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerDailyStats(Base):
    __tablename__ = "player_daily_stats"
    __table_args__ = (
        UniqueConstraint("day", "player_name", name="uix_day_player_name"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    day = Column(Integer, nullable=False, comment="比赛日")
    uid = Column(String(255), nullable=False, comment="选手pid")
    player_name = Column(String(255), nullable=False, comment="选手名")
    team_name = Column(String(255), nullable=False, comment="队伍名")
    daily_kill = Column(Integer, nullable=False, comment="单日击杀", default=0)
    daily_assist = Column(Integer, nullable=False, comment="单日助攻", default=0)
    daily_dmg = Column(Integer, nullable=False, comment="单日伤害", default=0)
    daily_hit_weak = Column(Integer, nullable=False, comment="单日击倒", default=0)
    daily_crit_rate = Column(Float, nullable=False, comment="单日暴击率", default=0)
    game_played = Column(Integer, nullable=False, comment="选手单日比赛场次", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerOverallStats(Base):
    __tablename__ = "player_overall_stats"
    __table_args__ = (UniqueConstraint("player_name", name="uix_player_name"),)
    uid = Column(String(255), primary_key=True, comment="选手pid")
    player_name = Column(String(255), nullable=False, comment="选手名")
    team_name = Column(String(255), nullable=False, comment="队伍名")
    overall_kill = Column(Float, nullable=False, comment="赛季场均击杀", default=0)
    overall_assist = Column(Float, nullable=False, comment="赛季场均助攻", default=0)
    overall_dmg = Column(Float, nullable=False, comment="赛季场均伤害", default=0)
    overall_hit_weak = Column(Float, nullable=False, comment="赛季场均击倒", default=0)
    overall_crit_rate = Column(
        Float, nullable=False, comment="赛季场均暴击率", default=0
    )
    game_played = Column(Integer, nullable=False, comment="赛季比赛场次", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamDailyStats(Base):
    __tablename__ = "team_daily_stats"
    __table_args__ = (UniqueConstraint("day", "team_name", name="uix_day_team_name"),)
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    day = Column(Integer, nullable=False, comment="比赛日")
    team_code = Column(Integer, nullable=False, comment="队伍code", default=0)
    team_name = Column(String(255), nullable=False, comment="队伍名")
    team_daily_kill = Column(Integer, nullable=False, comment="队伍单日击杀", default=0)
    team_daily_assist = Column(
        Integer, nullable=False, comment="队伍单日助攻", default=0
    )
    team_daily_dmg = Column(Integer, nullable=False, comment="队伍单日伤害", default=0)
    team_daily_hit_weak = Column(
        Integer, nullable=False, comment="队伍单日击倒", default=0
    )
    team_daily_pts = Column(Integer, nullable=False, comment="队伍单日积分", default=0)
    game_played = Column(Integer, nullable=False, comment="队伍单日比赛场次", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamOverallStats(Base):
    __tablename__ = "team_overall_stats"
    __table_args__ = (UniqueConstraint("team_name", name="uix_team_name"),)
    team_code = Column(Integer, primary_key=True, comment="队伍code")
    team_name = Column(String(255), nullable=False, comment="队伍名")
    team_overall_kill = Column(
        Float, nullable=False, comment="队伍赛季场均击杀", default=0
    )
    team_overall_assist = Column(
        Float, nullable=False, comment="队伍赛季场均助攻", default=0
    )
    team_overall_dmg = Column(
        Float, nullable=False, comment="队伍赛季场均伤害", default=0
    )
    team_overall_hit_weak = Column(
        Float, nullable=False, comment="队伍赛季场均击倒", default=0
    )
    team_overall_pts = Column(
        Float, nullable=False, comment="队伍赛季场均积分", default=0
    )
    game_played = Column(Integer, nullable=False, comment="赛季比赛场次", default=0)
    top5_rate = Column(Float, nullable=False, comment="队伍赛季Top5率", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class HighlightTeam(Base):
    __tablename__ = "highlight_team"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    team_name = Column(String(255), nullable=False, comment="队伍名")
    match_day_1 = Column(Integer, nullable=False, comment="比赛日1", default=0)
    match_day_2 = Column(Integer, nullable=False, comment="比赛日2", default=0)
    is_select = Column(Integer, nullable=False, comment="是否选中", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class HighlightPlayer(Base):
    __tablename__ = "highlight_player"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    player_name = Column(String(255), nullable=False, comment="选手名")
    match_day_1 = Column(Integer, nullable=False, comment="比赛日1", default=0)
    match_day_2 = Column(Integer, nullable=False, comment="比赛日2", default=0)
    is_select = Column(Integer, nullable=False, comment="是否选中", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class PlayerStatsTips(Base):
    __tablename__ = "player_stats_tips"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    player_name = Column(String(255), nullable=False, comment="选手名")
    is_select = Column(Integer, nullable=False, comment="是否选中", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class TeamSkillCard(Base):
    __tablename__ = "team_skill_card"
    war_id = Column(String(255), nullable=False, comment="比赛ID", primary_key=True)
    team_1 = Column(String(255), nullable=False, comment="队伍1的team_name")
    team_2 = Column(String(255), nullable=False, comment="队伍2的team_name")
    team_3 = Column(String(255), nullable=False, comment="队伍3的team_name")
    team_4 = Column(String(255), nullable=False, comment="队伍4的team_name")
    is_select = Column(Integer, nullable=False, comment="是否选中", default=0)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


class OCR(Base):
    __tablename__ = "ocr"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="唯一主键")
    player_name = Column(String(255), nullable=False, comment="选手名")
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录生成的时间",
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.now(),
        server_onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
        comment="记录更新的时间",
    )


# -----------------------------
# Create all tables in database
# -----------------------------

engine = create_engine(
    f"mysql+pymysql://{db_username}:{db_password}@{db_url}",
    echo=False,
    future=True,
    # pool_pre_ping=True,
    # pool_size=30,  # 最大连接数为 30
    # max_overflow=50,  # 允许的最大溢出连接数
    # pool_timeout=30,  # 连接池获取连接的超时时间
    # pool_recycle=3600,  # 连接池中的连接每小时重置一次（防止超时）
)
# Base.metadata.create_all(engine)
