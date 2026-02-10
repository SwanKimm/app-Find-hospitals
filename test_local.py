"""로컬 테스트용 스크립트"""
import json
from lambda_function import lambda_handler

def test_hospital_search():
    """병원 검색 테스트"""
    
    # 테스트 케이스들
    test_cases = [
        "성남시 성남대로331번길 8 이비인후과",
        "성남시 성남대로331번길 8 피부과",
        "성남시 성남대로331번길 8 내과",
    ]
    
    for text in test_cases:
        print(f"\n{'='*70}")
        print(f"테스트: {text}")
        print('='*70)
        
        # 슬랙 요청 시뮬레이션
        event = {
            "body": f"text={text}"
        }
        
        context = {}
        
        # Lambda 함수 실행
        response = lambda_handler(event, context)
        
        print("Status Code:", response["statusCode"])
        
        body = json.loads(response["body"])
        
        # 결과 전체 출력
        if "attachments" in body and body["attachments"]:
            result_text = body["attachments"][0]["text"]
            lines = result_text.split('\n')
            
            # 첫 줄 (검색 결과 개수)
            print(lines[0])
            print()
            
            # 모든 병원 출력 (10개)
            for line in lines[2:]:
                if line.strip():  # 빈 줄이 아니면
                    print(line)


if __name__ == "__main__":
    print("=== 병원 찾기 앱 로컬 테스트 ===")
    print("검색 위치: 성남시 성남대로331번길 8\n")
    test_hospital_search()
