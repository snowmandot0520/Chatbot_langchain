import os, logging, sys, psutil
import joblib
import pickle
import json
from huggingface_hub import login
from llama_index.core import SimpleDirectoryReader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.core import VectorStoreIndex, PromptTemplate, Settings
import torch
from llama_index.llms.huggingface import HuggingFaceLLM
from IPython.display import HTML, display
from dotenv import load_dotenv
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

"""Hugging Face Login"""
# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
hf_key = os.getenv("HF_KEY")
if hf_key is None:
    raise ValueError("HF_KEY is not set in the environment.")
os.environ["HF_KEY"] = hf_key

login(token=os.environ.get('HF_KEY'),add_to_git_credential=True)

# Specify the directory containing the papers
papers_directory = "papers/"

# Function to find all PDF files in a directory and its subdirectories
def find_all_pdfs(directory):
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
                # print(f"Found PDF file: {os.path.join(root, file)}")
    return pdf_files

# Get a list of all PDF files in the directory and its subdirectories
pdf_files = find_all_pdfs(papers_directory)

# Initialize the documents list
documents = []

# Function to check memory usage
def check_memory_usage(threshold=80):
    memory = psutil.virtual_memory()
    return memory.percent < threshold

# Batch size for processing PDF files
batch_size = 10

# Process PDF files in batches
for i in range(0, len(pdf_files), batch_size):
    if not check_memory_usage():
        logging.warning("Memory usage is high, pausing processing.")
        break
    batch = pdf_files[i:i+batch_size]
    for pdf_file in batch:
        try:
            reader = SimpleDirectoryReader(input_dir=os.path.dirname(pdf_file), required_exts=".pdf").load_data()
            documents.extend(reader)
        except Exception as e:
            logging.warning(f"Failed to read {pdf_file}: {e}")

# Print the first document
if documents:
    print("█"*30)
    print(documents[0])
else:
    print("No documents found.")

"""**Vector Embedding**

[Local Embeddings with HuggingFace](https://docs.llamaindex.ai/en/stable/examples/embeddings/huggingface/)

HuggingFaceEmbeddings is a class in the LangChain library that provides a wrapper around Hugging Face's sentence transformer models for generating text embeddings. It allows you to use any sentence embedding model available on Hugging Face for tasks like semantic search, document clustering, and question answering.

Tried 3 HF sentence transformer models `multi-qa-MiniLM-L6-cos-v1,all-MiniLM-L6-v2, all-mpnet-base-v2`. `all-MiniLM-L6-v2` and `all-mpnet-base-v2` did not perform well and answers often have hallucination i.e. non factual incorrect answers. `multi-qa-MiniLM-L6-cos-v1` is more suitable for Q&A conversation.
"""

EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

"""Initialize the Vector Store Index

Vector Store is a type of index that stores data as vector embeddings. These vector embeddings are numerical representations of the data that capture their semantic meaning. This allows for efficient similarity searches, where the most similar items to a given query are retrieved.
"""

index = VectorStoreIndex.from_documents(documents, embed_model = embed_model)

"""Set up prompts"""

system_prompt = """<|SYSTEM|># You are an AI-enabled medical research assistant.
Your goal is to answer questions accurately using only the context provided.
"""

# This will wrap the default prompts that are internal to llama-index
query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")

LLM_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

# To import models from HuggingFace directly
llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=512,
    generate_kwargs={"temperature": 0.1, "do_sample": False},
    system_prompt=system_prompt,
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=LLM_MODEL_NAME,
    model_name=LLM_MODEL_NAME,
    device_map="auto",
    # uncomment this if using CUDA to reduce memory usage
    model_kwargs={"torch_dtype": torch.float16 , "load_in_8bit":True}
)

"""[Migrating from ServiceContext to Settings](https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/service_context_migration/)

Introduced in LlamaIndex v0.10.0, there is a new global Settings object intended to replace the old ServiceContext configuration.

The new Settings object is a global settings, with parameters that are lazily instantiated. Attributes like the LLM or embedding model are only loaded when they are actually required by an underlying module.
"""

Settings.embed_model = embed_model
Settings.llm = llm
Settings.chunk_size = 1024
#Settings.chunk_overlap = 256

"""
Initialize the Query Engine
"""

query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)

"""Format the output with line wrapping enabled"""

def set_css():
  display(HTML('''
  <style>
    pre {
        white-space: pre-wrap;
    }
  </style>
  '''))
get_ipython().events.register('pre_run_cell', set_css)

"""Generate contextual results using retrieval-augmented prompt"""

done = False
while not done:
  print("*"*30)
  question = input("Enter your question: ")
  response = query_engine.query(question)
  print(response)
  done = input("End the chat? (y/n): ") == "y"


# Function to save components
def save_model_components(index, embed_model, llm, path):
    os.makedirs(path, exist_ok=True)

    # Save the vector index
    index_save_path = str(path + "/vector_index")
    os.makedirs(index_save_path, exist_ok=True)
    index_file_path = os.path.join(index_save_path, "index.pkl")
    with open(index_file_path, "wb") as f:
        pickle.dump(index, f)

    # Save the embedding model
    embed_model_path = os.path.join(path, 'embedding_model.pkl')
    joblib.dump(embed_model, embed_model_path)

    # Save LLM model
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, max_memory=4.0)
    model.save_pretrained(os.path.join(path, 'llm_model'))

    # Save the LLM tokenizer
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME, 
        max_memory=4.0)
    tokenizer.save_pretrained(os.path.join(path, 'llm_tokenizer'))

    # Save the LLM configuration
    llm_config_path = os.path.join(path, "llm_config.json")
    llm_config = {
        "context_window": llm.context_window,
        "max_new_tokens": llm.max_new_tokens,
        "generate_kwargs": llm.generate_kwargs,
        "system_prompt": llm.system_prompt,
        "query_wrapper_prompt": str(llm.query_wrapper_prompt),
        "tokenizer_name": llm.tokenizer_name,
        "model_name": llm.model_name,
        "device_map": llm.device_map,
        "model_kwargs": llm.model_kwargs,
    }
    with open(llm_config_path, "w") as f:
        json.dump(llm_config, f)

# Save the model components
save_path = "llama_3_model"
save_model_components(index, embed_model, llm, save_path)
