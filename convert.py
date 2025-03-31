#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///
"""Process markdown files to add title and date after frontmatter."""
from pathlib import Path
import re
import yaml


def format_date(date_val) -> str:
    """Format date string or date object to Sun, 01 Jan 2000."""
    return date_val.strftime("%a, %d %b %Y")

def process_markdown_file(file_path: Path) -> None:
    """Process a single markdown file to add title and date after frontmatter."""
    content = file_path.read_text()

    # Split content into frontmatter and body
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not frontmatter_match:
        return

    frontmatter, body = frontmatter_match.groups()

    # Parse frontmatter
    try:
        metadata = yaml.safe_load(frontmatter)
    except yaml.YAMLError:
        return

    # Extract title and date
    title = metadata.get("title", "").strip('"')
    date = metadata.get("date")
    if not title or not date:
        return

    # Format new content
    formatted_date = format_date(date)
    new_content = f"""---
{frontmatter}
---

# {title}

*{formatted_date}*

{body.strip()}"""

    # Write back to file
    file_path.write_text(new_content)

def main() -> None:
    """Process all markdown files in the current directory."""
    for file_path in Path(".").glob("2*.md"):
        process_markdown_file(file_path)

if __name__ == "__main__":
    main()
