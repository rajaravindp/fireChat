import json
import boto3
from typing import Optional

class Summarization:
    """
    This class is responsible for generating a summary of the given text using the OpenAI API.
    """
    def __init__(self,
                text: str,
                modelId: str,
                prompt: str,
                max_tokens: Optional[int] = None,
                temperature: Optional[float] = None):
        
        self.text = text
        self.modelId = modelId
        self.prompt = prompt
        self.max_tokens = max_tokens if max_tokens is not None else 2000
        self.temperature = temperature if temperature is not None else 0.3
        self.session = boto3.Session()
        self.bedrock_client = self.session.client(
                                service_name='bedrock-runtime',
                                region_name='us-east-1',
                                verify=False)
        
    def get_summarization(self) -> str:
        """
        Generate a summary of the given text using the OpenAI API.
        
        Args:
            text (str): The text to summarize.
        
        Returns:
            str: The generated summary.
        """

        body = json.dumps(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": self.prompt
                            }
                        ]
                    }
                ], 
                "inferenceConfig": {
                    "maxTokens": self.max_tokens,
                    "temperature": self.temperature
                },
            }
        )
        accept='application/json'
        contentType='application/json'

        response = self.bedrock_client.invoke_model(
            body=body,
            modelId=self.modelId,
            accept=accept,
            contentType=contentType,
        )
        response_body = json.loads(response.get('body').read())
        content_text = response_body['output']['message']['content'][0]['text']
        bedrock_response = "".join(content_text)

        return bedrock_response