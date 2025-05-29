class Prompt:
    """
    This class is used to generate a prompt for the Bedrock LLm endpoint.
    """
    def __init__(self, text: str):
        self.text = text

    def get_prompt(self) -> str:
        prompt = f""" 
                Please provide a brief sumary of the following text: {self.text}, keeping in mind the following instructions:

                INSTRUCTIONS:
                1. Focus only on the main content.
                
                2. IGNORE irrelevant elements such as:
                    - Cookie preferences and privacy notices
                    - Navigation menus and website headers/footers
                    - Advertisement content and promotional banners
                    - User interface elements (buttons, forms, etc.)
                    - Feedback requests and survey prompts
                    - Social media links and sharing options
                    - Copyright notices and legal disclaimers
                    - "Related articles" or "You might also like" sections
                
                3. FOCUS on extracting and summarizing:
                - The main topic and core subject matter
                - Key concepts, definitions, and explanations
                - Important facts, features, and capabilities
                - Step-by-step processes or procedures
                - Technical specifications and requirements
                - Benefits, use cases, and applications
                - Important warnings, notes, or limitations

                4. STRUCTURE your summary with:
                - A clear opening sentence identifying the main topic
                - Bullet points or numbered lists for key information
                - Logical flow from general concepts to specific details
                - Concise language without unnecessary jargon
                """
        return prompt