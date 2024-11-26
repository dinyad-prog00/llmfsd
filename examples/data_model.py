import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append("../llmfsd")

from llmfsd import Faker, DataModel

# Define data models

model1 = DataModel("artists", ["name", "age", "country"])
model2 = DataModel(
    "dogs", {"id": "Number in range(5,20)", "name": None, "breed": "Breed of the dog"}
)


faker = Faker(model_id="mistral:mistral-large-latest", data_models=[model1, model2])

print(faker.json("select * from dogs limit 3"))

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
