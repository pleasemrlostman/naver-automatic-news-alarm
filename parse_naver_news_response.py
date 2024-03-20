import json
import pandas as pd
from remove_html_tags import remove_html_tags
from datetime import datetime, timedelta

def parse_naver_news_response(response):
    news_data = json.loads(response)
    df = pd.DataFrame(news_data['items'])
    # 'pubDate' 열을 datetime 형식으로 변환
    df['pubDate'] = pd.to_datetime(df['pubDate']).dt.tz_localize(None)  # 타임존 정보를 제거
    # HTML 태그 제거
    df['title'] = df['title'].apply(remove_html_tags)
    df['description'] = df['description'].apply(remove_html_tags)  # description 열에서도 HTML 태그 제거

    # 현재 시간으로부터 한 시간 전의 데이터만 필터링
    one_hour_ago = datetime.now() - timedelta(hours=1)
    df_filtered = df[df['pubDate'] >= one_hour_ago]

    return df_filtered