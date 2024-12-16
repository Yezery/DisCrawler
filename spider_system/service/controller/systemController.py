import os
import uuid
import psutil
from scrapy.utils.project import get_project_settings
from fastapi import APIRouter, HTTPException
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from service.dao.dto.system.StartSpiderRequest import StartSpiderRequest
from service.dao.dto.system.StopSpiderRequest import StopSpiderRequest
import signal
import time

system = APIRouter()
running_spiders = {}  # 用于保存正在运行的爬虫实例


def run_spider(spider_name: str, **spider_args):
    settings = get_project_settings()
    settings.set("INSTALL_SHUTDOWN_HANDLERS", True)  # 允许信号处理
    process = CrawlerProcess(settings)
    # 将 spider_args 作为关键字参数传递给爬虫
    process.crawl(spider_name, **spider_args)
    process.start()


# 开启爬虫
@system.post("/spider/start")
async def start_spider(request: StartSpiderRequest):
    spider_name = request.spider_name
    spider_args = request.spider_args
    description = request.description
    spider_id = str(uuid.uuid4())
    # 在独立线程中运行爬虫
    p = Process(target=run_spider, args=(spider_name,), kwargs=spider_args)
    p.start()
    running_spiders[spider_id] = {
        "spider_name": spider_name,
        "process": p,
        "description": description,
        "start_time": int(time.time()),
        "spider_id": spider_id,
    }
    return {
        "message": "success",
        "spider_id": spider_id,
    }


@system.get("/spider/support")
def support():
    scrapys = [
        {
            "spider_name": "csdn_website_scrapy",
            "version": "1.0",
            "description": "CSDN 推荐爬虫任务",
            "icon":'https://img.icons8.com/?size=100&id=qYz8huKUwljl&format=png&color=000000',
            "args":[]
        },
        {
            "spider_name": "boss_website_scrapy",
            "version": "1.0",
            "description": "BOSS 直聘爬虫任务",
            "icon":'https://ts1.cn.mm.bing.net/th/id/R-C.7cb4bb3fc18ef32ab594c14eb070a54e?rik=cm2qfVwyVcwEZA&riu=http%3a%2f%2fwww.kuaipng.com%2fUploads%2fpic%2fw%2f2021%2f11-15%2f112916%2fwater_112916_698_698_.png&ehk=JtG6sCVyeVJSwlPY5c%2bAXLxOl%2fdwkxHlugBejEXX%2fqU%3d&risl=&pid=ImgRaw&r=0',
            "args":[
                {"工作名称":"job"},
                {"城市名称":"city"}]
        },
    ]
    return scrapys


# 查看正在运行的爬虫进程
@system.get("/spider/list")
async def list_all_spiders():
    try:
        spiders = []
        for spider_id, spider in running_spiders.items():
            status = True if spider["process"].is_alive() else False
            spiders.append(
                {
                    "spider_name": spider["spider_name"],
                    "start_time": spider["start_time"],
                    "spider_id": spider_id,
                    "status": status,
                    "description":spider['description'],
                }
            )
        return {"spiders": spiders}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# 检查爬虫状态
@system.post("/spider/status")
async def check_spider_status(request: StopSpiderRequest):
    spider_id = request.spider_id
    spider_process: Process = running_spiders.get(spider_id)

    if spider_process is None:
        raise HTTPException(status_code=404, detail="爬虫 ID 不存在或已停止")

    # 检查爬虫进程是否存活
    is_running = spider_process.is_alive()
    status = "运行中" if is_running else "已停止"

    return {"spider_id": spider_id, "status": status}


# 停止爬虫
@system.post("/spider/stop")
async def stop_spider(request: StopSpiderRequest):
    spider_id = request.spider_id
    spider_process: Process = running_spiders.get(spider_id)

    if spider_process is None:
        raise HTTPException(status_code=404, detail="爬虫 ID 不存在或已停止")

    spider_process = spider_process["process"]
    # # 强制停止爬虫
    try:
        os.kill(spider_process.pid, signal.SIGKILL)  # 使用 SIGKILL 信号终止进程
        spider_process.join()  # 等待进程终止
        del running_spiders[spider_id]  # 从全局字典中删除
    except Exception as e:
        del running_spiders[spider_id]
    return {"message": f"爬虫 {spider_id} 已停止"}


# 获取系统信息
@system.get("/system_info")
def get_system_info() -> dict:
    # 获取 CPU 占比
    cpu_usage = psutil.cpu_percent(interval=1)  # 获取当前 CPU 占比
    # 获取内存信息
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent  # 内存占比
    # 获取磁盘信息
    disk_info = psutil.disk_usage("/")
    disk_usage = disk_info.percent  # 磁盘占比
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
    }
