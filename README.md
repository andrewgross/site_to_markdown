# Markdown Documentation Scraper

This tool is a web scraper built using Scrapy that extracts and consolidates content from a documentation website into a single Markdown file. It is flexible, allowing you to specify a starting URL, restrict crawling to specific domains, and define the output file name.

---

## Features

- Crawls a documentation website starting from a given URL.
- Automatically extracts the main content using `Readability` while skipping non-relevant elements (headers, sidebars, etc.).
- Consolidates all pages into a single Markdown file with structured headings.
- Allows optional restriction to specific domains.
- Skips non-English pages to keep the output consistent.

---

## Requirements

### Python Libraries
- `scrapy`
- `readability-lxml`
- `lxml[html_clean]`
- `langdetect`
- `markdownify`

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage
### Command Syntax

```
scrapy runspider site_to_markdown.py \
    -a start_url=<STARTING_URL> \
    [-a allowed_domains=<DOMAIN1,DOMAIN2>] \
    [-a output_file=<OUTPUT_FILENAME>]
    [-a cookies_file=<PATH_TO_COOKIE_JSON_FILE>]
```

### Arguments


1. `start_url` (required): The starting URL for the crawler. The scraper will begin its crawl from this URL.
    * Example: `https://example-docs-site.com`

2. `allowed_domains` (optional): A comma-separated list of domains to restrict the crawl. If not provided, the scraper will infer the domain from the start_url.
    * Example: `example-docs-site.com,docs.example.com`

3. `output_file` (optional): The name of the output Markdown file. Default is documentation.md. 
    * Example: `output.md`

3. `cookies_file` (optional): The path to a JSON file of cookies to use for requests. Default is None.
    * Example: `./cookies.json`


## Example Usage
### Basic Crawling

To crawl a single domain:


```
scrapy runspider site_to_markdown.py \
    -a start_url=https://example-docs-site.com
```

### Multiple Domains

To allow crawling across multiple domains:

```
scrapy runspider site_to_markdown.py \
    -a start_url=https://example-docs-site.com \
    -a allowed_domains=example-docs-site.com,docs.example.com
```

### Custom Output File

To specify a custom output file:

```
scrapy runspider site_to_markdown.py \
    -a start_url=https://example-docs-site.com \
    -a output_file=my_documentation.md
```

## Output Format

The scraper generates a single Markdown file with the following structure:

```
# Documentation

## Page 1 Title

Content for Page 1...

## Page 2 Title

Content for Page 2...

...
```

## Notes

* `Non-Text Content`: The scraper skips non-HTML pages (e.g., images, PDFs).
* `Non-English Pages`: Only English pages are processed.
* `URL Validation`: Ensures only valid URLs are crawled (ignores javascript:, mailto:, etc.).
* `File Overwriting`: If the output file already exists, it will be overwritten.

## Contributing

Contributions are welcome! Feel free to submit pull requests or report issues on GitHub.