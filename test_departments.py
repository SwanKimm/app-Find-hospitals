"""다양한 진료과목 테스트"""
from lambda_function import lambda_handler
import json

test_cases = [
    "경기도 성남시 분당구 정자동 이비인후과",
    "경기도 성남시 분당구 정자동 내과",
    "경기도 성남시 분당구 정자동 정형외과",
    "서울특별시 강남구 치과",
]

for text in test_cases:
    print(f"\n{'='*60}")
    print(f"테스트: {text}")
    print('='*60)
    
    event = {"body": f"text={text}"}
    response = lambda_handler(event, {})
    
    body = json.loads(response["body"])
    
    # 결과 요약
    if "attachments" in body and body["attachments"]:
        result_text = body["attachments"][0]["text"]
        lines = result_text.split('\n')
        
        # 첫 줄 (검색 결과 개수)
        print(lines[0])
        
        # 병원 이름만 추출 (최대 3개)
        count = 0
        for line in lines[2:]:
            if line.startswith('*') and '.' in line:
                print(line)
                count += 1
                if count >= 3:
                    break

