from datetime import datetime
import re

# from newspaper import Article


def convert_to_number(text):
    # 移除非数字和单位的前缀（如"点赞数"、"阅读量"等）
    text = re.sub(r"[^\d\.wWkK]+", "", text)
    # 检查处理后的 text 是否为空
    if not text:  # 如果是空字符串
        return 0

    # 根据单位进行转换
    if "w" in text.lower():  # 万的情况
        number = float(text.lower().replace("w", "")) * 10000
    elif "k" in text.lower():  # 千的情况
        number = float(text.lower().replace("k", "")) * 1000
    else:  # 没有单位
        number = float(text)

    return int(number)


def convert_to_timestamp(text):
    # 提取日期时间部分，例如 "2024-10-21 13:17:08"
    date_str = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)

    if date_str:
        # 将提取到的日期字符串转换为 datetime 对象
        date_time = datetime.strptime(date_str.group(), "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳
        timestamp = int(date_time.timestamp())
        return timestamp
    else:
        return None  # 如果找不到日期格式，返回 None


# def extract_content_from_url(url):
#     article = Article(url)
#     article.download()
#     article.parse()
#     return article.text

