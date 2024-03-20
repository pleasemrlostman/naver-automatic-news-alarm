import re
from bs4 import BeautifulSoup
def remove_html_tags(text):
    if "<" in text and ">" in text:  # HTML 마크업인지 확인
        # HTML 태그 제거
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()

        # HTML 엔티티 제거
        text = re.sub(r"&quot;", "", text)

    return text

