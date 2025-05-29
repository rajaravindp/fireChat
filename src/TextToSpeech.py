import boto3
from typing import IO

class TextToSpeech:
    def __init__(self, voice_id="Ivy", output_format="mp3", language_code="en-US"):
        self.voice_id = voice_id
        self.output_format = output_format
        self.language_code = language_code
        self.session = boto3.Session()
        self.polly_client = self.session.client(
            service_name='polly',
            region_name='us-east-2',
            verify=False)

    def synthesize(self, text) -> IO[bytes]:
        """
        Convert text to speech using Amazon Polly.
        """
        response = self.polly_client.synthesize_speech(
            Text=text,
            OutputFormat=self.output_format,
            VoiceId=self.voice_id,
            LanguageCode=self.language_code
        )
        return response['AudioStream']