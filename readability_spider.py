import scrapy
from readability import Document
from langdetect import detect
import os


class DocumentationSpider(scrapy.Spider):
    name = "readability_docs"
    start_urls = ["https://dspy.ai"]
    output_dir = "markdown_pages"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.makedirs(self.output_dir, exist_ok=True)

    def parse(self, response):
        if response.url.endswith(".html"):  # Optional: Only handle HTML pages
            # Use Readability to extract relevant content
            doc = Document(response.text)
            relevant_html = doc.summary()
            title = doc.title()

            # Detect language
            try:
                lang = detect(relevant_html)
            except Exception as e:
                self.logger.warning(
                    f"Language detection failed for {response.url}: {e}"
                )
                return

            if lang != "en":
                self.logger.info(f"Skipping non-English page: {response.url}")
                return

            # Convert to Markdown
            from markdownify import markdownify as md

            markdown_content = md(relevant_html)

            # Save the markdown file
            file_name = f"{self.sanitize_filename(title)}.md"
            output_path = os.path.join(self.output_dir, file_name)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n{markdown_content}")

        # Follow links to other pages
        for link in response.css("a::attr(href)").getall():
            yield response.follow(link, self.parse)

    @staticmethod
    def sanitize_filename(name):
        # Replace unsafe characters in filenames
        return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in name).strip()
