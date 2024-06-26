import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .utils import load_lora_weights
from huggingface_hub import hf_hub_download, list_repo_files
import os

class LoRAAdapterManager:
    def __init__(self, model_name, device='cuda'):
        self.model_name = model_name
        self.device = device
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        except Exception as e:
            raise RuntimeError(f"Error loading model or tokenizer: {e}")
        self.lora_weights = {}
        self.hooks = {}

    def load_lora_weights(self, adapter_name, filepath_or_repo):
        if os.path.isfile(filepath_or_repo):
            # If filepath_or_repo is a local file path
            filepath = filepath_or_repo
        else:
            # If filepath_or_repo is assumed to be a Hugging Face repo
            try:
                files = list_repo_files(filepath_or_repo)
                weight_files = [f for f in files if f.endswith(('.bin', '.pt'))]
                if not weight_files:
                    raise RuntimeError("No suitable weight files found in the repository.")
                filepath = hf_hub_download(repo_id=filepath_or_repo, filename=weight_files[0])
            except Exception as e:
                raise RuntimeError(f"Error downloading LoRA weights from Hugging Face hub")

        try:
            self.lora_weights[adapter_name] = load_lora_weights(filepath, self.device)
        except Exception as e:
            raise RuntimeError(f"Error loading LoRA weights from {filepath}")


    def integrate_lora_weights(self, adapter_name):
        if adapter_name not in self.lora_weights:
            raise ValueError(f"Adapter {adapter_name} not found. Please load the adapter weights first.")
        try:
            hooks = []
            for name, param in self.model.named_parameters():
                if name in self.lora_weights[adapter_name]:
                    def hook_fn(grad, lw=self.lora_weights[adapter_name][name], param_name=name):
                        print(f"Applying LoRA weights to parameter: {param_name}")
                        return grad + lw.data

                    hook = param.register_hook(hook_fn)
                    hooks.append(hook)
            self.hooks[adapter_name] = hooks
            print(f'Setup: {adapter_name} LoRA adapter')
        except Exception as e:
            raise RuntimeError(f"Error integrating LoRA weights for {adapter_name}")



    def remove_adapter_hooks(self, adapter_name):
        if adapter_name in self.hooks:
            try:
                for hook in self.hooks[adapter_name]:
                    hook.remove()
                del self.hooks[adapter_name]
                print(f'Unplugged: {adapter_name} LoRA adapter')
            except Exception as e:
                raise RuntimeError(f"Error removing hooks for {adapter_name}: {e}")
        else:
            raise ValueError(f"Adapter {adapter_name} not found in hooks.")

    def remove_all_hooks(self):
        try:
            for adapter_name, hooks in self.hooks.items():
                for hook in hooks:
                    hook.remove()
            self.hooks = {}
            print('Unplugged: All LoRA adapters')
        except Exception as e:
            raise RuntimeError(f"Error removing all hooks: {e}")

    def generate_response(self, query, max_length=50):
        try:
            inputs = self.tokenizer(query, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=max_length)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            raise RuntimeError(f"Error generating response: {e}")
