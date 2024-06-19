import json
import os
import time
import pickle
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from llama_index.core import PromptTemplate, Settings
from llama_index.llms.huggingface import HuggingFaceLLM

showMessage = True

LLM_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

# GPU acceleration with metal on Mac
device = torch.device("metal") if torch.cuda.is_available() else torch.device("cpu")


# Function to print the current time and a message
def log_time(message):
    if showMessage:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")


# Load the vector index
def load_index(directory_path):
    index_file_path = os.path.join(directory_path, "index.pkl")

    with open(index_file_path, "rb") as f:
        index = pickle.load(f)

    log_time(f"Index loaded from {index_file_path}")
    return index


# Load the model and tokenizer
def load_model(directory_path):
    model_save_path = os.path.join(directory_path, "llm_model")
    tokenizer_save_path = os.path.join(directory_path, "llm_tokenizer")

    model = AutoModelForCausalLM.from_pretrained(model_save_path)
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_save_path)

    log_time("Model and tokenizer loaded." + "██" * 10)
    return model, tokenizer


# Load the embedding model
def load_embedding_model(directory_path):
    embedding_model_path = os.path.join(directory_path, "embedding_model_cpu.pkl")

    with open(embedding_model_path, "rb") as f:
        embed_model = pickle.load(f)
        log_time("Embedding model loaded." + "██" * 10)
    return embed_model


# Load LLM configuration from JSON file
def load_config(directory_path):
    config_file_path = os.path.join(directory_path, "llm_config.json")

    with open(config_file_path, "r") as f:
        llm_config = json.load(f)
        log_time("LLM configuration loaded." + "██" * 20)
    return llm_config


# Import the saved model with HuggingFace
def initialize_llm(llm_config, model, tokenizer):
    llm = HuggingFaceLLM(
        context_window=llm_config["context_window"],
        max_new_tokens=llm_config["max_new_tokens"],
        generate_kwargs=llm_config["generate_kwargs"],
        system_prompt=llm_config["system_prompt"],
        query_wrapper_prompt=PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>"),
        model=model,
        tokenizer=tokenizer,
        # tokenizer_name=LLM_MODEL_NAME,
        # model_name=LLM_MODEL_NAME,
        # device_map="auto",

    )

    log_time("LLM initialized.")
    return llm


# congfigure the settings
def configure_settings(embed_model, llm):
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = 1024
    log_time("Settings configured.")


def generate_response(model, tokenizer, question):
    try:
        # # Tokenize the input text
        # inputs = tokenizer("This is sample text.", return_tensors="pt")

        # # Get model outputs with hidden states
        # outputs = model(**inputs, output_hidden_states=True)

        # # Extract the hidden states
        # hidden_states = outputs.hidden_states

        # # Typically, the last hidden state is used as the embedding
        # embeddings = hidden_states[-1]

        # print(embeddings)

        log_time(f"Using device: {device}")

        log_time("Tokenizing input...")
        inputs = tokenizer(question, return_tensors="pt").to(device)
        log_time("Input tokenized.")

        log_time("Generating response...")
        start_time = time.time()
        output = model.generate(**inputs, max_new_tokens=30, pad_token_id=tokenizer.eos_token_id)
        end_time = time.time()
        log_time(f"Response generated in {end_time - start_time:.2f} seconds.")

        log_time("Decoding response...")
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        log_time("Response decoded.")
        return response
    except Exception as e:
        log_time(f"Failed to generate response: {e}")
        return None


def initialize_all(directory):
    index = load_index(directory)
    model, tokenizer = load_model(directory)
    embed_model = load_embedding_model(directory)
    llm_config = load_config(directory)
    llm = initialize_llm(llm_config, model, tokenizer)
    configure_settings(embed_model, llm)
    return model, tokenizer


# Initialize the model, tokenizer, and settings when the module is imported
model_dir = "./models/"
model, tokenizer = initialize_all(model_dir)


# def main():
#     directory = "./models/"
#
#     index = load_index(directory)
#     model, tokenizer = load_model(directory)
#     embed_model = load_embedding_model(directory)
#     llm_config = load_config(directory)
#
#     llm = initialize_llm(llm_config, model, tokenizer)
#     configure_settings(embed_model, llm)
#
#     # Example question + response
#     question = "What is ECG (Electrocardiography)?"
#     response = generate_response(model, tokenizer, question)
#
#     print("*" * 30)
#     print("Question:", question)
#
#     if response:
#         print("Response:", response)
#     else:
#         print("Failed to generate response.")

# query_engine = index.as_query_engine(llm=Settings.llm, similarity_top_k=5)

# done = False
# while not done:
#   print("*"*30)
#   question = input("Enter your question: ")
#   response = query_engine.query(question)
#   print(response)
#   done = input("End the chat? (y/n): ") == "y"


""" RAG Query Engine (In Progress) """
# # Combine retrieval with generation
# class RAGQueryEngine:
#     def __init__(self, retrieval_engine, llm):
#         self.retrieval_engine = retrieval_engine
#         self.llm = llm

#     def query(self, question):
#         # Retrieve relevant documents
#         relevant_docs = self.retrieval_engine.query(question)
#         # Use retrieved documents as context for generation
#         context = "\n".join([doc.text for doc in relevant_docs])
#         prompt = f"{self.llm.system_prompt}\n\n{context}\n\n{self.llm.query_wrapper_prompt.format(query_str=question)}"
#         return self.llm.generate(prompt)


# # Initialize the RAG query engine
# retrieval_engine = index.as_query_engine(similarity_top_k=5)
# rag_query_engine = RAGQueryEngine(retrieval_engine, Settings.llm)

# print("RAG query engine set up.")

"""Using the RAGQueryEngine for querying"""

# done = False
# while not done:
#     print("*" * 30)
#     question = input("Enter your question: ")
#     response = rag_query_engine.query(question)
#     print(response)
#     done = input("End the chat? (y/n): ") == "y"
# """
