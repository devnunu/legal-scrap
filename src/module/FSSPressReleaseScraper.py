import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import pytz  # 추가: 한국 시간(KST) 설정을 위해 필요
from ..util.Utils import save_to_csv, get_html


class FSSPressReleaseScraper:
    def __init__(self):
        self.base_url = "https://www.fss.or.kr"
        self.press_release_url = f"{self.base_url}/fss/bbs/B0000188/list.do?menuNo=200218"
        self.output_dir = "output"
        self.ensure_output_dir()
        self.kst = pytz.timezone('Asia/Seoul')  # 추가: KST 타임존 설정

    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"{self.output_dir} 디렉토리를 생성했습니다.")

    def parse_releases(self, html):
        print("HTML 콘텐츠를 파싱하는 중입니다...")
        soup = BeautifulSoup(html, 'html.parser')
        releases = []
        yesterday = (datetime.now(self.kst) - timedelta(days=1)).strftime('%Y-%m-%d')

        items = soup.select('.bd-list tbody tr')
        total_items = len(items)
        print(f"총 {total_items}개의 항목이 발견되었습니다. 처리 중입니다...")

        for idx, item in enumerate(items):
            date = item.select_one('td:nth-of-type(4)').get_text(strip=True)
            if date == yesterday:
                title_element = item.select_one('.title a')
                title = title_element.get_text(strip=True)
                link = self.base_url + title_element['href']
                releases.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'agency': '금융감독원'
                })
            print(f"{idx + 1}/{total_items} 항목 처리 완료.", end="\r")

        print("\n파싱이 완료되었습니다.")
        return releases

    def scrape(self):
        html = get_html(self.press_release_url)
        releases = self.parse_releases(html)
        if releases:
            save_to_csv(releases, "fss_press_releases.csv", self.output_dir)
            print(f"어제 날짜의 보도자료 {len(releases)}개를 찾았습니다.")
        else:
            print("어제 날짜의 보도자료를 찾지 못했습니다.")

        print("\033[95m금융감독원 스크래핑이 완료되었습니다\033[0m")

