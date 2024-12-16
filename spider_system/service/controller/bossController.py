import re
from fastapi import APIRouter
from service.config.elasticsearch_config import es, BOSS_DATA
from service.dao.dto.boss.JobPie import JobPie
from service.utils.r import Result

boss = APIRouter()


@boss.post("/job/salary")
def job_salary(jobPie: JobPie = None):
    jobPieName = jobPie.job_name
    jobPieCityName = jobPie.city_name

    def parse_salary(salary_str):
        salary_str = salary_str.strip()

        # 处理日薪（如 180-200元/天）
        daily_pattern = r"(\d+)-(\d+)\s*元/天"
        daily_match = re.match(daily_pattern, salary_str)
        if daily_match:
            low_daily = int(daily_match.group(1))
            high_daily = int(daily_match.group(2))
            avg_daily_salary = (low_daily + high_daily) / 2
            return avg_daily_salary * 22  # 假设一个月22个工作日

        # 处理年薪（如 20k-30k/15薪）
        annual_pattern = r"(\d+)k-(\d+)k[·\s]*(\d+)薪"
        annual_match = re.match(annual_pattern, salary_str)
        if annual_match:
            low = int(annual_match.group(1)) * 1000
            high = int(annual_match.group(2)) * 1000
            avg_annual_salary = (low + high) / 2
            return avg_annual_salary / 12  # 转换为月薪

        # 处理月薪（如 3000/月）
        monthly_pattern = r"(\d+)\s*/\s*月"
        monthly_match = re.match(monthly_pattern, salary_str)
        if monthly_match:
            return int(monthly_match.group(1))

        # 处理区间薪资（如 4-6K、5-10K）
        range_pattern = r"(\d+)-(\d+)\s*K"
        range_match = re.match(range_pattern, salary_str)
        if range_match:
            low = int(range_match.group(1)) * 1000
            high = int(range_match.group(2)) * 1000
            return (low + high) / 2  # 取中间值

        # 处理带有 13薪 或 14薪 的薪资格式
        special_pattern = r"(\d+)-(\d+)\s*K·(\d+)薪"
        special_match = re.match(special_pattern, salary_str)
        if special_match:
            low = int(special_match.group(1)) * 1000
            high = int(special_match.group(2)) * 1000
            avg_annual_salary = (low + high) / 2
            return avg_annual_salary / 12  # 转换为月薪

        # 如果没有匹配，返回 None
        return None

    def fetch_all_salaries_from_es(CSDN_DATA):
        salaries = []
        if jobPie is None:
            query = {"query": {"match_all": {}}}
        else:
            query = {
                "query": {
                    "bool": {
                        "must": [{"wildcard": {"job_name": "*" + jobPieName + "*"}}],
                        "filter": [],
                    }
                }
            }

            # 根据 city_name 是否为空进行条件添加
            if jobPieCityName:
                query["query"]["bool"]["filter"].append(
                    {"term": {"city_name": jobPieCityName}}
                )

        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query, scroll="2m", size=1000)
        scroll_id = response["_scroll_id"]

        for hit in response["hits"]["hits"]:
            salary_desc = hit["_source"].get("salary_desc")
            if salary_desc:
                parsed_salary = parse_salary(salary_desc)
                if parsed_salary is not None:
                    salaries.append(parsed_salary)

        # 循环获取后续批次数据
        while len(response["hits"]["hits"]):
            response = es.scroll(scroll_id=scroll_id, scroll="2m")
            scroll_id = response["_scroll_id"]

            for hit in response["hits"]["hits"]:
                salary_desc = hit["_source"].get("salary_desc")
                if salary_desc:
                    parsed_salary = parse_salary(salary_desc)
                    if parsed_salary is not None:
                        salaries.append(parsed_salary)

        return salaries

    def calculate_salary_statistics(salaries):
        if not salaries:
            return None, None, {}

        max_salary = max(salaries)
        min_salary = min(salaries)

        # 定义薪资段
        salary_segments = {
            "0-3K": 0,
            "3-5K": 0,
            "5-8K": 0,
            "8-12K": 0,
            "12-20K": 0,
            "20K以上": 0,
        }

        # 统计每个薪资段的数量
        for salary in salaries:
            if salary < 3000:
                salary_segments["0-3K"] += 1
            elif 3000 <= salary < 5000:
                salary_segments["3-5K"] += 1
            elif 5000 <= salary < 8000:
                salary_segments["5-8K"] += 1
            elif 8000 <= salary < 12000:
                salary_segments["8-12K"] += 1
            elif 12000 <= salary < 20000:
                salary_segments["12-20K"] += 1
            else:
                salary_segments["20K以上"] += 1

        return max_salary, min_salary, salary_segments

    CSDN_DATA = BOSS_DATA
    salaries = fetch_all_salaries_from_es(CSDN_DATA)
    max_salary, min_salary, salary_segments = calculate_salary_statistics(salaries)

    print(f"最高薪资: {max_salary}, 最低薪资: {min_salary}")
    print("薪资段占比:", salary_segments)
    return Result.success(
        {
            "max_salary": max_salary,
            "min_salary": min_salary,
            "salary_segments": salary_segments,
        }
    )


@boss.get("/job/distribution")
async def job_distribution():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {
                        "field": "city_name",
                    },
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            city_name = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"name": city_name, "value": doc_count})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/job/degree")
async def job_degree():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_degrees": {
                    "terms": {
                        "field": "job_degree",
                    }
                }
            },
        }
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_degrees"]["buckets"]:
            degree = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"value": doc_count, "name": degree})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/job/skills")
async def job_skills():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {
                        "field": "skills",
                    }
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            city_name = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"name": city_name, "value": doc_count})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/job/experience")
async def job_experience():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {"field": "job_experience", "size": 100},
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            city_name = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"name": city_name, "value": doc_count})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/company/finance")
async def company_finance():
    try:
        CSDN_DATA = BOSS_DATA
        data = {}
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {
                        "field": "brand_stage_name",
                    },
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            brand_stage = bucket["key"]
            doc_count = bucket["doc_count"]

            # 将 brand_stage 为 "" 或 "不需要融资" 合并为 "未融资"
            if not brand_stage or brand_stage == "不需要融资":
                brand_stage = "未融资"

            # 累计统计相同 name 的 value
            if brand_stage in data:
                data[brand_stage] += doc_count
            else:
                data[brand_stage] = doc_count

        # 转换为列表格式
        result = [{"name": k, "value": v} for k, v in data.items()]
        print(result)
    except Exception as e:
        return Result.bad_request(e)
    return Result.success(result)



@boss.get("/company/size")
async def company_size():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {
                        "field": "brand_scale_name",
                    },
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            city_name = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"name": city_name, "value": doc_count})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/company/industry")
async def company_industry():
    try:
        CSDN_DATA = BOSS_DATA
        data = []
        # 构造聚合查询
        query = {
            "size": 0,  # 不返回文档，只返回聚合结果
            "aggs": {
                "unique_cities": {
                    "terms": {
                        "field": "brand_industry",
                    },
                }
            },
        }
        # 初始化滚动查询
        response = es.search(index=CSDN_DATA, body=query)
        for bucket in response["aggregations"]["unique_cities"]["buckets"]:
            city_name = bucket["key"]
            doc_count = bucket["doc_count"]
            data.append({"name": city_name, "value": doc_count})
    except Exception as e:
        return Result.fail(e)
    return Result.success(data)


@boss.get("/job/salary/all")
async def job_salary_all():
    def categorize_salary(salary_str):
        """将薪资字符串分类到不同区间"""
        # 初始化结果字典
        salary_ranges = {
            "0-3K": 0,
            "3-5K": 0,
            "5-8K": 0,
            "8-12K": 0,
            "12-20K": 0,
            "20K以上": 0,
        }

        # 提取数值范围
        import re

        match = re.search(r"(\d+)-(\d+)(K|元/天)", salary_str)
        if match:
            lower = int(match.group(1))
            upper = int(match.group(2))
            unit = match.group(3)

            # 处理单位为 K 或 元/天
            if unit == "元/天":
                lower, upper = lower * 30, upper * 30  # 按 30 天/月转换

            # 分类范围
            avg_salary = (lower + upper) / 2
            if avg_salary < 3000:
                salary_ranges["0-3K"] += 1
            elif avg_salary < 5000:
                salary_ranges["3-5K"] += 1
            elif avg_salary < 8000:
                salary_ranges["5-8K"] += 1
            elif avg_salary < 12000:
                salary_ranges["8-12K"] += 1
            elif avg_salary < 20000:
                salary_ranges["12-20K"] += 1
            else:
                salary_ranges["20K以上"] += 1

        return salary_ranges

    try:
        CSDN_DATA = BOSS_DATA
        # 构造聚合查询
        # 聚合查询
        query = {
            "size": 0,
            "aggs": {
                "salary_buckets": {
                    "terms": {
                        "field": "salary_desc",
                        "size": 10000,  # 确保能返回足够的薪资分组
                    }
                }
            },
        }
        response = es.search(index=CSDN_DATA, body=query)
        # 获取所有薪资字段
        buckets = response["aggregations"]["salary_buckets"]["buckets"]
        salaries = [bucket["key"] for bucket in buckets]
        # 初始化分类结果
        final_result = {
            "0-3K": 0,
            "3-5K": 0,
            "5-8K": 0,
            "8-12K": 0,
            "12-20K": 0,
            "20K以上": 0,
        }

        # 遍历薪资字段并分类
        for salary in salaries:
            categorized = categorize_salary(salary)
            for key in final_result:
                final_result[key] += categorized[key]

    except Exception as e:
        return Result.fail(e)
    return Result.success(final_result)


# 获取数据量
@boss.get("/count/data")
def count():
    return Result.success(es.count(index=BOSS_DATA)["count"])


# 获取城市数量
@boss.get("/count/city")
def count_city():
    response = es.search(
        index=BOSS_DATA,
        body={
            "size": 0,
            "aggs": {"count_by_city": {"terms": {"field": "city_name"}}},
        },
    )
    return Result.success(len(response["aggregations"]["count_by_city"]["buckets"]))


# 获取最新的数据时间
@boss.get("/latest/data")
def latest_data():
    try:
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 0,
                "aggs": {"latest_data": {"max": {"field": "create_time"}}},
            },
        )
        return Result.success(response["aggregations"]["latest_data"]["value"])
    except Exception as e:
        return Result.bad_request(e)


# 获取所有招聘公司数量
@boss.get("/count/company")
def count_company():
    try:
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 0,
                "aggs": {"count_by_company": {"cardinality": {"field": "brand_name"}}},
            },
        )
        return Result.success(response["aggregations"]["count_by_company"]["value"])
    except Exception as e:
        return Result.bad_request(e)


@boss.get("/analysis/jobkey")
def analysis_job_key():
    try:
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 0,  # 不返回具体文档
                "aggs": {
                    "skills_agg": {
                        "terms": {
                            "field": "skills",  # 按 skills 字段进行分组（注意需为 keyword 类型）
                            "size": 10,  # 返回前 100 个技能
                            "order": {"_count": "desc"},  # 根据岗位数量排序
                        },
                        "aggs": {
                            "unique_companies": {
                                "cardinality": {  # 计算相关公司数量
                                    "field": "brand_name"
                                }
                            },
                            "job_count": {
                                "value_count": {  # 统计岗位数量
                                    "field": "job_name"  # 假设岗位信息字段是 job_title
                                }
                            },
                        },
                    }
                },
            },
        )
        # 解析 Elasticsearch 返回的聚合结果
        buckets = response["aggregations"]["skills_agg"]["buckets"]

        # yAxis 的数据（技能名称）
        y_axis = [bucket["key"] for bucket in buckets]

        # series 数据
        company_series_data = [
            bucket["unique_companies"]["value"] for bucket in buckets
        ]
        job_series_data = [bucket["job_count"]["value"] for bucket in buckets]
        # 转换为 ECharts 所需的数据结构
        chart_data = {
            "yAxis": {"type": "category", "inverse": True, "data": y_axis},
            "series": [
                {"name": "招聘公司", "type": "bar", "data": company_series_data},
                {"name": "招聘岗位", "type": "bar", "data": job_series_data},
            ],
        }
        return Result.success(chart_data)
    except Exception as e:
        return Result.bad_request(e)


@boss.get("/analysis/salary_brand")
async def salary_by_brand():
    try:
        # 初次查询，设置 scroll 参数（例如1分钟），每次返回1000条数据
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 1000,  # 每次返回1000条数据
                "_source": ["brand_stage_name", "salary_desc"],  # 只返回需要的字段
                "query": {
                    "regexp": {"salary_desc": ".*K.*"}  # 匹配包含 "K" 的薪资
                },
            },
            scroll="1m"  # 设置 scroll 过期时间为1分钟
        )

        # 获取 scroll_id，用于获取后续数据
        scroll_id = response["_scroll_id"]

        # 数据存储
        stage_salary_data = {}

        # 正则匹配 "25-45K" 或 "25-45K·14薪" 的数据
        valid_salary_pattern = re.compile(r"(\d+)-(\d+)K(?:·\d+薪)?")

        # 处理当前批次的结果
        while len(response["hits"]["hits"]) > 0:
            for hit in response["hits"]["hits"]:
                stage_name = hit["_source"]["brand_stage_name"]
                salary_desc = hit["_source"]["salary_desc"]

                # 将空值或 "不需要融资" 全部归为 "未融资"
                if not stage_name or stage_name == "不需要融资":
                    stage_name = "未融资"

                # 匹配有效薪资
                match = valid_salary_pattern.match(salary_desc)
                if match:
                    # 解析最小和最大薪资
                    min_salary = int(match.group(1)) * 1000
                    max_salary = int(match.group(2)) * 1000

                    # 按企业类型分类存储数据
                    if stage_name not in stage_salary_data:
                        stage_salary_data[stage_name] = {
                            "max_salaries": [],
                            "min_salaries": [],
                        }

                    stage_salary_data[stage_name]["max_salaries"].append(max_salary)
                    stage_salary_data[stage_name]["min_salaries"].append(min_salary)

            # 使用 scroll_id 获取后续数据
            response = es.scroll(
                scroll_id=scroll_id,
                scroll="1m"  # 每次滚动间隔1分钟
            )
            scroll_id = response["_scroll_id"]

        # 聚合每种企业类型的最高和最低薪资
        categories = []
        max_salaries = []
        min_salaries = []

        for stage_name, salaries in stage_salary_data.items():
            categories.append(stage_name)
            max_salaries.append(max(salaries["max_salaries"]))
            min_salaries.append(min(salaries["min_salaries"]))

        # 清除 scroll 上下文，释放资源
        es.clear_scroll(scroll_id=scroll_id)

        # 输出 ECharts 配置
        echarts_option = {
            "title": {
                "text": "不同融资阶段的薪资分布"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "cross"
                }
            },
            "legend": {
                "data": ["最高薪水", "最低薪水"]
            },
            "grid": {
                "left": '3%',
                "right": '4%',
                "bottom": '3%',
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 30
                }
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {
                    "name": "最高薪水",
                    "type": "line",
                    "data": max_salaries,
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "{c} 元"
                    }
                },  # 最高薪水
                {
                    "name": "最低薪水",
                    "type": "line",
                    "data": min_salaries,
                    "label": {
                        "show": True,
                        "position": "top",
                        "formatter": "{c} 元"
                    }
                },  # 最低薪水
            ],
        }
        return Result.success(echarts_option)
    except Exception as e:
        return Result.bad_request(str(e))

@boss.get("/analysis/salary_companySize")
async def salary_by_companySize():
    try:
        # 初次查询，设置 scroll 参数（例如1分钟），每次返回1000条数据
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 1000,  # 每次返回1000条数据
                "_source": ["brand_scale_name", "salary_desc"],  # 只返回需要的字段
                "query": {
                    "regexp": {"salary_desc": ".*K.*"}  # 初步匹配包含 "K" 的薪资
                },
            },
            scroll="1m"  # 设置scroll过期时间为1分钟
        )

        # 获取scroll_id，用于获取后续数据
        scroll_id = response["_scroll_id"]

        # 数据存储
        stage_salary_data = {}

        # 正则匹配 "25-45K" 或 "25-45K·14薪" 的数据
        valid_salary_pattern = re.compile(r"(\d+)-(\d+)K(?:·\d+薪)?")

        # 处理当前批次的结果
        while len(response["hits"]["hits"]) > 0:
            for hit in response["hits"]["hits"]:
                scale_name = hit["_source"]["brand_scale_name"]
                salary_desc = hit["_source"]["salary_desc"]

                # 匹配有效薪资
                match = valid_salary_pattern.match(salary_desc)
                if match:
                    # 解析最小和最大薪资
                    min_salary = int(match.group(1)) * 1000
                    max_salary = int(match.group(2)) * 1000

                    # 按公司规模分类存储数据
                    if scale_name not in stage_salary_data:
                        stage_salary_data[scale_name] = {
                            "max_salaries": [],
                            "min_salaries": [],
                        }

                    stage_salary_data[scale_name]["max_salaries"].append(max_salary)
                    stage_salary_data[scale_name]["min_salaries"].append(min_salary)

            # 使用scroll_id获取后续数据
            response = es.scroll(
                scroll_id=scroll_id,
                scroll="1m",  # 每次滚动间隔1分钟
            )
            scroll_id = response["_scroll_id"]

        # 聚合每种公司规模的最高和最低薪资
        categories = []
        max_salaries = []
        min_salaries = []

        for scale_name, salaries in stage_salary_data.items():
            categories.append(scale_name)
            max_salaries.append(max(salaries["max_salaries"]))
            min_salaries.append(min(salaries["min_salaries"]))

        # 清除scroll上下文，释放资源
        es.clear_scroll(scroll_id=scroll_id)
        
        # 输出 ECharts 配置
        echarts_option = {
            "title": {
                "text": "不同公司规模的薪资分布"
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "cross"
                }
            },
            "legend": {
                "data": ["最高薪水", "最低薪水"]
            },
            "grid": {
                "left": '3%',
                "right": '4%',
                "bottom": '3%',
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 30
                }
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {"name": "最高薪水", "type": "line", "data": max_salaries, "label": {
                    "show": True,
                    "position": "top",
                    "formatter": "{c} 元"
                }},  # 最高薪水
                {"name": "最低薪水", "type": "line", "data": min_salaries, "label": {
                    "show": True,
                    "position": "top",
                    "formatter": "{c} 元"
                }},  # 最低薪水
            ],
        }
        return Result.success(echarts_option)
    except Exception as e:
        return Result.bad_request(str(e))

@boss.get("/analysis/salary_degree")
async def salary_by_degree():
    try:
        # 初次查询，设置 scroll 参数（例如1分钟），每次返回1000条数据
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 1000,  # 每次返回1000条数据
                "_source": ["job_degree", "salary_desc"],  # 只返回需要的字段
                "query": {
                    "regexp": {"salary_desc": ".*K.*"}  # 初步匹配包含 "K" 的薪资
                },
            },
            scroll="1m"  # 设置scroll过期时间为1分钟
        )

        # 获取scroll_id，用于获取后续数据
        scroll_id = response["_scroll_id"]

        # 数据存储
        degree_salary_data = {}

        # 正则匹配 "25-45K" 或 "25-45K·14薪" 的数据
        valid_salary_pattern = re.compile(r"(\d+)-(\d+)K(?:·\d+薪)?")

        # 处理当前批次的结果
        while len(response["hits"]["hits"]) > 0:
            for hit in response["hits"]["hits"]:
                degree = hit["_source"]["job_degree"]  # 改为根据学历字段分类
                salary_desc = hit["_source"]["salary_desc"]

                # 匹配有效薪资
                match = valid_salary_pattern.match(salary_desc)
                if match:
                    # 解析最小和最大薪资
                    min_salary = int(match.group(1)) * 1000
                    max_salary = int(match.group(2)) * 1000

                    # 按学历分类存储数据
                    if degree not in degree_salary_data:
                        degree_salary_data[degree] = {
                            "max_salaries": [],
                            "min_salaries": [],
                        }

                    degree_salary_data[degree]["max_salaries"].append(max_salary)
                    degree_salary_data[degree]["min_salaries"].append(min_salary)

            # 使用scroll_id获取后续数据
            response = es.scroll(
                scroll_id=scroll_id,
                scroll="1m",  # 每次滚动间隔1分钟
            )
            scroll_id = response["_scroll_id"]

        # 聚合每种学历的最高和最低薪资
        categories = []
        max_salaries = []
        min_salaries = []

        for degree, salaries in degree_salary_data.items():
            categories.append(degree)
            max_salaries.append(max(salaries["max_salaries"]))
            min_salaries.append(min(salaries["min_salaries"]))

        # 清除scroll上下文，释放资源
        es.clear_scroll(scroll_id=scroll_id)
        
        # 输出 ECharts 配置
        echarts_option = {
            "title": {
                "text": "不同学历的薪资分布"  # 修改标题为“不同学历的薪资分布”
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "cross"
                }
            },
            "legend": {
                "data": ["最高薪水", "最低薪水"]
            },
            "grid": {
                "left": '3%',
                "right": '4%',
                "bottom": '3%',
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 30
                }
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {"name": "最高薪水", "type": "line", "data": max_salaries, "label": {
                    "show": True,
                    "position": "top",  
                    "formatter": "{c} 元" 
                }},  # 最高薪水
                {"name": "最低薪水", "type": "line", "data": min_salaries, "label": {
                    "show": True,
                    "position": "top",  
                    "formatter": "{c} 元"
                }},  # 最低薪水
            ],
        }
        return Result.success(echarts_option)
    except Exception as e:
        return Result.bad_request(str(e))

@boss.get("/analysis/salary_experience")
async def salary_by_experience():
    try:
        # 初次查询，设置 scroll 参数（例如1分钟），每次返回1000条数据
        response = es.search(
            index=BOSS_DATA,
            body={
                "size": 1000,  # 每次返回1000条数据
                "_source": ["job_experience", "salary_desc"],  # 只返回需要的字段
                "query": {
                    "regexp": {"salary_desc": ".*K.*"}  # 初步匹配包含 "K" 的薪资
                },
            },
            scroll="1m"  # 设置scroll过期时间为1分钟
        )

        # 获取scroll_id，用于获取后续数据
        scroll_id = response["_scroll_id"]

        # 数据存储
        experience_salary_data = {}

        # 正则匹配 "25-45K" 或 "25-45K·14薪" 的数据
        valid_salary_pattern = re.compile(r"(\d+)-(\d+)K(?:·\d+薪)?")

        # 处理当前批次的结果
        while len(response["hits"]["hits"]) > 0:
            for hit in response["hits"]["hits"]:
                job_experience = hit["_source"]["job_experience"]  # 根据 job_experience 字段分类
                salary_desc = hit["_source"]["salary_desc"]

                # 匹配有效薪资
                match = valid_salary_pattern.match(salary_desc)
                if match:
                    # 解析最小和最大薪资
                    min_salary = int(match.group(1)) * 1000
                    max_salary = int(match.group(2)) * 1000

                    # 按工作经验分类存储数据
                    if job_experience not in experience_salary_data:
                        experience_salary_data[job_experience] = {
                            "max_salaries": [],
                            "min_salaries": [],
                        }

                    experience_salary_data[job_experience]["max_salaries"].append(max_salary)
                    experience_salary_data[job_experience]["min_salaries"].append(min_salary)

            # 使用scroll_id获取后续数据
            response = es.scroll(
                scroll_id=scroll_id,
                scroll="1m",  # 每次滚动间隔1分钟
            )
            scroll_id = response["_scroll_id"]

        # 聚合每种经验水平的最高和最低薪资
        categories = []
        max_salaries = []
        min_salaries = []

        for job_experience, salaries in experience_salary_data.items():
            categories.append(job_experience)
            max_salaries.append(max(salaries["max_salaries"]))
            min_salaries.append(min(salaries["min_salaries"]))

        # 清除scroll上下文，释放资源
        es.clear_scroll(scroll_id=scroll_id)
        
        # 输出 ECharts 配置
        echarts_option = {
            "title": {
                "text": "不同工作经验水平的薪资分布"  # 修改标题为“不同工作经验水平的薪资分布”
            },
            "tooltip": {
                "trigger": "axis",
                "axisPointer": {
                    "type": "cross"
                }
            },
            "legend": {
                "data": ["最高薪水", "最低薪水"]
            },
            "grid": {
                "left": '3%',
                "right": '4%',
                "bottom": '3%',
                "containLabel": True
            },
            "xAxis": {
                "type": "category",
                "data": categories,
                "axisLabel": {
                    "interval": 0,
                    "rotate": 30
                }
            },
            "yAxis": {
                "type": "value"
            },
            "series": [
                {"name": "最高薪水", "type": "line", "data": max_salaries, "label": {
                    "show": True,
                    "position": "top",  
                    "formatter": "{c} 元" 
                }},  # 最高薪水
                {"name": "最低薪水", "type": "line", "data": min_salaries, "label": {
                    "show": True,
                    "position": "top",  
                    "formatter": "{c} 元"
                }},  # 最低薪水
            ],
        }
        return Result.success(echarts_option)
    except Exception as e:
        return Result.bad_request(str(e))