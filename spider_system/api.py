import os
import time
from fastapi import FastAPI, HTTPException
import psutil
from pydantic import BaseModel
import uvicorn
from search_scrapy.config.elasticsearch_config import es, INDEX_NAME
from search_scrapy.utils.nlp_transformers import get_sentence_embedding
from fastapi.middleware.cors import CORSMiddleware
from collections import Counter
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import uuid
from multiprocessing import Process
from search_scrapy.utils.convert import bytesToGB
import signal
from dotenv import load_dotenv
app = FastAPI()
running_spiders = {}  # 用于保存正在运行的爬虫实例
load_dotenv()
port = os.getenv('PORT')
# 开启跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str


# 查询
@app.post("/search")
async def search_by_semantics(searchRequest: SearchRequest):
    query = searchRequest.query
    # 获取查询语义嵌入
    query_embedding = get_sentence_embedding(
        query, model_path="search_scrapy/models/all-MiniLM-L6-v2"
    )

    # 使用 Elasticsearch 的 script_score 计算相似度
    script_query = {
        "bool": {
            "must": [{"match": {"text": {"query": query, "boost": 1.0}}}],
            "should": [  # 语义相似度补充
                {
                    "script_score": {
                        "query": {"match_all": {}},  # 匹配所有文档
                        "script": {
                            # 结合余弦相似度，并增加权重来提高它的重要性
                            "source": """
                                double cosineSim = cosineSimilarity(params.query_vector, 'embedding');
                                return cosineSim * 2.0 + 1.0;
                            """,
                            "params": {"query_vector": query_embedding.tolist()},
                        },
                    }
                }
            ],
            "minimum_should_match": 1,  # 至少满足一个 `should` 条件
        }
    }

    # 执行搜索
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": script_query,
            "sort": [
                {"_score": {"order": "desc"}},
            ],
            # "collapse": {"field": "link.keyword"},  # 基于 'link' 字段去重
        },
        size=10,
    )

    # 返回结果
    result = [
        {
            "link": hit["_source"].get("link"),
            "title": hit["_source"].get("text"),
            "read_count": hit["_source"].get("read_count"),
            "collection": hit["_source"].get("collection"),
            "blog_digg_num": hit["_source"].get("blog_digg_num"),
            "crawl_time": hit["_source"].get("crawl_time"),
            "create_time": hit["_source"].get("create_time"),
        }
        for hit in results["hits"]["hits"]
    ]
    return {"results": result}


# 获取网站数量
@app.get("/getWebsiteCount")
def count():
    count = es.count(index=INDEX_NAME)["count"]
    return count


# 获取词云数据
@app.get("/getWordCloud")
def wordCloud():
    # 使用 terms 聚合直接计算词频
    results = es.search(
        index=INDEX_NAME,
        body={"query": {"match_all": {}}},
    )
    categories = []
    for hit in results["hits"]["hits"]:
        # 假设 categories 是一个数组
        if "category" in hit["_source"]:
            categories.extend(hit["_source"]["category"])
    # 统计各个类别的出现次数
    counter = Counter(categories)
    sorted_categories = counter.most_common()
    word_cloud_data = [
        {"name": category, "value": count} for category, count in sorted_categories
    ]
    return word_cloud_data


# 获取观看量排名
@app.get("/getReadCount")
def getReadCount():
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": {"match_all": {}},
            "sort": [{"read_count": {"order": "desc"}}],
            "size": 100,
        },
    )
    watch_count_data = [
        {
            "link": hit["_source"].get("link"),
            "title": hit["_source"].get("text"),
            "read_count": hit["_source"].get("read_count"),
            "collection": hit["_source"].get("collection"),
            "blog_digg_num": hit["_source"].get("blog_digg_num"),
            "crawl_time": hit["_source"].get("crawl_time"),
            "create_time": hit["_source"].get("create_time"),
        }
        for hit in results["hits"]["hits"]
    ]
    return watch_count_data


# 获取点赞量排名
@app.get("/getBlogDiggNum")
def getBlogDiggNum():
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": {"match_all": {}},
            "sort": [{"blog_digg_num": {"order": "desc"}}],
            "size": 100,
        },
    )
    blog_digg_num_data = [
        {
            "link": hit["_source"].get("link"),
            "title": hit["_source"].get("text"),
            "read_count": hit["_source"].get("read_count"),
            "collection": hit["_source"].get("collection"),
            "blog_digg_num": hit["_source"].get("blog_digg_num"),
            "crawl_time": hit["_source"].get("crawl_time"),
            "create_time": hit["_source"].get("create_time"),
        }
        for hit in results["hits"]["hits"]
    ]
    return blog_digg_num_data


# 获取收藏量排名
@app.get("/getCollectCount")
def getCollectCount():
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": {"match_all": {}},
            "sort": [{"collection": {"order": "desc"}}],
            "size": 100,
        },
    )
    collection_num_data = [
        {
             "link": hit["_source"].get("link"),
            "title": hit["_source"].get("text"),
            "read_count": hit["_source"].get("read_count"),
            "collection": hit["_source"].get("collection"),
            "blog_digg_num": hit["_source"].get("blog_digg_num"),
            "crawl_time": hit["_source"].get("crawl_time"),
            "create_time": hit["_source"].get("create_time"),
        }
        for hit in results["hits"]["hits"]
    ]
    return collection_num_data


# 获取综合排名
@app.get("/getRanked")
def get_ranked_items():
    results = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "params.readWeight * doc['read_count'].value + params.likeWeight * doc['blog_digg_num'].value + params.favoriteWeight * doc['collection'].value",
                        "params": {
                            "readWeight": 0.1,
                            "likeWeight": 0.2,
                            "favoriteWeight": 0.7,
                        },
                    },
                }
            },
            "size": 100,  # 返回前 10 条记录，可根据需要调整
            "sort": [{"_score": {"order": "desc"}}],  # 按综合分数降序排列
        },
    )

    ranked_items = [
        {
            "link": hit["_source"].get("link"),
            "title": hit["_source"].get("text"),
            "read_count": hit["_source"].get("read_count"),
            "collection": hit["_source"].get("collection"),
            "blog_digg_num": hit["_source"].get("blog_digg_num"),
            "crawl_time": hit["_source"].get("crawl_time"),
            "create_time": hit["_source"].get("create_time"),
        }
        for hit in results["hits"]["hits"]
    ]

    return ranked_items


# 获取时间段内爬虫数据量
@app.get("/getDataCounts")
def get_data_counts():
    # 定义时间范围和对应标签
    time_ranges = {
        "1分钟": "now-1m",        # 过去1分钟的数据
        "3分钟": "now-3m",     # 过去3分钟的数据
        "6分钟": "now-6m",     # 过去6分钟的数据
        "10分钟": "now-10m",   # 过去10分钟的数据
        # "半小时": "now-30m",  # 过去半小时的数据
        # "1小时": "now-1h",  # 过去1小时的数据
        # "3小时": "now-3h",  # 过去3小时的数据
        # "6小时": "now-6h",  # 过去6小时的数据
        # "12小时": "now-12h",  # 过去12小时的数据
    }

    # 初始化存储条数的字典
    counts = {}

    # 针对每个时间范围进行查询
    for label, time_range in time_ranges.items():
        # 构建查询
        body = {"query": {"range": {"crawl_time": {"gte": time_range, "lte": "now"}}}}

        # 使用 count API 获取匹配条数
        result = es.count(index=INDEX_NAME, body=body)
        counts[label] = result["count"]

    # 格式化为 ECharts 可接受的数据格式
    echarts_data = {"xAxis": list(counts.keys()), "data": list(counts.values())}

    return echarts_data


class StartSpiderRequest(BaseModel):
    spider_name: str


class StopSpiderRequest(BaseModel):
    spider_id: str


def run_spider(spider_name: str):
    settings = get_project_settings()
    settings.set("INSTALL_SHUTDOWN_HANDLERS", True)  # 允许信号处理
    process = CrawlerProcess(settings)
    process.crawl(spider_name)
    process.start()


# 开启爬虫
@app.post("/spider/start")
async def start_spider(request: StartSpiderRequest):
    spider_name = request.spider_name

    if spider_name == "csdn_website_scrapy":
        spider = spider_name
    else:
        raise HTTPException(status_code=400, detail="未知的爬虫名称")

    spider_id = str(uuid.uuid4())
    # 在独立线程中运行爬虫
    p = Process(target=run_spider, args=(spider,))
    p.start()
    running_spiders[spider_id] = {
        "spider_name": spider_name,
        "process": p,
        "start_time": int(time.time()),
        "spider_id": spider_id,
    }
    return {
        "message": "success",
        "spider_id": spider_id,
    }

@app.get("/spider/support")
def support():
    scrapys = []
    scrapys.append(
        {"spider_name":"csdn_website_scrapy","version":"1.0","description":"CSDN 推荐爬虫任务"}
    )
    return scrapys

# 查看正在运行的爬虫进程
@app.get("/spider/list")
async def list_all_spiders():
    try:
        spiders = []
        for spider_id, spider in running_spiders.items():
            status = True if spider["process"].is_alive() else False
            spiders.append(
                {
                    "spider_name":spider['spider_name'],
                    "start_time": spider['start_time'],
                    "spider_id": spider_id,
                    "status": status,
                    "description":"CSDN 推荐爬虫"
                }
            )
        return {"spiders": spiders}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


# 检查爬虫状态
@app.post("/spider/status")
async def check_spider_status(request: StopSpiderRequest):
    spider_id = request.spider_id
    spider_process = running_spiders.get(spider_id)

    if spider_process is None:
        raise HTTPException(status_code=404, detail="爬虫 ID 不存在或已停止")

    # 检查爬虫进程是否存活
    is_running = spider_process.is_alive()
    status = "运行中" if is_running else "已停止"

    return {"spider_id": spider_id, "status": status}


# 停止爬虫
@app.post("/spider/stop")
async def stop_spider(request: StopSpiderRequest):
    spider_id = request.spider_id
    spider_process = running_spiders.get(spider_id)

    if spider_process is None:
        raise HTTPException(status_code=404, detail="爬虫 ID 不存在或已停止")
    
    spider_process = spider_process['process']
    # # 强制停止爬虫
    try :
        os.kill(spider_process.pid, signal.SIGKILL)  # 使用 SIGKILL 信号终止进程
        spider_process.join()  # 等待进程终止
        del running_spiders[spider_id]  # 从全局字典中删除
    except Exception as e:
         del running_spiders[spider_id]  
    return {"message": f"爬虫 {spider_id} 已停止"}


# 获取系统信息
@app.get("/system_info")
def get_system_info() -> dict:
    # 获取 CPU 占比
    cpu_usage = psutil.cpu_percent(interval=1)  # 获取当前 CPU 占比
    # 获取内存信息
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent  # 内存占比
    total_memory = memory_info.total  # 总内存
    used_memory = memory_info.used  # 已使用内存
    available_memory = memory_info.available  # 可用内存
    # 获取磁盘信息
    disk_info = psutil.disk_usage("/")
    disk_usage = disk_info.percent  # 磁盘占比
    total_disk = disk_info.total  # 总磁盘
    # 获取网络信息
    network_info = psutil.net_io_counters()
    bytes_sent = network_info.bytes_sent  # 发送的字节数
    bytes_recv = network_info.bytes_recv  # 接收的字节数
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "total_memory": bytesToGB(total_memory),
        "used_memory": bytesToGB(used_memory),
        "available_memory": bytesToGB(available_memory),
        "total_disk": bytesToGB(total_disk),
        "bytes_sent": bytesToGB(bytes_sent),
        "bytes_recv": bytesToGB(bytes_recv),
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(port))
