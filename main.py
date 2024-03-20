import time

import pandas as pd

from get_naver_api_credentials import get_naver_api_credentials
from keywords import keywords
from parse_naver_news_response import parse_naver_news_response
from search_naver_news import search_naver_news
from send_email import send_email


def main():
    client_id, client_secret = get_naver_api_credentials()

    previous_merged_df = None  # 이전에 저장된 merged_df

    while True:
        dfs = []  # DataFrame을 저장할 리스트 생성
        for keyword in keywords:
            query_with_seoul = keyword + " 서울"
            response = search_naver_news(query_with_seoul, client_id, client_secret)
            if response:
                df = parse_naver_news_response(response)
                print(df)
                dfs.append(df)
            else:
                print(f"Failed to retrieve data from Naver API for the query '{keyword}'.")

        # 생성된 DataFrame이 있을 때만 합치기
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)  # 생성된 모든 DataFrame을 하나로 합침
            # title column에서 첫 글자부터 10번째 글자까지가 동일한 행 제거
            merged_df['title_prefix'] = merged_df['title'].str.slice(stop=10)  # title의 첫 10글자를 새로운 열에 저장
            merged_df.drop_duplicates(subset='title_prefix', keep='first', inplace=True)  # title_prefix 기준으로 중복된 행 제거

            # 중복 제거 후 필요없는 열 제거
            merged_df.drop(columns=['title_prefix'], inplace=True)

            if previous_merged_df is not None:
                # 이전 실행의 첫 번째 행과 현재 실행의 첫 번째 행의 'title' 값을 비교
                previous_first_title = previous_merged_df.iloc[0]['title']
                current_first_title = merged_df.iloc[0]['title']

                if previous_first_title == current_first_title:
                    print("데이터가 변경된게 없습니다.")
                else:
                    # 현재 실행의 첫 번째 행의 'title' 값이 이전 실행에서 어떤 행에 위치하는지 확인
                    found_index = merged_df[merged_df['title'] == previous_first_title].index
                    if len(found_index) > 0:
                        # 현재 실행된 merged_df에서 이전 실행의 첫 번째 행의 'title' 값과 동일한 행부터 첫 번째 행까지 필터링하여 새로운 DataFrame 만들기
                        filtered_df = merged_df.loc[found_index[0]:0]
                        print("필터링된 DataFrame:")
                        print(filtered_df)

                        # 필터링된 DataFrame을 CSV 파일로 저장
                        csv_filename = "filtered_dataframe.csv"
                        filtered_df.to_csv(csv_filename, index=False)

                        # CSV 파일을 메일로 전송
                        send_email(csv_filename)

                    else:
                        print("이전 실행에서 현재 실행의 첫 번째 행의 title을 찾을 수 없습니다.")
            previous_merged_df = merged_df.copy()  # 현재 merged_df를 previous_merged_df에 저장


            # print(merged_df)  # 이 부분에 필요한 추가 작업을 수행할 수 있습니다.
            if previous_merged_df is not None:
                merged_df.to_csv('merged_data.csv', index=False)  # index=False로 설정하여 인덱스를 CSV에 포함하지 않음
                previous_merged_df.to_csv('previous_merged_df.csv', index=False)  # index=False로 설정하여 인덱스를 CSV에 포함하지 않음





        time.sleep(10)  # 1시간(3600초) 동안 대기합니다.
if __name__ == "__main__":
    main()