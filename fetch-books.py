import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://dev.gutenberg.org/browse/scores/top'
response = requests.get(url)
web_content = response.content

soup = BeautifulSoup(web_content, 'html.parser')

target_url_pattern = re.compile(r'/ebooks/(\d+)')
elements = soup.find_all('a', href=lambda href: href and target_url_pattern.match(href))

save_dir = 'data'
os.makedirs(save_dir, exist_ok=True)

unique_hrefs = set()
for element in elements:
    href = element['href']
    if href not in unique_hrefs:
        unique_hrefs.add(href)
        
        match = target_url_pattern.search(href)
        if match:
            id = match.group(1)
            title = re.sub(r'\s*\(\d+\)\s*$', '', element.text).strip()
            txt_url = f"https://dev.gutenberg.org/cache/epub/{id}/pg{id}.txt"

            print(f"Text: {title}")
            print(f"Href: {href}")
            print(f"ID: {id}")
            print(f"URL: {txt_url}")
            print()

            file_path = os.path.join(save_dir, title)

            try:
                text_response = requests.get(txt_url)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_response.text)

                print(f"Text saved to {file_path}")
            except Exception as e:
                print(f"Error downloading {txt_url}: {e}")

print(f"Found {len(unique_hrefs)} unique elements")