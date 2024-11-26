from typing import Dict


system_prompt = """
                 You are a SQL Fake Database. Given a SQL query, generate fake data as a {format}. 
                 Ensure the data matches the schema and respects the query conditions. 
                 Return the fake data only, do not use ```json or ```scsv or ```around data.
                """
user_prompt = """
                SQL Query: {query}
                Fake Data ({format} format):
               """


class PromptTemplate:
    def __init__(
        self, system_prompt: str = system_prompt, user_prompt: str = user_prompt
    ):
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
                self.system_prompt.format(format=format)
                + "\nDescriptions:\n"
                + description_text
            )
        else:
            full_system_prompt = self.system_prompt.format(format=format)

        return [
            {"role": "system", "content": full_system_prompt},
            {
                "role": "user",
                "content": self.user_prompt.format(format=format, query=query),
            },
        ]
