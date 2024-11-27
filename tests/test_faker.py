import unittest
from unittest.mock import patch, MagicMock
from llmfsd.data_model import DataModel
from llmfsd.faker import Faker


class TestFaker(unittest.TestCase):

    def setUp(self):
        self.model1 = DataModel("dogs", ["name", "breed", "age"])
        self.model2 = DataModel("colors", {"id": None, "name": "Color name"})
        self.faker = Faker("id")

    def test_process_query_with_data_model(self):
        faker = Faker("id", data_models=[self.model1, self.model2])

        query1 = "select * from dogs;"
        query2 = "select name from colors;"
        q1, descs1 = faker._process_query(query1)
        q2, descs2 = faker._process_query(query2)

        self.assertEqual(q1, "select name, breed, age from dogs;")
        self.assertEqual(descs1, {})
        self.assertEqual(q2, query2)
        self.assertEqual(descs2, {"name": "Color name"})

    def test_process_query_without_data_model(self):
        faker = Faker("id")
        query1 = "select * from bags;"
        q1, descs1 = faker._process_query(query1)

        self.assertEqual(q1, query1)
        self.assertEqual(descs1, {})

    @patch("aisuite.Client")
    def test_json_generation(self, MockClient):
        # Mock the client response
        mock_client_instance = MockClient.return_value
        mock_client_instance.chat.completions.create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content='[{"name": "Buddy", "breed": "Labrador", "age": 3}]'
                    )
                )
            ]
        )
        self.faker._client = MockClient() 
        
        result = self.faker.json("SELECT * FROM dogs LIMIT 1")
        expected = [{"name": "Buddy", "breed": "Labrador", "age": 3}]
        self.assertEqual(result, expected)

    @patch("aisuite.Client")
    def test_csv_generation(self, MockClient):
        # Mock the client response
        mock_client_instance = MockClient.return_value
        mock_client_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="id,name\n1,red\n2,blue"))]
        )
        
        self.faker._client = MockClient()    
    
        result = self.faker.csv("SELECT id, name FROM colors LIMIT 2")
        expected = "id,name\n1,red\n2,blue"
        self.assertEqual(result, expected)
        
        
    @patch("aisuite.Client")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_json_to_file(self, mock_open, MockClient):
        # Mock the client response
        mock_client_instance = MockClient.return_value
        mock_client_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='[{"name": "Buddy"}]'))]
        )
        
        self.faker._client = MockClient()  

        self.faker.json("SELECT * FROM dogs LIMIT 1", output="output.json")

        # Check that the file was written correctly
        mock_open.assert_called_with("output.json", "w", encoding="utf-8")
        mock_open().write.assert_called_once_with('[\n    {\n        "name": "Buddy"\n    }\n]')


    @patch("aisuite.Client")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_csv_to_file(self, mock_open, MockClient):
        # Mock the client response
        mock_client_instance = MockClient.return_value
        mock_client_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="id,name\n1,red"))]
        )
        
        self.faker._client = MockClient()  

        self.faker.csv("SELECT id, name FROM colors LIMIT 1", output="output.csv")

        # Check that the file was written correctly
        mock_open.assert_called_with("output.csv", "w", encoding="utf-8")
        mock_open().write.assert_called_once_with("id,name\n1,red")

if __name__ == "__main__":
    unittest.main()
