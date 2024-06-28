from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.legacy.embeddings.langchain import LangchainEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import ServiceContext

LLM_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"
EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


