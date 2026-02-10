"""로컬 테스트용 스크립트"""
import json
from lambda_function import lambda_handler

def test_hospital_search():
    """병원 검색 테스트"""
    
    # 슬랙 요청 시뮬레이션
    event = {
        "body": "text=경기도 성남시 분당구 정자동 이비인후과"
    }
    
    context = {}
    
    # Lambda 함수 실행
    response = lambda_handler(event, context)
    
    print("Status Code:", response["statusCode"])
    print("\nResponse Body:")
    
    body = json.loads(response["body"])
    print(json.dumps(body, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print("=== 병원 찾기 앱 로컬 테스트 ===\n")
    test_hospital_search()
