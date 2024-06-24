# LLM Chatbot from LLaMA-2 model fine-tuned with PDF data

This project utilizes HuggingFace's pretrained LLM `meta-llama/Llama-2-7b-chat-hf`, fine-tuned with PDF data, to generate accurate responses to queries.

_save_model.py_ will create and save the model locally. The code for the model was edited from this article: [ Build LLM Chatbot With PDF Documents](https://www.linkedin.com/pulse/build-llm-chatbot-pdf-documents-peng-wang-bq5fc/). I ran the model on Google Collab using L4 GPU. The Jupyter Notebook can be accessed here: [Google Collab Notebook](https://colab.research.google.com/drive/1ittu4zTPqlZF0MFNlG_86_z_DN2kyZ9G?usp=sharing).

_run_model.py_ loads the model, tokenizer, embedded model, and vector index to generate example response from the LLM chatbot. Then it takes the given question and sends the model's response to the user.

You will need to create a _.env_ file with your own HuggingFace Access Token to run the project.

## Loading the model

The original article would run the vector embedding and model creation everytime the notebook was run. I changed their project to be able to save the model locally, so you could load the model later and directly run the queries.

A more detailed explanation can be found here: [models/README.md](models/README.md)

## Saving the model

Running _save_model.py_ will save the model locally. I'll briefly go over how this works:

#### Prepare PDF documents

- Using `pypdf`, all .pdf documents in the _papers/_ folder is read and loaded into memory.

#### Vector Embedding

- Authenticates and sets up the environment for using Hugging Face models (Hugging Face Login).
- The `sentence-transformers/multi-qa-MiniLM-L6-cos-v1` embedding model using a HuggingFaceEmbeddings wrapper from the `langchain` library is used to save a vector embedding model.

#### Vector Store Index

- Creates a Vector Store Index (Index that stores numerical representations of the data that capture their semantic meaning) from the given pdf documents and vector embedding model

#### LLM Setup

- Initializes a HuggingFaceLLM from `meta-llama/Llama-2-7b-chat-hf`.
- The `system_prompt`, `query_wrapper_prompt`, `context_window`, and other important fields are set.
- Configures global settings (Settings) for the embedding model, LLM, and chunk size to optimize performance during query operations.

#### Saving Model Components

- The function save_model_components() will save all important files of the LLM to models/
  - Vector index (_index.pkl_)
  - Embedding model (_embedding_model.pkl_ if using CUDA, otherwise _embedding_model_cpu.pkl_)
  - LLM model and tokenizer (_llm_model/_ and _llm_tokenizer/_)
  - LLM configuration (_llm_config.json_)

## Chatbot web-application (In progress)

I used Django and React to create a simple web application as the interface for the chatbot. Users would be able to type their question in the textbox and receive a response from the model, shown when they click send.

#### Run Django Server

I added a script in _manage.py_ to automatically build the React frontend with Vite before starting the Django server, so you don't need to run `npm run build` everytime.

```
python manage.py runserver
```

## Model Evaluation

I tested the LLM's responses to some sample questions relevant to the pdf papers used in fine-tuning.

I ran the model on both my Macbook Air and Google Collab. Running it on my computer takes significantly longer than running it on Google Collab.

The detailed report of the runtimes and responses from the LLM can be found here: [papers/README.md](papers/README.md)

## Dependencies

`langchain`, `llama-index`, `transformers`, `torch`, `pypdf`, `python-dotenv`, `einops`, `accelerate`, `bitsandbytes`, `sentence_transformers`, `sentencepiece`, `Django`

#### Install dependencies

```
install --no-cache-dir -r requirements.txt
```
