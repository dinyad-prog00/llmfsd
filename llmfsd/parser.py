class OuputParser:
    def parse(self, response):
        return response.choices[0].message.content
