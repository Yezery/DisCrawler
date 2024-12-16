import os
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from service.config.elasticsearch_config import init_es
from service.config.logging_config import setup_logging
from service.controller.csdnController import csdn
from service.controller.bossController import boss
from service.controller.systemController import system
from dotenv import load_dotenv
# 设置日志
# setup_logging()
load_dotenv()
init_es()
port = os.getenv("PORT")
app = FastAPI()
# 开启跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(
    csdn,
    prefix="/csdn",
    tags=[
        "CSDN 接口",
    ],
)
app.include_router(
    boss,
    prefix="/boss",
    tags=[
        "BOSS 接口",
    ],
)
app.include_router(
    system,
    prefix="/system",
    tags=[
        "系统 接口",
    ],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port))

# {
#     "spider_name":"boss_website_scrapy",
#     "spider_args":{
#         "job":"java",
#         "city":"广州"
#     }
# }