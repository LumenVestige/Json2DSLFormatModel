from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model_name = "databricks/dolly-v2-3b"  # Example model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define a prompt for structured data generation
prompt = "Generate a JSON object with the following structure: {'name': 'string', 'age': 'integer', 'city': 'string'}"

# Tokenize and generate text
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(inputs['input_ids'], max_length=100)

# Decode and print the generated text
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)