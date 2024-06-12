# import os, logging, sys
# import logging
# import psutil
# import torch
# from huggingface_hub import login
# from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, PromptTemplate, Settings
# from langchain_huggingface import HuggingFaceEmbeddings
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from llama_index.llms.huggingface import HuggingFaceLLM

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# os.environ["HF_KEY"] = "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"
# login(token=os.environ.get('HF_KEY'),add_to_git_credential=True)

# # Configure logging
# logging.basicConfig(filename='pdf_errors.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# # Specify the directory containing the papers
# papers_directory = "papers/"

# # Function to find all PDF files in a directory and its subdirectories
# def find_all_pdfs(directory):
#     pdf_files = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.pdf'):
#                 pdf_files.append(os.path.join(root, file))
#                 print(f"Found PDF file: {os.path.join(root, file)}")
#     return pdf_files

# # Get a list of all PDF files in the directory and its subdirectories
# pdf_files = find_all_pdfs(papers_directory)

# # Initialize the documents list
# documents = []

# # Function to check memory usage
# def check_memory_usage(threshold=80):
#     memory = psutil.virtual_memory()
#     return memory.percent < threshold


# # Batch size for processing PDF files
# batch_size = 10

# # Process PDF files in batches
# for i in range(0, len(pdf_files), batch_size):
#     if not check_memory_usage():
#         logging.warning("Memory usage is high, pausing processing.")
#         break
#     batch = pdf_files[i:i+batch_size]
#     for pdf_file in batch:
#         try:
#             reader = SimpleDirectoryReader(input_dir=os.path.dirname(pdf_file), required_exts=".pdf").load_data()
#             documents.extend(reader)
#         except Exception as e:
#             logging.warning(f"Failed to read {pdf_file}: {e}")

# # Print the first document
# if documents:
#     print("████████████████████████████████████████████████████████████████████████████████████████████████")
#     print(documents[0])
# else:
#     print("No documents found.")


# EMBEDDING_MODEL_NAME = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

# embed_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


# index = VectorStoreIndex.from_documents(documents, embed_model = embed_model)

# system_prompt = """<|SYSTEM|># You are an AI-enabled medical research assistant.
# Your goal is to answer questions accurately using only the context provided.
# """

# # This will wrap the default prompts that are internal to llama-index
# query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")

# LLM_MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

# # Initialize the tokenizer
# tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)

# # Check if CUDA is available and set device accordingly
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load the model with the appropriate device map
# model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, device_map=device)

# # Create the HuggingFaceLLM instance with the loaded model and tokenizer
# llm = HuggingFaceLLM(
#     context_window=4096,
#     max_new_tokens=512,
#     generate_kwargs={"temperature": 0.1, "do_sample": False},
#     system_prompt=system_prompt,
#     query_wrapper_prompt=query_wrapper_prompt,
#     model=model,
#     tokenizer=tokenizer,
#     # Uncomment and set torch_dtype if using CUDA to reduce memory usage
#     # model_kwargs={"torch_dtype": torch.float16}
# )

# # Print some information to confirm
# print("Model loaded successfully")

# Settings.embed_model = embed_model
# Settings.llm = llm
# Settings.chunk_size = 1024
# #Settings.chunk_overlap = 256

# query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)


# # Debugging: print the number of documents and embeddings
# # print(f"Number of documents: {len(documents)}")
# # print(f"Index embeddings: {len(index.docstore.index_to_docstore_id)}")


# # def set_css():
# #   display(HTML('''
# #   <style>
# #     pre {
# #         white-space: pre-wrap;
# #     }
# #   </style>
# #   '''))
# # get_ipython().events.register('pre_run_cell', set_css)


# done = False
# while not done:
#   print("*"*30)
#   question = input("Enter your question: ")
#   response = query_engine.query(question)
#   # Debugging: print the raw response
#   print(f"Raw Response: {response}")
#   print(response)
#   done = input("End the chat? (y/n): ") == "y"