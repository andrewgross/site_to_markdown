import scrapy
from readability import Document
from langdetect import detect
import os
from markdownify import markdownify as md
from urllib.parse import urlparse


class DocumentationSpider(scrapy.Spider):
    name = "readability_docs"
    start_urls = ["https://dspy.ai"]
    allowed_domains = ["dspy.ai"]
    output_dir = "markdown_pages"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.makedirs(self.output_dir, exist_ok=True)

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

        self.save_markdown(title, relevant_html)

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

    def save_markdown(self, title, html_content):
        """Convert HTML to Markdown and save to a file."""
        markdown_content = md(html_content)
        file_name = f"{self.sanitize_filename(title)}.md"
        output_path = os.path.join(self.output_dir, file_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{markdown_content}")

    @staticmethod
    def sanitize_filename(name):
        """Sanitize filenames for safe storage."""
        return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in name).strip()

    @staticmethod
    def is_valid_url(url):
        """Check if the URL is valid and starts with http or https."""
        parsed = urlparse(url)
        return not parsed.scheme or parsed.scheme in ("http", "https")
