from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="ProBalance")

# Получаем абсолютный путь к папке, где лежит main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Подключаем статику (папка static находится рядом с main.py)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Подключаем шаблоны (папка templates — это текущая папка)
templates = Jinja2Templates(directory=BASE_DIR)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})