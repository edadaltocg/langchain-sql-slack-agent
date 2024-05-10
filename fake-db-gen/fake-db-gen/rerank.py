import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "BAAI/bge-large-en-v1.5"
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-reranker-large")
model = AutoModelForSequenceClassification.from_pretrained("BAAI/bge-reranker-large")
model.eval()

pairs = [
    [
        "what is panda?",
        "hi",
    ],
    [
        "what is panda?",
        "The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.",
    ],
]

query = [
    "What features best explain customer churn?",
]
instances = [
    "membershipstatus,VARCHAR(50),Status of any membership program (Active, Inactive)",
    "creativesused,VARCHAR(255),Path to any creative materials used",
    "churnriskscore,FLOAT,Predicted churn risk score",
    "marketingsegment,VARCHAR(50),Marketing segment classification",
]
pairs = [[query[0], i] for i in instances]
print(pairs)
inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors="pt", max_length=512)
with torch.no_grad():
    logits = model(**inputs).logits.reshape(1, -1)
print(logits)
scores = torch.nn.functional.softmax(logits, dim=1)
print(scores)
