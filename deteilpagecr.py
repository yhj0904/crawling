import requests
from bs4 import BeautifulSoup

def get_detail_content(detail_url):
    response = requests.get(detail_url, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = {}

    # 1~7: <li><strong>항목명</strong><span>값</span>
    field_map = {
        "전문기관": "전문기관",
        "사업년도": "사업년도",
        "사업": "사업",
        "사업목적": "사업목적",
        "지원대상분야": "지원대상분야",
        "지원내용": "지원내용",
        "세부사항": "세부사항"
    }

    for li in soup.select('ul.list_dot02 > li'):
        strong = li.find('strong')
        span = li.find('span')
        if strong and span:
            key = strong.get_text(strip=True)
            if key in field_map:
                result[key] = span.get_text(separator='\n', strip=True)

    # 8: 첨부파일명
    file_tag = soup.select_one('ul.add_file span.text')
    result["첨부파일"] = file_tag.text.strip() if file_tag else "[첨부파일 없음]"

    # 9: 공모예정월 - 체크된 input에 대응하는 label 텍스트 추출
    months = []
    checked_inputs = soup.select('table.month_check input[checked]')
    for input_tag in checked_inputs:
        input_id = input_tag.get('id')
        label = soup.select_one(f'label[for="{input_id}"]')
        if label:
            months.append(label.text.strip())
    result["공모예정월"] = ', '.join(months) if months else "[없음]"

    return result
