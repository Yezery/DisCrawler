from collections import Counter
from fastapi import APIRouter

from service.config.elasticsearch_config import es, CSDN_DATA
from search_scrapy.utils.nlp_transformers import get_sentence_embedding
from service.dao.dto.csdn.SearchRequest import SearchRequest
from service.dao.vo.csdn.WebsiteCount import WebsiteCount
from service.utils.r import Result
csdn = APIRouter()

# 查询
@csdn.post("/search")
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
        index=CSDN_DATA,
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
    
    return Result.success(result)


# 获取网站数量
@csdn.get("/getWebsiteCount")
def count():
    return Result.success(es.count(index=CSDN_DATA)["count"])


# 获取词云数据
@csdn.get("/getWordCloud")
def wordCloud():
    # 使用 terms 聚合直接计算词频
    results = es.search(
        index=CSDN_DATA,
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
    return Result.success(word_cloud_data)


# 获取观看量排名
@csdn.get("/getReadCount")
def getReadCount():
    results = es.search(
        index=CSDN_DATA,
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
    return Result.success(watch_count_data)


# 获取点赞量排名
@csdn.get("/getBlogDiggNum")
def getBlogDiggNum():
    results = es.search(
        index=CSDN_DATA,
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
    return Result.success(blog_digg_num_data)


# 获取收藏量排名
@csdn.get("/getCollectCount")
def getCollectCount():
    results = es.search(
        index=CSDN_DATA,
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
    return Result.success(collection_num_data)


# 获取综合排名
@csdn.get("/getRanked")
def get_ranked_items():
    results = es.search(
        index=CSDN_DATA,
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

    return Result.success(ranked_items)


# 获取时间段内爬虫数据量
@csdn.get("/getDataCounts")
def get_data_counts():
    # 定义时间范围和对应标签
    time_ranges = {
        "1分钟": "now-1m",  # 过去1分钟的数据
        "3分钟": "now-3m",  # 过去3分钟的数据
        "6分钟": "now-6m",  # 过去6分钟的数据
        "10分钟": "now-10m",  # 过去10分钟的数据
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
        result = es.count(index=CSDN_DATA, body=body)
        counts[label] = result["count"]

    # 格式化为 ECharts 可接受的数据格式
    echarts_data = {"xAxis": list(counts.keys()), "data": list(counts.values())}

    return Result.success(echarts_data)

