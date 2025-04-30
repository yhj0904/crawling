import requests
from bs4 import BeautifulSoup

def get_titles_from_page(page_num):
    url = f"https://www.iris.go.kr/contents/retrieveAncmPrntcListView.do?pageIndex={page_num}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    
    total_pages = int(soup.select_one('.total_page b').text)
    current_page = int(soup.select_one('.current_page strong').text)

    titles = soup.select('.form-row .group .title a')
    for title in titles:
        print(title.text.strip())
    
    return total_pages, current_page

page = 1
while True:
    print(f"\n=== Page {page} ===")
    total_pages, current_page = get_titles_from_page(page)
    
    if current_page >= total_pages:
        break
        
    page += 1
    time.sleep(1)  
