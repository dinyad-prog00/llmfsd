from typing import Dict


system_prompt = """
                You are a SQL Fake Database. Given a SQL query, your task is to generate fake data in {format} format. 
                Ensure the generated data adheres to the schema and satisfies all query conditions.
                For attributes containing text such as descriptions, ensure their content is in {lang}.
                Return the fake data only, without wrapping it in any code fences or additional formatting. Include a header if the format is CSV.
                """
user_prompt = """
                SQL Query: {query}
                Fake Data ({format} format):
               """


class PromptTemplate:
    def __init__(
        self, lang, system_prompt: str = system_prompt, user_prompt: str = user_prompt
    ):
        self.lang = lang
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def get_messages(
        self, format: str, query: str, descriptions: Dict[str, str]
    ) -> list[dict[str, str]]:
        """
        Generate a list of messages for the LLM prompt.
        :param format: The output format (JSON or CSV).
        :param query: The SQL query.
        :param descriptions: Attribute descriptions for the data model.
        """
        # Add descriptions only if they exist
        if descriptions:
            description_text = "\n".join(
                [f"{key}: {desc}" for key, desc in descriptions.items()]
            )
            full_system_prompt = (
                self.system_prompt.format(format=format, lang=self.lang)
                + "\nDescriptions:\n"
                + description_text
            )
        else:
            full_system_prompt = self.system_prompt.format(
                format=format, lang=self.lang
            )

        return [
            {"role": "system", "content": full_system_prompt},
            {
                "role": "user",
                "content": self.user_prompt.format(format=format, query=query),
            },
        ]
