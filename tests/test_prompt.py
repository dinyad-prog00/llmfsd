import unittest

from llmfsd.prompt import PromptTemplate


class TestPromptTemplate(unittest.TestCase):
    def setUp(self):
        self.prompt_template = PromptTemplate(lang="french")

    def test_get_messages_with_descriptions(self):
        format = "json"
        query = "SELECT * FROM users limit 2;"
        descriptions = {"age": "Age of the user"}

        messages = self.prompt_template.get_messages(format, query, descriptions)

        expected_system_content = (
            self.prompt_template.system_prompt.format(
                format=format, lang=self.prompt_template.lang
            )
            + "\nDescriptions:\nage: Age of the user"
        )
        expected_user_content = self.prompt_template.user_prompt.format(
            format=format, query=query
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["content"], expected_system_content)
        self.assertEqual(messages[1]["content"], expected_user_content)

    def test_get_messages_without_descriptions(self):
        format = "csv"
        query = "SELECT name, email FROM users;"

        messages = self.prompt_template.get_messages(format, query, descriptions={})

        expected_system_content = self.prompt_template.system_prompt.format(
            format=format, lang=self.prompt_template.lang
        )

        expected_user_content = self.prompt_template.user_prompt.format(
            format=format, query=query
        )

        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["content"], expected_system_content)
        self.assertEqual(messages[1]["content"], expected_user_content)


if __name__ == "__main__":
    unittest.main()
