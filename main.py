import shutil
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from graph import check
from loguru import logger
import uvicorn
import sys

app = FastAPI()

# disabled, all logs should be managed by systemd
logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "level": "DEBUG",  # 根据需要设置日志级别
            "backtrace": True,
            "diagnose": True,
        }
    ]
)


# Serve static files and homepage
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.svg")


@app.post("/upload")
async def upload(
    files: list[UploadFile], game_id: str = Form(...), stage: int = Form(...)
):
    try:
        for file in files:
            file_location = f"./images/{file.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"error handling file upload: {e}")
        raise HTTPException(
            status_code=500,
            detail="error handling file upload",
        )

    try:
        error_list = check(game_id, stage)
    except Exception as e:
        logger.error(f"error checking game result: {e}")
        raise HTTPException(
            status_code=500,
            detail="error checking game result",
        )

    return {"error_list": error_list}


# only enabled when developing
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=False)
