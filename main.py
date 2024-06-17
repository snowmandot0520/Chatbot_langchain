import json
import os
import pickle
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from llama_index.core import VectorStoreIndex, PromptTemplate, Settings
from llama_index.llms.huggingface import HuggingFaceLLM
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

# Load the vector index
directory_path = "./models/"
index_file_path = os.path.join(directory_path, "index.pkl")

with open(index_file_path, "rb") as f:
    index = pickle.load(f)

print(f"Index loaded from {index_file_path}")

# Load the model and tokenizer
LLM_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
model_save_path = os.path.join(directory_path, "llm_model")
tokenizer_save_path = os.path.join(directory_path, "llm_tokenizer")

model = AutoModelForCausalLM.from_pretrained(model_save_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_save_path)

print("Model and tokenizer loaded.")

# Load the embedding model
embedding_model_path = os.path.join(directory_path, "embedding_model_cpu.pkl")

with open(embedding_model_path, "rb") as f:
    embed_model = pickle.load(f)

print("Embedding model loaded.")

# Load LLM configuration from JSON file
config_file_path = os.path.join(directory_path, "llm_config.json")

with open(config_file_path, "r") as f:
    llm_config = json.load(f)

# Configure the Settings object
Settings.embed_model = embed_model
Settings.llm = HuggingFaceLLM(
    model=model,
    tokenizer=tokenizer,
    context_window=llm_config["context_window"],
    max_new_tokens=llm_config["max_new_tokens"],
    generate_kwargs=llm_config["generate_kwargs"],
    system_prompt=llm_config["system_prompt"],
    query_wrapper_prompt=PromptTemplate(template=llm_config["query_wrapper_prompt"]["template"]),
)
Settings.chunk_size = 1024

print("Settings configured.")

# Combine retrieval with generation
class RAGQueryEngine:
    def __init__(self, retrieval_engine, llm):
        self.retrieval_engine = retrieval_engine
        self.llm = llm

    def query(self, question):
        # Retrieve relevant documents
        relevant_docs = self.retrieval_engine.query(question)
        # Use retrieved documents as context for generation
        context = "\n".join([doc.text for doc in relevant_docs])
        prompt = f"{self.llm.system_prompt}\n\n{context}\n\n{self.llm.query_wrapper_prompt.format(query_str=question)}"
        return self.llm.generate(prompt)


# Initialize the RAG query engine
retrieval_engine = index.as_query_engine(similarity_top_k=5)
rag_query_engine = RAGQueryEngine(retrieval_engine, Settings.llm)

print("RAG query engine set up.")

# Using the RAGQueryEngine for querying
done = False
while not done:
    print("*" * 30)
    question = input("Enter your question: ")
    response = rag_query_engine.query(question)
    print(response)
    done = input("End the chat? (y/n): ") == "y"

# from safetensors import safe_open

# model_save_path = "./models/llm_model"

# # List all safetensor files
# shard_files = [
#     "model-00001-of-00006.safetensors",
#     "model-00002-of-00006.safetensors",
#     "model-00003-of-00006.safetensors",
#     "model-00004-of-00006.safetensors",
#     "model-00005-of-00006.safetensors",
#     "model-00006-of-00006.safetensors",
# ]

# # Try loading each shard separately
# for shard in shard_files:
#     shard_path = f"{model_save_path}/{shard}"
#     try:
#         # Attempt to load the shard
#         with safe_open(shard_path, framework="pt") as f:
#             print(f"{shard} loaded successfully.")
#     except Exception as e:
#         print(f"Failed to load {shard}: {e}")
