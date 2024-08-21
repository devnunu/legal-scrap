import os
from src.module.FSCPressReleaseScraper import FSCPressReleaseScraper
from src.module.FSSPressReleaseScraper import FSSPressReleaseScraper
from src.module.PIPCPressReleaseScraper import PIPCPressReleaseScraper
from src.module.KIFPressReleaseScraper import KIFPressReleaseScraper
from src.module.FSECPressReleaseScraper import FSECPressReleaseScraper
from src.module.KInternetPressReleaseScraper import KInternetPressReleaseScraper
from src.module.SejongNewsletterScraper import SejongNewsletterScraper
from src.module.BKLNewsletterScraper import BKLNewsletterScraper
from src.module.YulchonNewsletterScraper import YulchonNewsletterScraper
from src.util.Utils import read_csv_and_format_message
from src.slack.SlackNotifier import SlackNotifier
from config import WEBHOOK_URL
from datetime import datetime
import pytz

# 한국 시간(KST) 타임존 설정
kst = pytz.timezone('Asia/Seoul')

def scrap_and_notify():
    """
    스크래핑과 에러 발생 시 슬랙 알림
    """
    scraper_classes = [
        ("금융위원회", FSCPressReleaseScraper),
        ("금융감독원", FSSPressReleaseScraper),
        ("개인정보보호 위원회", PIPCPressReleaseScraper),
        ("금융보안원", FSECPressReleaseScraper),
        ("한국 인터넷 기업협회", KInternetPressReleaseScraper),
        ("법무법인 태평양", BKLNewsletterScraper),
        ("법무법인 율촌", YulchonNewsletterScraper)
    ]

    notifier = SlackNotifier(WEBHOOK_URL)

    for agency_name, ScraperClass in scraper_classes:
        scraper = ScraperClass()
        try:
            scraper.scrape()
        except Exception as e:
            # 스크래핑 중 에러가 발생했을 경우 슬랙 메시지 발송
            error_message = f"⚠️ [{agency_name}] 모듈에서 문제가 발생했습니다. HTML 구조가 변경되었을수 있으니 확인해주세요!"
            notifier.send_message(error_message)
            print(error_message)  # 콘솔에도 출력


def make_and_send_slack_msg():
    # Slack Webhook URL 설정
    webhook_url = WEBHOOK_URL
    notifier = SlackNotifier(webhook_url)

    # output 폴더의 모든 CSV 파일 처리
    output_dir = "output"
    agencies = {
        "fsc_press_releases.csv": ("금융위원회", "https://www.fsc.go.kr"),
        "fss_press_releases.csv": ("금융감독원", "https://www.fss.or.kr"),
        "pipc_press_releases.csv": ("개인정보보호 위원회", "https://www.pipc.go.kr"),
        "fsec_press_releases.csv": ("금융보안원", "https://www.fsec.or.kr"),
        "kinternet_press_releases.csv": ("한국 인터넷 기업협회", "https://www.kinternet.org"),
        "bkl_newsletters.csv": ("법무법인 태평양", "https://www.bkl.co.kr"),
        "yulchon_newsletters.csv": ("법무법인 율촌", "https://www.yulchon.com")
    }

    final_message = ""
    for file_name, (agency_name, base_url) in agencies.items():
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            message = read_csv_and_format_message(file_path, agency_name, base_url)
            if message:  # 만약 파일에 항목이 있으면 메시지를 추가합니다.
                final_message += f"{message}\n"

    # 최종 메시지 전송
    today_date = datetime.now(kst).strftime("%m월 %d일")
    if final_message:
        header = f"*:judge: [{today_date}일, 새로운 법률 소식]*\n\n"
        notifier.send_message(header + final_message)
    else:
        # 만약 final_message가 빈 문자열이면 "업데이트된 법률 소식이 없음" 메시지 전송
        no_update_message = f"*:judge: [{today_date}일, 새로운 법률 소식]*\n\n*신규로 업데이트된 법률 소식이 없어요!*"
        notifier.send_message(no_update_message)


if __name__ == "__main__":
    scrap_and_notify()  # 스크래핑 실행 및 오류 발생 시 알림
    make_and_send_slack_msg()  # 슬랙 메시지 발송
    print("\033[92m모든 작업이 완료되었습니다\033[0m")

