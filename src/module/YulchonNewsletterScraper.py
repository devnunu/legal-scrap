import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from ..util.Utils import save_to_csv, get_html

# 법무법인 율촌
class YulchonNewsletterScraper:
    def __init__(self):
        self.base_url = "https://www.yulchon.com"
        self.newsletter_url = f"{self.base_url}/ko/resources/publications/newsletter.do"
        self.output_dir = "output"
        self.ensure_output_dir()

    def ensure_output_dir(self):
        # output 디렉토리가 없으면 생성합니다.
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"{self.output_dir} 디렉토리를 생성했습니다.")

    def parse_newsletters(self, html):
        print("HTML 콘텐츠를 파싱하는 중입니다...")
        soup = BeautifulSoup(html, 'html.parser')
        newsletters = []
        yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y. %m. %d.')

        items = soup.select('ul.list_type_post li')
        total_items = len(items)
        print(f"총 {total_items}개의 항목이 발견되었습니다. 처리 중입니다...")

        for idx, item in enumerate(items):
            date = item.select_one('.date').get_text(strip=True)
            if date == yesterday:
                title_element = item.select_one('.title em')
                title = title_element.get_text(strip=True) if title_element else "제목 없음"
                # 링크 추출 및 base_url과 결합
                link_element = item.select_one('.new_post_link')
                link = self.base_url + link_element['href'] if link_element else "링크 없음"
                newsletters.append({
                    'title': title,
                    'link': link,
                    'date': date,
                    'agency': '법무법인 율촌'
                })
            print(f"{idx + 1}/{total_items} 항목 처리 완료.", end="\r")

        print("\n파싱이 완료되었습니다.")
        return newsletters

    def scrape(self):
        html = get_html(self.newsletter_url)
        newsletters = self.parse_newsletters(html)
        if newsletters:
            save_to_csv(newsletters, "yulchon_newsletters.csv", self.output_dir)
            print(f"어제 날짜의 뉴스레터 {len(newsletters)}개를 찾았습니다.")
        else:
            print("어제 날짜의 뉴스레터를 찾지 못했습니다.")

        # 스크래핑 완료 메시지 출력 (보라색 텍스트)
        print("\033[95m법무법인 율촌 스크래핑이 완료되었습니다\033[0m")
