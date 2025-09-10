import time
from typing import Dict, List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from app.models.quote import Quote


class QuoteScraper:
    """Selenium을 사용한 명언 스크래핑 클래스"""

    def __init__(self, headless: bool = True):
        self.base_url = "https://quotes.toscrape.com"
        self.driver = None
        self.headless = headless
        self.wait = None

    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")  # 브라우저 창 숨기기

        # 추가 옵션들 (안정성을 위해)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        # ChromeDriver 자동 설치 및 설정
        service = Service(ChromeDriverManager().install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)  # 최대 10초 대기

        print("✅ Chrome 드라이버가 설정되었습니다.")

    def close_driver(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print("✅ Chrome 드라이버가 종료되었습니다.")

    def __enter__(self):
        """컨텍스트 매니저 진입"""
        self.setup_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close_driver()

    def parse_quotes_from_page(self) -> List[Dict[str, str]]:
        """현재 페이지에서 명언 파싱"""
        quotes = []

        try:
            # 명언 요소들이 로드될 때까지 대기
            quote_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.quote"))
            )

            print(f"📄 페이지에서 {len(quote_elements)}개의 명언 요소를 찾았습니다.")

            for quote_element in quote_elements:
                try:
                    # 명언 텍스트 추출
                    text_element = quote_element.find_element(By.CSS_SELECTOR, "span.text")
                    quote_text = text_element.text.strip().strip('"')

                    # 작가 추출
                    author_element = quote_element.find_element(By.CSS_SELECTOR, "small.author")
                    author = author_element.text.strip()

                    # 태그 추출 (선택사항)
                    try:
                        tag_elements = quote_element.find_elements(
                            By.CSS_SELECTOR, "div.tags a.tag"
                        )
                        tags = [tag.text.strip() for tag in tag_elements]
                    except NoSuchElementException:
                        tags = []

                    if quote_text and author:
                        quotes.append({"content": quote_text, "author": author, "tags": tags})
                        print(f"✅ 명언 파싱: {author} - {quote_text[:50]}...")

                except NoSuchElementException as e:
                    print(f"⚠️ 명언 요소 파싱 실패: {e}")
                    continue

        except TimeoutException:
            print("❌ 페이지 로딩 타임아웃 - 명언 요소를 찾을 수 없습니다.")
        except Exception as e:
            print(f"❌ 페이지 파싱 중 오류 발생: {e}")

        return quotes

    def scrape_quotes(self, max_pages: int = 5) -> List[Dict[str, str]]:
        """명언 스크래핑 실행"""
        all_quotes = []

        for page_num in range(1, max_pages + 1):
            try:
                url = f"{self.base_url}/page/{page_num}/"
                print(f"\n📖 페이지 {page_num} 접속 중: {url}")

                # 페이지 이동
                self.driver.get(url)

                # 페이지 로딩 대기
                time.sleep(2)

                # 현재 페이지에서 명언 추출
                quotes = self.parse_quotes_from_page()

                if not quotes:  # 더 이상 명언이 없으면 종료
                    print(f"✅ 페이지 {page_num}에서 명언을 찾을 수 없어 스크래핑을 종료합니다.")
                    break

                all_quotes.extend(quotes)
                print(f"✅ 페이지 {page_num}에서 {len(quotes)}개의 명언을 수집했습니다.")

                # 다음 페이지 버튼 확인
                try:
                    next_btn = self.driver.find_element(By.CSS_SELECTOR, "li.next a")
                    if not next_btn:
                        print("✅ 다음 페이지가 없어 스크래핑을 종료합니다.")
                        break
                except NoSuchElementException:
                    print("✅ 다음 페이지 버튼을 찾을 수 없어 스크래핑을 종료합니다.")
                    break

                # 서버 부하 방지를 위한 지연
                time.sleep(1)

            except Exception as e:
                print(f"❌ 페이지 {page_num} 스크래핑 실패: {e}")
                continue

        print(f"\n🎉 총 {len(all_quotes)}개의 명언을 스크래핑했습니다!")
        return all_quotes

    async def save_quotes_to_db(self, quotes: List[Dict[str, str]]) -> int:
        """명언을 데이터베이스에 저장"""
        saved_count = 0

        for quote_data in quotes:
            try:
                # 중복 체크 (내용과 작가가 같은 명언)
                existing_quote = await Quote.filter(
                    content=quote_data["content"], author=quote_data["author"]
                ).first()

                if not existing_quote:
                    await Quote.create(content=quote_data["content"], author=quote_data["author"])
                    saved_count += 1
                    print(f"✅ 명언 저장: {quote_data['author']} - {quote_data['content'][:50]}...")
                else:
                    print(f"⏭️ 중복 명언 건너뜀: {quote_data['author']}")

            except Exception as e:
                print(f"❌ 명언 저장 실패: {e}")
                continue

        return saved_count
