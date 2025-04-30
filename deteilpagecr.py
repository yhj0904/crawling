import re
import requests
from bs4 import BeautifulSoup
import os

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
                if key == "세부사항":
                    raw_text = span.get_text(separator='\n', strip=True)
                    cleaned = re.sub(r'\n{2,}', '\n', raw_text)
                    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
                    result[key] = cleaned.strip()
                else:
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
    
    a_tag = soup.select_one('ul.add_file a.file_down')
    if a_tag:
        onclick = a_tag.get('href')  # javascript:f_ancmPrntc_downloadAtchFile(...)
        match = re.search(r"f_ancmPrntc_downloadAtchFile\('(.+?)','(.+?)','(.+?)','(.+?)'\)", onclick)
        if match:
            atch_doc_id, atch_file_id, file_name, _ = match.groups()
            download_msg = download_attachment_file(atch_doc_id, atch_file_id, file_name)
            result["첨부파일 다운로드"] = download_msg
        else:
            result["첨부파일 다운로드"] = "[onclick 파싱 실패]"
    else:
        result["첨부파일 다운로드"] = "[첨부파일 없음]"


    return result

def print_pretty_detail(data):
    print("\n📌 상세 페이지 요약\n" + "="*50)
    field_order = [
        "전문기관", "사업년도", "사업", "사업목적",
        "지원대상분야", "지원내용", "세부사항",
        "첨부파일", "공모예정월", "첨부파일 다운로드"
    ]

    for field in field_order:
        value = data.get(field, "[없음]").strip()
        print(f"\n✅ {field}\n{'-'*len(field)}")
        print(value)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def download_attachment_file(atch_doc_id, atch_file_id, file_name, save_dir='./downloads'):
    os.makedirs(save_dir, exist_ok=True)

    url = "https://www.iris.go.kr/comm/file/fileDownload.do"
    params = {
        'atchDocId': atch_doc_id,
        'atchFileId': atch_file_id,
        'otxt': 'Y'
    }
    
    safe_file_name = sanitize_filename(file_name)
    file_path = os.path.join(save_dir, safe_file_name)

    if os.path.exists(file_path):
        return f"[건너뜀] 이미 존재함: {file_path}"

    response = requests.post(url, params=params, stream=True)

    if response.status_code == 200 and 'Content-Disposition' in response.headers:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return f"[✔ 저장됨] {file_path}"
    else:
        return f"[✘ 실패] status={response.status_code}, headers={response.headers}"
