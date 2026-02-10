"""Kakao API 디버깅"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

KAKAO_API_KEY = "1c40a7e4cd2e0187852872f40b41c698"

def test_kakao_api():
    """Kakao API 상세 디버깅"""
    
    address = "서울특별시 강남구"
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    
    print("=== Kakao API 디버깅 ===\n")
    print(f"1. API 키: {KAKAO_API_KEY}")
    print(f"2. 요청 URL: {full_url}")
    print(f"3. Authorization 헤더: KakaoAK {KAKAO_API_KEY}\n")
    
    # 요청 생성
    request = urllib.request.Request(
        full_url,
        headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    )
    
    print("4. 요청 헤더:")
    for key, value in request.headers.items():
        print(f"   {key}: {value}")
    print()
    
    try:
        print("5. API 호출 중...\n")
        with urllib.request.urlopen(request) as response:
            print(f"✅ 성공! 상태 코드: {response.status}")
            data = json.loads(response.read().decode('utf-8'))
            print(f"응답 데이터:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 오류 발생!")
        print(f"   상태 코드: {e.code}")
        print(f"   이유: {e.reason}")
        print(f"\n   응답 본문:")
        try:
            error_body = e.read().decode('utf-8')
            print(f"   {error_body}")
            
            # JSON 파싱 시도
            try:
                error_json = json.loads(error_body)
                print(f"\n   파싱된 오류:")
                print(json.dumps(error_json, indent=2, ensure_ascii=False))
            except:
                pass
        except:
            print("   (응답 본문 읽기 실패)")
            
    except Exception as e:
        print(f"❌ 기타 오류: {e}")


if __name__ == "__main__":
    test_kakao_api()
