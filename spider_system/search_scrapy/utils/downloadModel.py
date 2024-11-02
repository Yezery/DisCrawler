from transformers import AutoModelForSequenceClassification, AutoTokenizer

# 设置模型和保存路径
model_name = ""
save_directory = ""

# 下载并保存模型和分词器
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
