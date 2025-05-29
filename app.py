import os
import streamlit as st
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

st.title("JetSetAccess")

col1, col2 = st.columns([0.5, 0.5], gap="large", vertical_alignment='top')

with col1:
    with st.popover("Click to expand image"):
        st.image("assets/united_homepage.png", caption="United Airlines Booking Page", use_container_width=False)
    # st.image("assets/united_homepage.png", caption="United Airlines Booking Page", use_container_width=True)

with col2:
    url_input = st.text_input("Enter the URL of the webpage you want to scrape:")
    summary = None
    audio_output = None
    if st.button("Generate Audio Summary", ):
        if not url_input:
            st.error("Please enter a URL or upload a file.")
        else:
            FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
            crawler = Firecrawler(api_key=FIRECRAWL_API_KEY)
            webpage_content = crawler.scrape_webpage_content(url_input)
            if webpage_content:
                logging.info("Success: Webpage content fetched successfully")
                st.success("Webpage content fetched successfully.")
            else:
                logging.error("Error: Failed to fetch webpage content.")
                st.error("Failed to fetch webpage content.")
                st.stop()

            prompt = Prompt(text=webpage_content).get_prompt()
            if prompt:
                logging.info("Success: Prompt generated successfully")
            else:
                logging.error("Error: Failed to generate prompt.")
                st.error("Failed to generate prompt.")
                st.stop()

            summary = Summarization(
                text=webpage_content,
                modelId="us.amazon.nova-lite-v1:0",
                prompt=prompt
            ).get_summarization()
            if summary:
                logging.info("Success: Summary generated successfully")
                with st.expander("Summary"):
                    st.write(summary)
            else:
                logging.error("Error: Failed to generate summary.")
                st.error("Failed to generate summary.")
                st.stop()

            audio_output = TextToSpeech().synthesize(summary)
            if audio_output:
                logging.info("Success: Audio generated successfully.")
                with st.expander("Audio Summary"):
                    st.audio(audio_output.read(), format="audio/mp3")
                audio_output.close()
            else:
                logging.error("Error: Failed to generate audio.")
                st.error("Failed to generate audio.")
