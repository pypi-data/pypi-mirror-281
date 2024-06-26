import torch
import psutil

def load_lora_weights(filepath, device):
    try:
        return torch.load(filepath, map_location=device)
    except Exception as e:
        raise RuntimeError(f"Error loading LoRA weights from {filepath}: {e}")

def get_memory_usage(device):
    try:
        # Get CPU RAM usage
        cpu_memory = psutil.virtual_memory().used
        # Get GPU VRAM usage if CUDA
        if device == 'cuda':
            vram_memory = torch.cuda.memory_allocated()
        else:
            vram_memory = 0
        return cpu_memory, vram_memory
    except Exception as e:
        raise RuntimeError(f"Error getting memory usage: {e}")
