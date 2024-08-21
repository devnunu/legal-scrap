from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from ..util.Utils import save_to_csv, get_html


class PIPCPressReleaseScraper:
    def __init__(self):
        self.base_url = "https://www.pipc.go.kr"
        self.press_release_url = f"{self.base_url}/np/cop/bbs/selectBoardList.do?bbsId=BS074&mCode=C020010000"
        self.output_dir = "output"
        self.ensure_output_dir()

    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"{self.output_dir} 디렉토리를 생성했습니다.")

    def parse_releases(self, html):
        print("HTML 콘텐츠를 파싱하는 중입니다...")
        soup = BeautifulSoup(html, 'html.parser')
        releases = []
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        items = soup.select('.boardArea tbody tr')
        total_items = len(items)
        print(f"총 {total_items}개의 항목이 발견되었습니다. 처리 중입니다...")

        for idx, item in enumerate(items):
            date = item.select_one('td:nth-of-type(4)').get_text(strip=True)
            if date == yesterday:
                title_element = item.select_one('.boardTitle a')
                title = title_element.get_text(strip=True)
                link = self.base_url + title_element['href']
                releases.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'agency': '개인정보보호위원회'
                })
            print(f"{idx + 1}/{total_items} 항목 처리 완료.", end="\r")

        print("\n파싱이 완료되었습니다.")
        return releases

    def scrape(self):
        html = get_html(self.press_release_url)
        releases = self.parse_releases(html)
        if releases:
            save_to_csv(releases, "pipc_press_releases.csv", self.output_dir)
            print(f"어제 날짜의 보도자료 {len(releases)}개를 찾았습니다.")
        else:
            print("어제 날짜의 보도자료를 찾지 못했습니다.")

        print("\033[95m개인정보보호위원회 스크래핑이 완료되었습니다\033[0m")

