from elasticsearch import Elasticsearch
import os

from fastapi.logger import logger
es_url = os.getenv('ES_URL')
INDEX_NAME = 'csdn_article_data'
es = Elasticsearch(es_url, timeout=30)

# INDEX2_NAME = 'csdn_article_data'
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(
        index=INDEX_NAME,
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
# if not es.indices.exists(index=INDEX2_NAME):
#     es.indices.create(
#         index=INDEX2_NAME,
#         body={
#             "mappings": {
#                 "properties": {
#                     "search_count": {"type": "integer"},
#                 }
#             }
#         },
#     )
        