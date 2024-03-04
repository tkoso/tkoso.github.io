from bs4 import BeautifulSoup
import requests
import os

# scrapowanie danych
url_link = "https://www.thechesswebsite.com/chess-openings/"
response = requests.get(url_link)

soup = BeautifulSoup(response.text, "html.parser")

header = soup.select_one('h1.elementor-heading-title.elementor-size-default')

scraped_openings = []
res = soup.findAll(id = "cb-container")
for auto in res[1].findAll("a"):
    scraped_openings.append(auto.find("h5").text)


container = soup.find('div', class_='elementor-text-editor elementor-clearfix')
paragraphs = [p.text for p in container.find_all('p')]
paragraphs.pop()
long_text = '\n\n'.join(paragraphs) + '\n\n'






# tworzenie pliku poczatkowego
with open('intro.md', 'w', encoding='utf-8') as file:
    buffer = f'# {header.text} \n'
    file.write("---\n")
    file.write("layout: page\n")
    file.write("title: \"Chess Openings - intro\"\n")
    file.write("permalink: /intro/\n")
    file.write("---\n")
    file.write(long_text)
    buffer = f'[list of openings](list_of_openings)'
    file.write(buffer)






# tworzenie pliku z lista
def scrape_opening_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    container = soup.find('div', class_='grid-65 mobile-grid-100 nopadding normal-left-col cb-post-grid')
    if container:
        paragraphs = container.find_all('p')
        if len(paragraphs) >= 3:
            return paragraphs[1].text + '\n\n' + paragraphs[2].text
    return "Description unavailable"

def scrape_opening_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    container = soup.find('div', class_='grid-65 mobile-grid-100 nopadding normal-left-col cb-post-grid')
    if container:
        paragraphs = container.find_all('p')
        filtered_paragraphs = [p.text for p in paragraphs if "video" not in p.text.lower() and "watch" not in p.text.lower()]
        full_description = '\n\n'.join(filtered_paragraphs)
        return full_description
    return "Description unavailable"

openings = [(name, f"openings/{name.lower().replace(' ', '-')}.md") for name in scraped_openings]
if not os.path.exists('openings'):
    os.makedirs('openings')

with open('list_of_openings.md', 'w', encoding='utf-8') as file:
    file.write("---\n")
    file.write("layout: page\n")
    file.write("title: \"List of chess openings\"\n")
    file.write("permalink: /intro/list_of_openings/\n")
    file.write("---\n")

    file.write(f"[back to intro](../)\n\n")
    for name, link in openings:
        detail_url = "https://www.thechesswebsite.com/" + link.replace("openings/", "").replace(".md", "/")
        short_description = scrape_opening_details(detail_url)
        long_description = scrape_opening_info(detail_url)
        local_detail_link = f"intro/list_of_openings/{link.replace('openings/', '').replace('.md', '')}"
        cropped_link = link.replace('openings/', '').replace('.md', '/')
        
        file.write(f"## [{name}]({detail_url})\n")
        file.write(f"{short_description}\n\n")
        file.write(f"[(...) for more info click here!]({cropped_link})\n\n")
        with open(link, 'w', encoding = 'utf-8') as detail_file:
            detail_file.write("---\n")
            detail_file.write("name: \"xyz\"\n")
            detail_file.write("title: null\n")
            detail_file.write("title-heading: false\n")
            detail_file.write("layout: page\n")
            detail_file.write("exclude: true\n")
            detail_file.write(f"permalink: /{local_detail_link}/\n")
            detail_file.write("---\n\n")

            detail_file.write(f"# {name}\n\n")
            detail_file.write(f"[back to list](../../list_of_openings)\n\n")
            detail_file.write(long_description)

