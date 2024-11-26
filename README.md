# llmfsd: LLM Fake Structured Data

**llmfsd** is a Python package designed to generate fake structured data using any Large Language Model (LLM). With this package, you can execute SQL-like queries to simulate structured data in formats like JSON or CSV. The tool is highly customizable and supports the integration of multiple AI providers (thanks aisuite).

## Features
- Generate fake structured data via SQL queries.
- Supports JSON and CSV output formats.
- Define custom data models to control schema and descriptions.
- Integrates with various AI providers (e.g., OpenAI, Mistral, Google, Anthropic).




## Installation

Install **llmfsd** using pip:

```bash
pip install llmfsd
```

### Install a Provider’s Package Along with aisuite

llmfsd supports all AI providers supported by aisuite. If you have not already installed the provider’s package, you can do so along with llmfsd. For example:

```bash
pip install "llmfsd[mistral]"
```
Alternatively, you can install the provider’s package directly with aisuite:

```bash
pip install "aisuite[mistral]"
```
For more details, visit the [aisuite repository](https://github.com/andrewyng/aisuite).

## Usage

### Basic Example

Here’s a simple example to get started:

```python
from llmfsd import Faker

# Initialize Faker with your LLM model_id (aisuite id format)
faker = Faker(model_id="mistral:mistral-large-latest")

# Generate JSON data
print(faker.json("SELECT uuid, name FROM phone_brands LIMIT 4"))

"""
Output:
[
 {'uuid': 'f47ac10b-58cc-4372-a567-0e02b2c3d479', 'name': 'Nokia'},
 {'uuid': 'f7bac13b-58cc-4372-a567-0e02b2c3d479', 'name': 'Samsung'}, 
 {'uuid': 'f98ac12b-58cc-4372-a567-0e02b2c3d479', 'name': 'Apple'},
 {'uuid': 'f47ac10b-58cc-4972-a567-0e02b2c3d479', 'name': 'Sony'}
]
"""

# Generate CSV data
print(faker.csv("SELECT id, color FROM colors LIMIT 2"))

"""
Output:
id,color
1,red
2,blue
"""
```

### More Advanced Example with Data Models

You can define custom data models to control the structure of your fake data.

```python
from llmfsd import Faker, DataModel

# Define data models

model = DataModel("dogs", 
    {"id": "Number in range(5,20)", "name": None, "breed": "Breed of the dog"}
)

# Initialize Faker with data models
faker = Faker(model_id="mistral:mistral-large-latest", data_models=[model])

# Generate JSON data for a specific model
print(faker.json("SELECT * FROM dogs LIMIT 3"))

"""
Output:
[
  {
    "id": 7,
    "name": "Buddy",
    "breed": "Labrador"
  },
  {
    "id": 12,
    "name": "Charlie",
    "breed": "Golden Retriever"
  },
  {
    "id": 15,
    "name": "Max",
    "breed": "German Shepherd"
  }
]
"""
```

## AI Providers

To initialize with different providers, set the model_id parameter during Faker initialization using **aisuite** format.

### Examples
```python
faker1 = Faker(model_id="groq:llama-3.2-3b-preview")

faker2 = Faker(model_id="openai:gpt-3.5-turbo")

faker3 = Faker(model_id="huggingface:mistralai/Mistral-7B-Instruct-v0.3")

```


Each provider requires proper API_KEY. Use environment variables or configuration files to store your API keys securely. For example you need mistral you need **MISTRAL_API_KEY**

```bash
export MISTRAL_API_KEY="your-mistral-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## Methods

### json(query: str, output: Optional[str] = None) -> list[dict] | None

Generate fake structured data in JSON format.
- query: The SQL query to execute.
- output: File path to save the JSON output. If None, returns the data directly.

### csv(query: str, output: Optional[str] = None) -> str | None

Generate fake structured data in CSV format.
- query: The SQL query to execute.
- output: File path to save the CSV output. If None, returns the data directly.


## Custom Data Models

You can create custom schemas using **DataModel**, defining either a list of attributes or a dictionary with descriptions. 

**DataModel** allows you to use * as a wildcard in queries or provide minimal descriptions for your attributes to the LLM. 

Avoid providing unnecessary descriptions, as they can increase token consumption. It is recommended to use a list of attributes if the attributes are self-explanatory for the LLM. When using a dictionary-based schema, you can leave None for some attributes and provide descriptions only for those you wish to clarify.


## Example:
```python
from llmfsd import DataModel
```

### Schema as a list
```python
model1 = DataModel("cars", ["brand", "model", "year"])
```

### Schema as a dictionary
```python
model2 = DataModel("pets", {
    "id" : "uuid string",
    "name": None,
    "age":  None,
    "species": "Type of pet (e.g., dog, cat)"
})
```

Pass these models to Faker during initialization:

```python
faker = Faker(model_id="openai:gpt-4o", data_models=[model1, model2])
```

## Saving Output to a File

Both json and csv methods support saving results directly to a file.

### Save JSON data to a file
```python
faker.json("SELECT * FROM artists LIMIT 20", output="artists.json")
```

### Save CSV data to a file
```python
faker.csv("SELECT name, age FROM pets LIMIT 20", output="pets.csv")
```

## Github
https://github.com/dinyad-prog00/llmfsd
