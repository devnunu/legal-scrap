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


def main():
    """
    스크래핑
    """
    # 금융위원회
    scraper = FSCPressReleaseScraper()
    scraper.scrape()

    # 금융감독원
    scraper = FSSPressReleaseScraper()
    scraper.scrape()

    # 개인정보보호 위원회
    scraper = PIPCPressReleaseScraper()
    scraper.scrape()

    # 한국 금융 연구원
    # scraper = KIFPressReleaseScraper()
    # scraper.scrape()

    # 금융보안원
    scraper = FSECPressReleaseScraper()
    scraper.scrape()

    # 한국 인터넷 기업협회
    scraper = KInternetPressReleaseScraper()
    scraper.scrape()

    # 법무법인 세종
    # scraper = SejongNewsletterScraper()
    # scraper.scrape()

    # 법무법인 태평양
    scraper = BKLNewsletterScraper()
    scraper.scrape()

    # 법무법인 율촌
    scraper = YulchonNewsletterScraper()
    scraper.scrape()

    """
    슬랙 메세지 발송
    """
    # Slack Webhook URL 설정
    webhook_url = WEBHOOK_URL
    notifier = SlackNotifier(webhook_url)

    # output 폴더의 모든 CSV 파일 처리
    output_dir = "output"
    agencies = {
        "fsc_press_releases.csv": "금융위원회",
        "fss_press_releases.csv": "금융감독원",
        "pipc_press_releases.csv": "개인정보보호 위원회",
        "fsec_press_releases.csv": "금융보안원",
        "kinternet_press_releases.csv": "한국 인터넷 기업협회",
        "bkl_newsletters.csv": "법무법인 태평양",
        "yulchon_newsletters.csv": "법무법인 율촌"
    }

    final_message = ""
    for file_name, agency_name in agencies.items():
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            message = read_csv_and_format_message(file_path, agency_name)
            final_message += f"{message}\n"

    # 최종 메시지 전송
    if final_message:
        notifier.send_message(final_message)
    else:
        print("No messages to send.")


if __name__ == "__main__":
    main()
