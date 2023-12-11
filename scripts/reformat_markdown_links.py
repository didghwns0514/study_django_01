# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse

import os
from newspaper import Article  # noqa


print("Starting script...")


def extract_title_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.title
    except Exception as e:
        print(f"Error while processing {url}: {e}")
        return None


def extract_base_domain(url):
    """
    Extract the base domain from a URL. For example,
    'https://www.youtube.com/watch' becomes 'youtube'.
    """
    domain = urlparse(url).netloc
    # Split by '.' and take the second last part to handle domains like 'www.youtube.com'
    return domain.split(".")[-2]


def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Find URLs that aren't already inside []()
    urls = re.findall(r"(?<!\]\()\bhttps?://\S+", content)

    modified = False
    for url in urls:
        title = extract_title_from_url(url)
        base_domain = extract_base_domain(url)
        if title:
            formatted_link = f"[{base_domain} - {title}]({url})"
            content = content.replace(
                url, formatted_link, 1
            )  # Replace only the first occurrence
            modified = True

    if modified:
        print(f"!!!!! Modified {file_path}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


def main():
    # Get the absolute path of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set your desired starting folder here, relative to the location of this script
    folder_path = os.path.join(script_dir, "../docs")

    # Convert to an absolute path
    folder_path = os.path.abspath(folder_path)
    root_path = list(os.walk(folder_path))

    print(f"Processing folder {folder_path}")
    print(f"root_path: {root_path}")

    for root, _, files in root_path:
        for file in files:
            if file.endswith(".md"):
                print("-" * 80)
                print("-" * 80)
                print(f"Processing {file}")
                process_file(os.path.join(root, file))
                print(f"Finished processing {file}")


main()
