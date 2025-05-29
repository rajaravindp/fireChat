import os
import logging
from src.TextToSpeech import TextToSpeech
from src.Firecrawler import Firecrawler
from src.Summarization import Summarization
from src.Prompt import Prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("webpage2audio.log"),
        logging.StreamHandler()
    ]
)

def main():
    url_input = input("Enter the URL of the webpage you want to scrape: ")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    crawler = Firecrawler(api_key=FIRECRAWL_API_KEY)
    webpage_content = crawler.scrape_webpage_content(url_input)
    if webpage_content:
        logging.info(f"Success: Webpage content fetched successfully ::: {webpage_content}")
    else:
        logging.error("Error: Failed to fetch webpage content.")
        return
  
    prompt = Prompt(text=webpage_content).get_prompt()
    if prompt:
        logging.info(f"Success ::: Prompt generated successfully ::: {prompt}")
    else:
        logging.error("Error ::: Failed to generate prompt.")
        return
    summary = Summarization(text=webpage_content, modelId="us.amazon.nova-lite-v1:0", prompt=prompt).get_summarization()
    if summary:
        logging.info(f"Success ::: Summary generated successfully ::: {summary}")
    else:
        logging.error("Error ::: Failed to generate summary.")
        return
    
    audio_output = TextToSpeech().synthesize(summary)
    if audio_output:
        logging.info("Success ::: Audio generated successfully.")
        with open("out/output.mp3", "wb") as file:
            file.write(audio_output.read())
            audio_output.close()
    else:
        logging.error("Error ::: Failed to generate audio.")

if __name__ == "__main__":
    main()