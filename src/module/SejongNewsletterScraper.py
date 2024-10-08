from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import pytz  # 추가: 한국 시간(KST) 설정을 위해 필요
from ..util.Utils import save_to_csv, get_html


class SejongNewsletterScraper:
    def __init__(self):
        self.base_url = "https://www.shinkim.com/kor/media/newsletter?code=%EC%A0%95%EB%B3%B4%EB%B3%B4%ED%98%B8&keyword="
        self.output_dir = "output"
        self.ensure_output_dir()
        self.kst = pytz.timezone('Asia/Seoul')  # 추가: KST 타임존 설정

    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"{self.output_dir} 디렉토리를 생성했습니다.")

    def parse_newsletters(self, html):
        print("HTML 콘텐츠를 파싱하는 중입니다...")
        soup = BeautifulSoup(html, 'html.parser')
        newsletters = []
        yesterday = (datetime.now(self.kst) - timedelta(days=1)).strftime('%Y.%m.%d')

        items = soup.select('ul.post-display li.post-item')
        total_items = len(items)
        print(f"총 {total_items}개의 항목이 발견되었습니다. 처리 중입니다...")

        for idx, item in enumerate(items):
            date = item.select_one('.foot-item.posted').get_text(strip=True)
            if date == yesterday:
                title_element = item.select_one('.post-name a.text')
                title = title_element.get_text(strip=True)
                link = "https://www.shinkim.com" + title_element['href']
                newsletters.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'agency': '법무법인 세종'
                })
            print(f"{idx + 1}/{total_items} 항목 처리 완료.", end="\r")

        print("\n파싱이 완료되었습니다.")
        return newsletters

    def scrape(self):
        html = get_html(self.base_url)
        newsletters = self.parse_newsletters(html)
        if newsletters:
            save_to_csv(newsletters, "shinkim_newsletters.csv", self.output_dir)
            print(f"어제 날짜의 뉴스레터 {len(newsletters)}개를 찾았습니다.")
        else:
            print("어제 날짜의 뉴스레터를 찾지 못했습니다.")

        print("\033[95m법무법인 세종 뉴스레터 스크래핑이 완료되었습니다\033[0m")
