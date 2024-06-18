# LLM Chatbot using fine-tuned LLaMA-2 model with PDF Data

This project utilizes HuggingFace's pretrained LLM `meta-llama/Llama-2-7b-chat-hf`, fine-tuned with PDF data, to generate accurate responses to queries. It also uses `sentence-transformers/multi-qa-MiniLM-L6-cos-v1` for vector embedding.

_llama_2_transformer_pdf.py_ will create and save the model locally. The code for the model was edited from this article: [ Build LLM Chatbot With PDF Documents](https://www.linkedin.com/pulse/build-llm-chatbot-pdf-documents-peng-wang-bq5fc/). I ran the model on Google Collab using L4 GPU. The Jupyter Notebook can be accessed here: [Google Collab Notebook](https://colab.research.google.com/drive/1ittu4zTPqlZF0MFNlG_86_z_DN2kyZ9G?usp=sharing).

_main.py_ loads the model, tokenizer, embedded model, and vector index to generate example response from the LLM chatbot.
