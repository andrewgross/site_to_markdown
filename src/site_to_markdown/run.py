from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from site_to_markdown.spider import DocumentationSpider
from urllib.parse import urlparse


def parse_domain(value):
    """Parse a domain from either a URL or plain domain string."""
    if value.startswith(('http://', 'https://')):
        return urlparse(value).netloc
    return value


def main():
    # Parse command-line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Run the site_to_markdown scraper")
    parser.add_argument(
        "-u", "--start_url", type=str, required=True, help="Starting URL for scraping"
    )
    parser.add_argument(
        "-a",
        "--allowed_domains",
        type=parse_domain,
        required=True,
        nargs="+",
        help="Allowed domains for scraping (can be URLs or plain domains)",
    )
    parser.add_argument(
        "-e",
        "--exclude_filetypes",
        type=str,
        required=False,
        nargs="+",
        help="Excluded filetypes for scraping (comma-separated). Ex: rst.txt,zip",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=True,
        help="Output file for markdown content",
    )
    parser.add_argument(
        "-c",
        "--cookies_file",
        type=str,
        default=None,
        help="Path to cookies file (optional)",
    )
    args = parser.parse_args()

    # Prepare settings dictionary (optional)
    settings = get_project_settings()
    if args.cookies_file:
        settings["COOKIES_ENABLED"] = True

    # Create crawler process
    process = CrawlerProcess(settings)
    
    # Pass arguments directly to spider
    process.crawl(
        DocumentationSpider,
        start_url=args.start_url,
        allowed_domains=",".join(args.allowed_domains),
        output_file=args.output_file,
        cookies_file=args.cookies_file,
        exclude_filetypes=args.exclude_filetypes,
    )

    # Start the crawl
    process.start()


if __name__ == "__main__":
    main()
