# Model Info / Folder structure

I saved my own model so I don't have to generate the vector index, embeddings, and model generation code everytime.

I can just load it locally, then run my queries on the saved model.

### Folder Structure

```
models/
│
├── llm_model/
│ ├── config.json
│ ├── model.safetensors.index.json
│ ├── generation_config.json
│ ├── model-00001-of-00006.safetensors
│ ├── model-00002-of-00006.safetensors
│ ├── model-00003-of-00006.safetensors
│ ├── model-00004-of-00006.safetensors
│ ├── model-00005-of-00006.safetensors
│ └── model-00006-of-00006.safetensors
│
├── llm_tokenizer/
│ ├── tokenizer.model
│ ├── special_tokens_map.json
│ └── tokenizer_config.json
│
├── index.pkl
├── embedding_model_cpu.pkl
└── llm_config.json
```

### Explanation of the Folder Structure:

- **index.pkl**: A pickle file containing the vector index.
- **llm_model/**: This folder contains the pre-trained language model files.
  - **config.json**: Configuration file for the language model, detailing the architecture and hyperparameters.
  - **model.safetensors.index.json**: Index file for the model shards, providing metadata for the individual safetensor files.
  - **generation_config.json**: Configuration file for generation-specific settings, such as temperature, max length, etc.
  - **model-00001-of-00006.safetensors** to **model-00006-of-00006.safetensors**: These files contain the sharded model weights stored in the safetensors format for efficient loading and processing.
- **llm_tokenizer/**: This folder contains the files related to the tokenizer.
  - **tokenizer.model**: The tokenizer model file
  - **special_tokens_map.json**: Mapping file for special tokens like `<PAD>`, `<CLS>`, etc.
  - **tokenizer_config.json**: Configuration file for the tokenizer, detailing its setup and parameters.
- **embedding_model_cpu.pkl**: Pickle file containing the embedding model used for generating embeddings from text inputs.
- **llm_config.json**: A JSON file containing configuration settings for the language model, including the `context_window`, `max_new_tokens`, `generate_kwargs`, `system_prompt`, `query_wrapper_prompt`, `tokenizer_name`, `model_name`, `device_map`, and `model_kwargs`.
