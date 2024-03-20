import urllib.parse
import urllib.request



def search_naver_news(query, client_id, client_secret):
    client_id = client_id
    client_secret = client_secret
    encText = urllib.parse.quote(query)

    # URL 생성
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&sort=date&start=1&display=20"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)
        return None
