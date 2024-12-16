from elasticsearch import Elasticsearch
import os

from fastapi.logger import logger

es_url = os.getenv("ES_URL")
CSDN_DATA = "csdn_article_data"
BOSS_DATA = "boss_data"
es = Elasticsearch(es_url, timeout=30)

def init_es():
    if not es.indices.exists(index=CSDN_DATA):
        es.indices.create(
            index=CSDN_DATA,
            body={
                "mappings": {
                    "properties": {
                        "link": {"type": "keyword"},
                        "text": {
                            "type": "text",
                        },
                        "crawl_time": {"type": "date", "format": "epoch_second"},
                        "create_time": {"type": "date", "format": "epoch_second"},
                        "sentiment_score": {"type": "float"},
                        "category": {"type": "keyword"},
                        "read_count": {"type": "integer"},
                        "collection": {"type": "integer"},
                        "blog_digg_num": {"type": "integer"},
                        "embedding": {"type": "dense_vector", "dims": 384},
                    }
                }
            },
        )
    else:
        logger.info("ES: csdn_article_dataex already created")
   
    if not es.indices.exists(index=BOSS_DATA):
        es.indices.create(
            index=BOSS_DATA,
            body={
                "mappings": {
                    "properties": {
                        "link": {"type": "keyword"},
                        "boss_name": {"type": "keyword"},
                        "boss_title": {"type": "keyword"},
                        "job_name": {"type": "keyword"},
                        "salary_desc": {"type": "keyword"},
                        "job_labels": {"type": "keyword"},
                        "skills": {"type": "keyword"},
                        "job_experience": {"type": "keyword"},
                        "job_degree": {"type": "keyword"},
                        "city_name": {"type": "keyword"},
                        "area_district": {"type": "keyword"},
                        "business_district": {"type": "keyword"},
                        "location": {"type": "geo_point"},
                        "brand_name": {"type": "keyword"},
                        "brand_stage_name": {"type": "keyword"},
                        "brand_industry": {"type": "keyword"},
                        "brand_scale_name": {"type": "keyword"},
                        "welfare_list": {"type": "keyword"},
                        "create_time": {"type": "date", "format": "epoch_second"},
                    }
                }
            },
        )
    else:
        logger.info("ES: boss_detail_data already created")