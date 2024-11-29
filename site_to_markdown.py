import scrapy
from readability import Document
from langdetect import detect
import os
from urllib.parse import urlparse


class DocumentationSpider(scrapy.Spider):
    name = "dynamic_markdown_docs"

    def __init__(
        self,
        start_url=None,
        allowed_domains=None,
        output_file="documentation.md",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError(
                "You must provide a starting URL using the `-a start_url=<URL>` argument."
            )
        self.start_urls = [start_url]

        # Parse allowed domains from the starting URL or use provided domains
        if allowed_domains:
            self.allowed_domains = allowed_domains.split(",")
        else:
            parsed_domain = urlparse(start_url).netloc
            self.allowed_domains = [parsed_domain]

        self.output_file = output_file

        # Initialize or overwrite the output file
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write("# Documentation\n\n")

    def parse(self, response):
        if not self.is_text_response(response):
            self.logger.info(f"Skipping non-text content: {response.url}")
            return

        extracted_content = self.extract_content(response)
        if not extracted_content:
            return

        relevant_html, title = extracted_content

        if not self.is_english(relevant_html, response.url):
            return

        self.append_to_markdown(title, relevant_html)

        # Follow links to other pages
        for link in response.css("a::attr(href)").getall():
            if self.is_valid_url(link):
                yield response.follow(link, self.parse)

    def is_text_response(self, response):
        """Check if the response is text-based."""
        content_type = response.headers.get("Content-Type", b"").decode("utf-8")
        return content_type.startswith("text/html")

    def extract_content(self, response):
        """Extract relevant content using Readability."""
        try:
            doc = Document(response.text)
            relevant_html = doc.summary()
            title = doc.title()
            return relevant_html, title
        except Exception as e:
            self.logger.warning(f"Failed to process page {response.url}: {e}")
            return None

    def is_english(self, text, url):
        """Check if the text is in English."""
        try:
            lang = detect(text)
            if lang != "en":
                self.logger.info(f"Skipping non-English page: {url}")
                return False
            return True
        except Exception as e:
            self.logger.warning(f"Language detection failed for {url}: {e}")
            return False

    def append_to_markdown(self, title, html_content):
        """Append extracted content to the single Markdown file."""
        from markdownify import markdownify as md

        markdown_content = md(html_content)
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"## {title}\n\n")
            f.write(markdown_content + "\n\n")

    @staticmethod
    def is_valid_url(url):
        """Check if the URL is valid and starts with http or https."""
        parsed = urlparse(url)
        return not parsed.scheme or parsed.scheme in ("http", "https")
