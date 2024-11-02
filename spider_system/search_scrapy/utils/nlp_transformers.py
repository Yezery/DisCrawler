from sentence_transformers import SentenceTransformer
from textblob import TextBlob

# 使用 Hugging Face 的模型，将句子转化为向量
def get_sentence_embedding(text,model_path="search_scrapy/models/all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_path)
    """
    使用预训练模型将文本转换为语义向量。
    """
    return model.encode(text)


def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity
   

