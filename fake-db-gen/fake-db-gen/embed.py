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