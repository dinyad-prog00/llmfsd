import csv
import io
import json
import os
from typing import Dict, List, Optional
import warnings
import aisuite as ai

from llmfsd.data_model import DataModel
from llmfsd.parser import OuputParser
from .prompt import PromptTemplate


class Faker:
    def __init__(self, model_id: str, data_models: Optional[List[DataModel]] = None):
        """
        Initialize the Faker class.

        :param model_id: The ID of the language model to use for data generation (aisuite format).
        :param data_models: A list of DataModel instances to define schemas for tables.
        """
        self.model_id = model_id
        self._client = ai.Client()
        self.data_models: Dict[str, DataModel] = {}

        # Convert list of DataModel to a dictionary for quick lookup
        if data_models:
            for model in data_models:
                self.data_models[model.name] = model

        self.prompt = PromptTemplate()
        self.parser = OuputParser()

    def json(self, query: str, output: Optional[str] = None) -> Optional[list[dict]]:
        """
        Generate fake data in JSON format.

        :param query: The SQL query.
        :param output: File path to save the output. If None, return the JSON object.
        :return: A JSON object (list of dictionaries) or None if saved to a file.
        """
        response = self.__create_completions("json", query)
        # Ensure the response is valid JSON
        try:
            data = json.loads(response)
            if not isinstance(data, list):
                raise ValueError("Expected a JSON list of dictionaries.")

            # Save to file if output is provided
            if output:
                self.__save_to_file(json.dumps(data, indent=4), "json", output)
                return None
            return data
        except json.JSONDecodeError:
            raise ValueError("Response is not valid JSON.")

    def csv(self, query: str, output: Optional[str] = None) -> Optional[str]:
        """
        Generate fake data in CSV format.

        :param query: The SQL query.
        :param output: File path to save the output. If None, return the CSV string.
        :return: A CSV string (text) or None if saved to a file.
        """
        response = self.__create_completions("csv", query)

        # Validate the response as a CSV string
        try:
            # Use StringIO to parse the response as CSV to ensure validity
            output_stream = io.StringIO(response)
            reader = csv.reader(output_stream)
            rows = list(reader)

            # Ensure there is at least a header row
            if len(rows) < 1:
                raise ValueError("Response is not a valid CSV format.")

            # Save to file if output is provided
            if output:
                self.__save_to_file(response, "csv", output)
                return None
            return response
        except Exception as e:
            raise e

    def __create_completions(self, format: str, query: str):
        """
        Generate a response from the LLM based on the query.

        :param format: The output format (JSON or CSV).
        :param query: The SQL query.
        """
        # Preprocess the query
        query, descriptions = self.__process_query(query)

        # Generate messages for the prompt
        messages = self.prompt.get_messages(format, query, descriptions)

        # Send request to the LLM
        response = self._client.chat.completions.create(
            model=self.model_id, messages=messages
        )

        # Parse and return the response
        return self.parser.parse(response)

    def __process_query(self, query: str) -> tuple[str, Dict[str, str]]:
        """
        Preprocess the SQL query to handle attribute extraction and descriptions.

        :param query: The SQL query.
        :return: The modified query and attribute descriptions.
        """
        # Extract table name from the query
        table_name = self.__extract_table_name(query)

        descriptions = {}
        # If the table exists in data_models
        if table_name in self.data_models:
            data_model = self.data_models[table_name]

            # Extract attribute descriptions
            descriptions = data_model.get_description()

            # Replace `*` with explicit attributes in the query
            if "*" in query.lower():
                attributes = ", ".join(data_model.get_attributes())
                query = query.replace("*", attributes)

        return query, descriptions

    def __extract_table_name(self, query: str) -> str:
        """
        Extract the table name from the SQL query.

        :param query: The SQL query.
        :return: The table name as a string.
        :raises ValueError: If the 'FROM' clause is missing in the query.
        """
        lower_query = query.lower()
        if "from" in lower_query:
            return lower_query.split("from")[1].split()[0].strip(";")
        raise ValueError("Invalid query: 'FROM' clause is missing.")

    def __save_to_file(self, data: str, format: str, path: str):
        """
        Save data directly to a file without validation.

        :param data: The data to save, assumed to be a correctly formatted string.
        :param format: Data's format
        :param path: The file path where the data will be saved. The extension (.json or .csv) determines the format.
        :raises ValueError: If the file format is unsupported.
        :raises OSError: If there is an error writing to the file.
        """
        # Determine the file extension
        ext = os.path.splitext(path)[-1].lower()

        if ext not in {".json", ".csv"}:
            raise ValueError("Unsupported file format. Use '.json' or '.csv'.")

        if ext != f".{format}":
            warnings.warn(
                f"You are using {ext} instead of {format}!", category=UserWarning
            )
        try:
            # Write the data directly to the file
            with open(path, "w", encoding="utf-8") as file:
                file.write(data)
        except FileNotFoundError:
            raise OSError(f"File path not found: {path}")
        except PermissionError:
            raise OSError(f"Permission denied for file path: {path}")
        except Exception as e:
            raise OSError(f"An unexpected error occurred while saving the file: {e}")
