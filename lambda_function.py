import json
import urllib.parse
import urllib.request
import ssl
import os
from typing import Dict, List, Any

# SSL 인증서 검증 비활성화 (개발 환경용)
ssl._create_default_https_context = ssl._create_unverified_context

# 공공데이터 API 설정
API_ENDPOINT = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"
SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"

# 진료과목 매핑 (CODE_MST의 'D000' 참조)
DEPARTMENT_MAP = {
    "내과": "D001",
    "소아청소년과": "D002",
    "신경과": "D003",
    "정신건강의학과": "D004",
    "피부과": "D005",
    "외과": "D006",
    "흉부외과": "D007",
    "정형외과": "D008",
    "신경외과": "D009",
    "성형외과": "D010",
    "산부인과": "D011",
    "안과": "D012",
    "이비인후과": "D013",
    "비뇨기과": "D014",
    "영상의학과": "D015",
    "방사선종양학과": "D016",
    "병리과": "D017",
    "진단검사의학과": "D018",
    "결핵과": "D019",
    "재활의학과": "D020",
    "핵의학과": "D021",
    "가정의학과": "D022",
    "응급의학과": "D023",
    "치과": "D024",
    "한의과": "D025"
}


def parse_slack_command(text: str) -> Dict[str, str]:
    """슬랙 명령어 파싱"""
    parts = text.strip().split()
    
    if len(parts) < 2:
        return {"error": "사용법: /병원 [장소] [진료과목]\n예시: /병원 경기도 성남시 분당구 정자동 이비인후과"}
    
    # 마지막 단어를 진료과목으로 간주
    department = parts[-1]
    location = " ".join(parts[:-1])
    
    return {
        "location": location,
        "department": department
    }


def search_hospitals(location: str, department: str) -> List[Dict[str, Any]]:
    """병원 검색 API 호출"""
    
    # 진료과목 코드 찾기
    dept_code = DEPARTMENT_MAP.get(department)
    if not dept_code:
        print(f"진료과목 '{department}'를 찾을 수 없습니다.")
        return []
    
    # 주소를 시/도와 시/군/구로 분리
    location_parts = location.split()
    sido = location_parts[0] if len(location_parts) > 0 else ""
    sigungu = location_parts[1] if len(location_parts) > 1 else ""
    
    # 올바른 파라미터 설정
    params = {
        "serviceKey": SERVICE_KEY,
        "Q0": sido,  # 주소(시도)
        "Q1": sigungu,  # 주소(시군구)
        "QD": dept_code,  # 진료과목
        "pageNo": "1",
        "numOfRows": "10",
        "_type": "json"
    }
    
    url = f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"
    print(f"요청 URL: {url}")
    print(f"파라미터: Q0(시도)={sido}, Q1(시군구)={sigungu}, QD(진료과목)={dept_code}")
    
    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode('utf-8')
            print(f"API 응답: {response_text[:1000]}")
            
            data = json.loads(response_text)
            
            # 에러 체크
            if isinstance(data, dict) and "response" in data:
                header = data["response"].get("header", {})
                result_code = header.get("resultCode")
                result_msg = header.get("resultMsg")
                
                print(f"응답 코드: {result_code}, 메시지: {result_msg}")
                
                if result_code != "00":
                    print(f"API 오류: {result_msg}")
                    return []
                
                body = data["response"].get("body", {})
                total_count = body.get("totalCount", 0)
                print(f"총 검색 결과: {total_count}개")
                
                items = body.get("items", "")
                
                # items가 빈 문자열인 경우
                if isinstance(items, str) and items == "":
                    print("검색 결과 없음")
                    return []
                
                # items.item 구조 확인
                if isinstance(items, dict) and "item" in items:
                    item_data = items["item"]
                    
                    # 단일 결과인 경우 리스트로 변환
                    if isinstance(item_data, dict):
                        return [item_data]
                    elif isinstance(item_data, list):
                        return item_data
            
            return []
    
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {str(e)}")
        return []
    except Exception as e:
        print(f"API 호출 오류: {str(e)}")
        return []


def format_hospital_info(hospitals: List[Dict[str, Any]]) -> str:
    """병원 정보를 슬랙 메시지 형식으로 변환"""
    
    if not hospitals:
        return "검색 결과가 없습니다. 장소나 진료과목을 확인해주세요."
    
    message = f"🏥 *검색 결과: {len(hospitals)}개 병원*\n\n"
    
    for idx, hospital in enumerate(hospitals[:5], 1):  # 최대 5개만 표시
        name = hospital.get("dutyName", hospital.get("dutyEmcls", "정보 없음"))
        addr = hospital.get("dutyAddr", hospital.get("dutyMapimg", "주소 정보 없음"))
        tel = hospital.get("dutyTel1", hospital.get("dutyTel3", "전화번호 없음"))
        
        message += f"*{idx}. {name}*\n"
        message += f"📍 주소: {addr}\n"
        message += f"📞 전화: {tel}\n\n"
    
    return message


def lambda_handler(event, context):
    """AWS Lambda 핸들러"""
    
    try:
        # Slack 요청 파싱
        body = event.get("body", "")
        
        # URL 인코딩된 데이터 파싱
        if isinstance(body, str):
            params = urllib.parse.parse_qs(body)
            text = params.get("text", [""])[0]
        else:
            text = ""
        
        # 명령어 파싱
        parsed = parse_slack_command(text)
        
        if "error" in parsed:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "response_type": "ephemeral",
                    "text": parsed["error"]
                })
            }
        
        location = parsed["location"]
        department = parsed["department"]
        
        # 병원 검색
        hospitals = search_hospitals(location, department)
        
        # 결과 포맷팅
        message = format_hospital_info(hospitals)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response_type": "in_channel",
                "text": f"🔍 *{location}* 지역의 *{department}* 검색 결과",
                "attachments": [{
                    "text": message,
                    "color": "#36a64f"
                }]
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response_type": "ephemeral",
                "text": f"오류가 발생했습니다: {str(e)}"
            })
        }
