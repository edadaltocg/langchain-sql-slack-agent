import torch
import torch.nn.functional as F
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

input_texts = [
    "what is the capital of China?",
    "how to implement quick sort in python?",
    "Beijing",
    "sorting algorithms",
]

queries = [
    "I want to conduct a churn prediction analysis on my customer data",
]

input_texts = [
    "What features best explain customer churn?",
    "campaignid,INT,Unique identifier for each marketing campaign",
    "name,VARCHAR(100),Name of the campaign",
    "startdate,DATE,Start date of the campaign",
    "enddate,DATE,End date of the campaign",
    "budget,DECIMAL(10,2),Budget allocated for the campaign",
    "channel,VARCHAR(50),Main channel used for the campaign (Email, Social Media, etc.)",
    "targetaudience,VARCHAR(100),Description of the target audience",
    "leadsgenerated,INT,Number of leads generated from the campaign",
    "salesgenerated,INT,Number of sales generated from the campaign",
    "roi,FLOAT,Return on investment for the campaign",
    "active,BOOLEAN,Whether the campaign is currently active",
    "objective,VARCHAR(200),Main objective of the campaign",
    "creativesused,VARCHAR(255),Path to any creative materials used",
    "feedbackreceived,TEXT,Feedback received from customers about the campaign",
    "conversionrate,FLOAT,Conversion rate achieved by the campaign",
    "customerid,INT,Unique identifier for each customer",
    "firstname,VARCHAR(50),Customer's first name",
    "lastname,VARCHAR(50),Customer's last name",
    "email,VARCHAR(100),Customer's email address",
    "phone,VARCHAR(20),Customer's contact phone number",
    "age,INT,Customer's age",
    "gender,VARCHAR(10),Customer's gender",
    "country,VARCHAR(50),Country where the customer resides",
    "city,VARCHAR(50),City where the customer resides",
    "signupdate,DATE,Date when the customer signed up",
    "lastpurchasedate,DATE,Date of the last purchase",
    "totalpurchases,INT,Total number of purchases made by the customer",
    "totalspend,DECIMAL(10,2),Total amount spent by the customer",
    "preferredcategory,VARCHAR(50),Most purchased category of products",
    "membershipstatus,VARCHAR(50),Status of any membership program (Active, Inactive)",
    "churnriskscore,FLOAT,Predicted churn risk score",
    "lastactivity,DATE,Date of last activity by the customer",
    "subscriptiontype,VARCHAR(50),Type of subscription if any",
    "leadscore,INT,Score indicating the quality of the lead",
    "marketingsegment,VARCHAR(50),Marketing segment classification",
    "notes,TEXT,Any additional notes about the customer",
]

device = torch.device("mps")
model_path = "Alibaba-NLP/gte-large-en-v1.5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
model.eval()
model.to(device)

# Tokenize the input texts
batch_dict = tokenizer(input_texts, max_length=8192, padding=True, truncation=True, return_tensors="pt")
batch_size = 8
embeddings = []
for i in tqdm(range(0, len(input_texts), batch_size)):
    inp = {k: v[i : i + batch_size].to(device) for k, v in batch_dict.items()}
    with torch.no_grad():
        out = model(**inp)
    embeddings.append(out.last_hidden_state[:, 0])
embeddings = torch.cat(embeddings, dim=0)


# (Optionally) normalize embeddings
embeddings = F.normalize(embeddings, p=2, dim=1)
scores = embeddings[:1] @ embeddings[1:].T  # query vs. candidates
top_p = 0.5
scores, indices = torch.sort(scores, descending=True, dim=1)
scores_filter = scores > top_p
scores = scores[scores_filter]
indices = indices[scores_filter]
print(scores, indices)
instances = [input_texts[i] for i in indices]
print("Top similar instances:", instances, scores)
