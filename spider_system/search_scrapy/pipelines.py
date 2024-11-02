# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from search_scrapy.config.elasticsearch_config import es, INDEX_NAME
from search_scrapy.utils.nlp_transformers import get_sentence_embedding
from elasticsearch import exceptions

class SearchScrapyPipeline:
    def process_item(self, item, spider):
        return item


class CSDNScrapyPipeline:
    def __init__(self):
        self.INDEX_NAME = INDEX_NAME
        self.connect = es

    # 192.168.195.93:5601
    def process_item(self, item, spider):
        # 获取语义向量
        embedding = get_sentence_embedding(f"{item['text']}")
        unique_id = item["link"]  # 使用链接作为唯一标识符

        try:
            # 检查文档是否存在
            response = self.connect.get(index=self.INDEX_NAME, id=unique_id)
            existing_data = response['_source']

            # 检查数据是否有变化（此处使用简单的比较，您可以根据需要修改逻辑）
            if item != existing_data:  # 这里的比较可以自定义更细粒度的比较
                print(f"Updating document with ID: {unique_id}")
                # 更新数据
                self.connect.index(
                    index=self.INDEX_NAME,
                    id=unique_id,  # 使用唯一 ID 更新
                    body={
                        "link": item["link"],
                        "text": item["text"],
                        "embedding": embedding,
                        "crawl_time": item["crawl_time"],
                        "create_time": item["create_time"],
                        "sentiment_score": item["sentiment_score"],
                        "category": item["category"],
                        "read_count": item["read_count"],
                        "collection": item["collection"],
                        "blog_digg_num": item["blog_digg_num"],
                    },
                )
            else:
                print(f"No changes detected for ID: {unique_id}, skipping update.")
        
        except exceptions.NotFoundError:
            # 如果文档不存在，执行插入
            print(f"Inserting new document with ID: {unique_id}")
            self.connect.index(
                index=self.INDEX_NAME,
                id=unique_id,  # 使用唯一 ID 插入
                body={
                    "link": item["link"],
                    "text": item["text"],
                    "embedding": embedding,
                    "crawl_time": item["crawl_time"],
                    "create_time": item["create_time"],
                    "sentiment_score": item["sentiment_score"],
                    "category": item["category"],
                    "read_count": item["read_count"],
                    "collection": item["collection"],
                    "blog_digg_num": item["blog_digg_num"],
                },
            )
        except exceptions.ElasticsearchException as e:
            print(f"Elasticsearch error: {e}")

        return item