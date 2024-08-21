# src/util/Utils.py

import os
import pandas as pd
import requests


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    print("HTML 콘텐츠를 가져오는 중입니다...")
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    print("HTML 콘텐츠를 성공적으로 가져왔습니다.")
    return response.text


def save_to_csv(data, filename, output_dir="output"):
    file_path = os.path.join(output_dir, filename)
    print("CSV 파일로 데이터를 저장하는 중입니다...")

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"데이터가 {file_path} 파일로 저장되었습니다.")


def read_csv_and_format_message(file_path, agency_name, base_url):
    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 메시지 형식 구성
    # 타이틀에 하이퍼링크 추가
    message = f"*<{base_url}|[{agency_name}]>*\n"
    for index, row in df.iterrows():
        title = row['title']
        link = row['link']
        # 비정상적인 URL 확인 후 처리
        if "javascript" not in link:
            message += f"- {title} (<{link}|링크>)\n"
        else:
            message += f"- {title}\n"

    return message
