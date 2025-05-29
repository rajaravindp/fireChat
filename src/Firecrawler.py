from firecrawl import FirecrawlApp, ScrapeOptions
from typing import Optional
class Firecrawler:
    """A class to handle webpage content scraping and crawling using Firecrawl."""
    
    def __init__(self, api_key: Optional[str]):
        """
        Initialize the WebpageScraper with Firecrawl API key.

        Args:
            api_key (str): Firecrawl API key.
        """
        self.api_key = api_key or "fc-7511ffc31f92450c8d4cde7a8895ca2e"
        self.app = FirecrawlApp(api_key=self.api_key)

    def scrape_webpage_content(self, url: str) -> str:
        """
        Fetches the content of a webpage given its URL.

        Args:
            url (str): The URL of the webpage to fetch.

        Returns:
            str: The content of the webpage.
        """
        webpage_scrape_result = self.app.scrape_url(
            url,
            formats=['markdown'],
            only_main_content=True, 
            exclude_tags=['nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript'],
            remove_base64_images=True,
            block_ads=True,
            wait_for=3
        )
        
        return str(webpage_scrape_result)

    def crawl_website(self, url: str) -> str:
        """
        Crawls a website and fetches content from multiple pages.

        Args:
            url (str): The URL of the website to crawl.
            max_pages (int): Maximum number of pages to crawl.

        Returns:
            list: List of scraped content from the crawled pages.
        """
        scrape_options = ScrapeOptions(
            onlyMainContent=True,
            formats=['markdown'],
            waitFor=3, 
            blockAds=True, 
            removeBase64Images=True
        )
        
        crawl_result = self.app.crawl_url(
                                    url,
                                    scrape_options=scrape_options)
                                
        return str(crawl_result)