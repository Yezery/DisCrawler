# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
# useful for handling different item types with a single interface
from service.config.elasticsearch_config import es, CSDN_DATA, BOSS_DATA
from search_scrapy.utils.nlp_transformers import get_sentence_embedding
from elasticsearch import exceptions


class SearchScrapyPipeline:
    def process_item(self, item, spider):
        return item

class CSDNScrapyPipeline:
    def __init__(self):
        self.CSDN_DATA = CSDN_DATA
        self.connect = es

    # 192.168.195.93:5601
    def process_item(self, item, spider):
        # 获取语义向量
        embedding = get_sentence_embedding(f"{item['text']}")
        unique_id = item["link"]  # 使用链接作为唯一标识符

        try:
            # 检查文档是否存在
            response = self.connect.get(index=self.CSDN_DATA, id=unique_id)
            existing_data = response["_source"]

            # 检查数据是否有变化（此处使用简单的比较，您可以根据需要修改逻辑）
            if item != existing_data:  # 这里的比较可以自定义更细粒度的比较
                logging.debug(f"Updating document with ID: {unique_id}")
                # 更新数据
                self.connect.index(
                    index=self.CSDN_DATA,
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
                logging.debug(f"No changes detected for ID: {unique_id}, skipping update.")

        except exceptions.NotFoundError:
            # 如果文档不存在，执行插入
            logging.info(f"Inserting new document with ID: {unique_id}")
            self.connect.index(
                index=self.CSDN_DATA,
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
        except Exception as e:
            logging.error(f"Elasticsearch error: {e}")

        return item


class BOSSScrapyPipeline:
    def __init__(self):
        self.CSDN_DATA = BOSS_DATA
        self.connect = es

    # 192.168.195.93:5601
    def process_item(self, item, spider):
        unique_id = str(item["link"])  # 使用链接作为唯一标识符

        try:
            # 检查文档是否存在
            response = self.connect.get(index=self.CSDN_DATA, id=unique_id)
            existing_data = response["_source"]
            # 检查数据是否有变化
            if item != existing_data:  # 这里的比较可以自定义更细粒度的比较
                logging.DEBUG(f"Updating document with ID: {unique_id}")
                # 更新数据
                self.connect.index(
                    index=self.CSDN_DATA,
                    id=unique_id,  # 使用唯一 ID 更新
                    body={
                        "link": item["link"],
                        "boss_name": item["boss_name"],
                        "boss_title": item["boss_title"],
                        "job_name": item["job_name"],
                        "salary_desc": item["salary_desc"],
                        "job_labels": item["job_labels"],
                        "skills": item["skills"],
                        "job_experience": item["job_experience"],
                        "job_degree": item["job_degree"],
                        "city_name": item["city_name"],
                        "area_district": item["area_district"],
                        "business_district": item["business_district"],
                        "location": item["location"],
                        "brand_name": item["brand_name"],
                        "brand_stage_name": item["brand_stage_name"],
                        "brand_industry": item["brand_industry"],
                        "brand_scale_name": item["brand_scale_name"],
                        "welfare_list": item["welfare_list"],
                        "create_time": item["create_time"],
                    },
                )
            else:
                logging.warning(f"No changes detected for ID: {unique_id}, skipping update.")

        except exceptions.NotFoundError:
            # 如果文档不存在，执行插入
            logging.info(f"Inserting new document with ID: {unique_id}")
            self.connect.index(
                index=self.CSDN_DATA,
                id=unique_id,  # 使用唯一 ID 插入
                body={
                    "link": item["link"],
                        "boss_name": item["boss_name"],
                        "boss_title": item["boss_title"],
                        "job_name": item["job_name"],
                        "salary_desc": item["salary_desc"],
                        "job_labels": item["job_labels"],
                        "skills": item["skills"],
                        "job_experience": item["job_experience"],
                        "job_degree": item["job_degree"],
                        "city_name": item["city_name"],
                        "area_district": item["area_district"],
                        "business_district": item["business_district"],
                        "location": item["location"],
                        "brand_name": item["brand_name"],
                        "brand_stage_name": item["brand_stage_name"],
                        "brand_industry": item["brand_industry"],
                        "brand_scale_name": item["brand_scale_name"],
                        "welfare_list": item["welfare_list"],
                        "create_time": item["create_time"],
                },
            )
        except Exception as e:
            logging.error(f"Elasticsearch error: {e}")

        return item
