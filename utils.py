from safetensors import safe_open

model_save_path = "./models/llm_model"


def verify_model():
    # List all safetensor files
    shard_files = [
        "model-00001-of-00006.safetensors",
        "model-00002-of-00006.safetensors",
        "model-00003-of-00006.safetensors",
        "model-00004-of-00006.safetensors",
        "model-00005-of-00006.safetensors",
        "model-00006-of-00006.safetensors",
    ]

    # Try loading each shard separately
    for shard in shard_files:
        shard_path = f"{model_save_path}/{shard}"
        try:
            # Attempt to load the shard
            with safe_open(shard_path, framework="pt") as f:
                print(f"{shard} loaded successfully.")
        except Exception as e:
            print(f"Failed to load {shard}: {e}")
