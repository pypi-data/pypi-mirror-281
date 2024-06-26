# Netra Adapters

`Netra Adapter` is a Python package designed to dynamically load and integrate Low-Rank Adaptation (LoRA) weights into transformer models, facilitating fine-tuned performance for various tasks.

## Features

- Load LoRA adapter weights from local files or directly from the Hugging Face Hub.
- Dynamically integrate and remove adapter weights based on query content.
- Generate responses using integrated LoRA weights.

## Installation

To install the `netra_adapter` package, clone this repository and install the dependencies:

```bash
pip install netra_adapter
```


## Example Usage

### Importing and Initializing

First, import the necessary modules and initialize the `LoRAAdapterManager` with the desired model:

```python
from netra_adapter import LoRAAdapterManager
import torch

# Determine the device to use (GPU or CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Instantiate the LoRAAdapterManager with a specified model
adapter_manager = LoRAAdapterManager(model_name='gpt2', device=device)

# Load LoRA weights from the Hugging Face Hub
adapter_manager.load_lora_weights(adapter_name='sales', filepath_or_repo='AdapterHub/gpt2_sales')
adapter_manager.load_lora_weights(adapter_name='support', filepath_or_repo='AdapterHub/gpt2_support')

# Function to generate a response based on query content
def generate_adaptive_response(query):
    adapter_name = None
    if 'sales' in query.lower():
        adapter_name = 'sales'
    elif 'support' in query.lower():
        adapter_name = 'support'
    else:
        return "Query does not match any adapter criteria."

    # Integrate the selected LoRA weights
    adapter_manager.integrate_lora_weights(adapter_name)
    
    # Generate the response with the integrated LoRA weights
    response = adapter_manager.generate_response(query)
    
    # Remove the integrated adapter hooks to reset the model
    adapter_manager.remove_adapter_hooks(adapter_name)
    
    return response
# Example queries
query_sales = "Can you provide me with the sales report for Q1?"
query_support = "I need help with my account, it doesn't login."

# Generate adaptive responses
response_sales = generate_adaptive_response(query_sales)
print("Sales query response:", response_sales)
print('#' * 100)
response_support = generate_adaptive_response(query_support)
print("Support query response:", response_support)

```