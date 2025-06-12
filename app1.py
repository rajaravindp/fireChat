import streamlit as st
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

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'homepage'

def show_homepage():
    """Display the JetSetAccess homepage"""
    st.title("JetSetAccess")
    st.markdown("---")
    
    # Welcome section
    st.header("Welcome to JetSetAccess")
    st.write("Your ultimate tool for converting web content into accessible audio summaries.")
    
    # Key features section
    st.subheader("Why JetSetAccess?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Web Content Extraction**")
        st.write("Effortlessly scrape text from any webpage")
    
    with col2:
        st.markdown("**Smart Summarization**")
        st.write("Generate concise summaries of lengthy content")
    
    with col3:
        st.markdown("**Audio Conversion**")
        st.write("Transform text into natural-sounding audio summaries")
    
    # Call to action
    st.markdown("---")
    st.subheader("Summary")
    # Add summary of the webpage
    st.write("""
            
            The main topic of the provided text is the United Airlines website, focusing on booking flights, travel deals, and related services.

            Core Subject Matter:
            Booking flights and travel deals on United Airlines.
            Information on MileagePlus award tickets and benefits.
            Key Concepts and Features:

            Booking Flights:
            Options for roundtrip, one-way, and flexible dates.
            Advanced search features for certificates, multi-city, and upgrades.
            MileagePlus:
            Benefits include 60,000 bonus miles and $0 intro annual fee with the United Explorer Card.
            Free Wi-Fi on select flights for MileagePlus members.

            Travel Deals:
            Offers on flights, hotels, and rental cars.
            Interactive map to find flights to various destinations.
            
            Important Facts and Capabilities:
            Prices shown are roundtrip fares available within the last 48 hours.
            Additional baggage fees and taxes/fees may apply.
            United Airlines provides various travel packages including flights, hotels, and car rentals.

            Step-by-Step Processes:
            Navigate to the United Airlines website.
            Select the type of trip (roundtrip, one-way).
            Enter travel dates and destinations.
            Use the search function to find flights.
            Book flights using miles or cash.
            Benefits and Use Cases:

            For Travelers:
            Easy booking process with various options.
            Access to travel deals and MileagePlus benefits.
            For MileagePlus Members:
            Exclusive perks like free Wi-Fi on select flights.
            Bonus miles and special card offers.
            
            Warnings and Limitations:
            Additional fees may apply for baggage and optional services.
            Prices are subject to change and availability.
    """)
    
    if st.button("Convert Your First Webpage"):
        st.session_state.current_page = 'main_page'
        st.rerun()

def show_main_page():
    """Display the main functionality page"""
    st.title("JetSetAccess - Webpage to Audio Converter")
    st.markdown("---")
    
    col1, col2 = st.columns([0.5, 0.5], gap="large", vertical_alignment='top')

    with col1:
        st.image("assets/united_homepage.png", caption="United Airlines Webpage", use_container_width=True)

    with col2:
        url_input = st.text_input("Enter the URL of the webpage you want to scrape:")
        summary = None
        audio_output = None
        
        if st.button("Generate Audio Summary"):
            if not url_input:
                st.error("Please enter a URL.")
            else:
                FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
                crawler = Firecrawler(api_key=FIRECRAWL_API_KEY)
                webpage_content = crawler.scrape_webpage_content(url_input)
                
                if not webpage_content:
                    logging.error("Error: Failed to fetch webpage content.")
                    st.error("Failed to fetch webpage content.")
                    st.stop()
                
                prompt = Prompt(text=webpage_content).get_prompt()
                if not prompt:
                    logging.error("Error: Failed to generate prompt.")
                    st.error("Failed to generate prompt.")
                    st.stop()

                summary = Summarization(
                    text=webpage_content,
                    modelId="us.amazon.nova-lite-v1:0",
                    prompt=prompt
                ).get_summarization()
                
                if not summary:
                    logging.error("Error: Failed to generate summary.")
                    st.error("Failed to generate summary.")
                    st.stop()

                with st.expander("See Summary"):
                    st.write(summary)
                
                audio_output = TextToSpeech().synthesize(summary)
                if not audio_output:
                    logging.error("Error: Failed to generate audio.")
                    st.error("Failed to generate audio.")
                else:
                    with st.expander("Play Audio Summary"):
                        st.audio(audio_output.read(), format="audio/mp3")
                    audio_output.close()

# Page navigation
if st.session_state.current_page == 'homepage':
    show_homepage()
else:
    show_main_page()