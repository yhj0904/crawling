import requests
from bs4 import BeautifulSoup
import time
import re

from deteilpagecr import print_pretty_detail, get_detail_content

def get_titles_from_page(page_num):
    url = f"https://www.iris.go.kr/contents/retrieveAncmPrntcListView.do?pageIndex={page_num}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    total_pages = int(soup.select_one('.total_page b').text)
    current_page = int(soup.select_one('.current_page strong').text)

    titles = soup.select('.form-row .group .title a')
    orgs = soup.select('.form-row .group > span[data-title="전문기관"]')
    businessYears = soup.select('.form-row .group > span:nth-of-type(3)')

    for title, org, year in zip(titles, orgs, businessYears):
        print(title.text.strip())
        print(org.text.strip().replace('전문기관 :', ''))
        print(year.find('strong').next_sibling.strip())

        onclick = title.get('onclick')
        if onclick:
            params = re.findall(r"'(.*?)'", onclick)
            if len(params) == 8:
                detail_url = (
                    f"https://www.iris.go.kr/contents/retrieveAncmPrntcView.do?"
                    f"ancmId={params[0]}&bsnsYy={params[1]}&sorgnBsnsCd={params[2]}"
                    f"&ancmPrntcSn={params[3]}&ancmTurn={params[4]}&seq={params[5]}"
                    f"&hirkSorgnBsnsCd={params[6]}&sorgnId={params[7]}"
                )
                
                detail_text = get_detail_content(detail_url) if detail_url else '[URL 없음]'
                
                print(detail_url)
                print_pretty_detail(detail_text)
        print("---")

    return total_pages, current_page

page = 1
while True:
    print(f"\n=== Page {page} ===")
    total_pages, current_page = get_titles_from_page(page)

    if current_page >= total_pages:
        break

    page += 1
    time.sleep(1)
