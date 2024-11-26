import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append("../llmfsd")

from llmfsd import Faker

faker = Faker(model_id="mistral:mistral-large-latest")


print(faker.json("select uuid, name from phone_brands limit 4"))

"""
 output:
 
 [{'uuid': 'f47ac10b-58cc-4372-a567-0e02b2c3d479', 'name': 'Nokia'}, {'uuid': 'f7bac13b-58cc-4372-a567-0e02b2c3d479', 'name': 'Samsung'}, {'uuid': 'f98ac12b-58cc-4372-a567-0e02b2c3d479', 'name': 'Apple'}, {'uuid': 'f47ac10b-58cc-4972-a567-0e02b2c3d479', 'name': 'Sony'}]
"""


print(faker.csv("select id, color from colors limit 2"))

"""
output:

id,color
1,red
2,blue

"""