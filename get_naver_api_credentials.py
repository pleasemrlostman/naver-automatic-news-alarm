def get_naver_api_credentials():
    # 클라이언트 ID와 시크릿을 입력 받는 함수
    client_id = input("네이버 API 클라이언트 ID를 입력하세요: ")
    client_secret = input("네이버 API 클라이언트 시크릿을 입력하세요: ")
    return client_id, client_secret