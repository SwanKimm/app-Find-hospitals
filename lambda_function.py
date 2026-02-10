import json
import urllib.parse
import urllib.request
import ssl
import os
from typing import Dict, List, Any
from math import radians, sin, cos, sqrt, atan2

# SSL 인증서 검증 비활성화 (개발 환경용)
ssl._create_default_https_context = ssl._create_unverified_context

# 공공데이터 API 설정
API_ENDPOINT = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"
API_ENDPOINT_LOCATION = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncLcinfoInqire"
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


def address_to_coords(address: str) -> tuple:
    """주소를 위경도로 변환 (간단한 매칭)"""
    
    # 도로명 주소 패턴 감지 (번길, 로, 대로 등)
    is_road_address = any(keyword in address for keyword in ["로", "길", "대로"])
    
    LOCATION_DB = {
        # 동 단위 (우선순위 높음)
        "정자동": (37.3595, 127.1088), "서현동": (37.3836, 127.1234),
        "야탑동": (37.4119, 127.1281), "이매동": (37.3897, 127.1289),
        "판교동": (37.3948, 127.1114), "삼평동": (37.4021, 127.1076),
        "수내동": (37.3833, 127.1019), "구미동": (37.3500, 127.1100),
        "금곡동": (37.3500, 127.1100),
        # 서울 구
        "강남구": (37.5172, 127.0473), "서초구": (37.4837, 127.0324),
        "송파구": (37.5145, 127.1059), "강동구": (37.5301, 127.1238),
        "종로구": (37.5735, 126.9792), "중구": (37.5641, 126.9979),
        "용산구": (37.5326, 126.9905), "성동구": (37.5634, 127.0368),
        "광진구": (37.5384, 127.0822), "동대문구": (37.5744, 127.0396),
        "중랑구": (37.6063, 127.0925), "성북구": (37.5894, 127.0167),
        "강북구": (37.6396, 127.0257), "도봉구": (37.6688, 127.0471),
        "노원구": (37.6542, 127.0568), "은평구": (37.6027, 126.9291),
        "서대문구": (37.5791, 126.9368), "마포구": (37.5663, 126.9019),
        "양천구": (37.5170, 126.8664), "강서구": (37.5509, 126.8495),
        "구로구": (37.4954, 126.8874), "금천구": (37.4519, 126.9020),
        "영등포구": (37.5264, 126.8962), "동작구": (37.5124, 126.9393),
        "관악구": (37.4784, 126.9516),
        # 경기도
        "분당구": (37.3595, 127.1088), "수정구": (37.4500, 127.1469),
        "중원구": (37.4370, 127.1547),
        "수원시": (37.2636, 127.0286), "성남시": (37.4201, 127.1262),
        "용인시": (37.2410, 127.1776), "안양시": (37.3943, 126.9568),
        "부천시": (37.5034, 126.7660), "광명시": (37.4786, 126.8644),
        "평택시": (36.9921, 127.1129), "안산시": (37.3219, 126.8309),
        "고양시": (37.6584, 126.8320), "과천시": (37.4292, 127.0137),
        "구리시": (37.5943, 127.1296), "남양주시": (37.6361, 127.2168),
        "의정부시": (37.7381, 127.0338),
        # 인천
        "인천": (37.4563, 126.7052), "남동구": (37.4475, 126.7314),
        "연수구": (37.4106, 126.6784), "부평구": (37.5069, 126.7219),
        # 기타
        "대전": (36.3504, 127.3845), "대구": (35.8714, 128.6014),
        "부산": (35.1796, 129.0756), "광주": (35.1595, 126.8526),
        "울산": (35.5384, 129.3114), "세종": (36.4800, 127.2890),
        # 주요 도로명 (대략적인 중심 좌표)
        "성남대로": (37.4201, 127.1262),
        "정자일로": (37.3595, 127.1088),
        "내정로": (37.3595, 127.1088),
    }
    
    # 도로명 주소인 경우
    if is_road_address:
        # 도로명에서 키워드 추출
        for road_name in ["성남대로", "정자일로", "내정로"]:
            if road_name in address:
                # 도로명 좌표 반환
                if road_name in LOCATION_DB:
                    return LOCATION_DB[road_name]
        
        # 도로명을 찾지 못하면 시/구로 검색
        for location, coords in LOCATION_DB.items():
            if location in address and location.endswith(("시", "구")):
                return coords
    
    # 일반 주소: 가장 구체적인 위치부터 찾기 (동이 우선)
    # 주소를 역순으로 검색 (뒤에서부터 = 더 구체적)
    address_parts = address.split()
    for part in reversed(address_parts):
        for location, coords in LOCATION_DB.items():
            if location in part or part in location:
                return coords
    
    # 전체 주소에서 찾기
    for location, coords in LOCATION_DB.items():
        if location in address:
            return coords
    
    return (37.5665, 126.9780)  # 기본값: 서울시청


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """두 좌표 간의 거리 계산 (km)"""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def search_hospitals(location: str, department: str) -> List[Dict[str, Any]]:
    """병원 검색 API 호출 - 목록 API로 진료과목 필터 + 거리 계산"""
    
    # 진료과목 코드 찾기
    dept_code = DEPARTMENT_MAP.get(department)
    if not dept_code:
        print(f"진료과목 '{department}'를 찾을 수 없습니다.")
        return []
    
    # 주소를 위경도로 변환
    lat, lon = address_to_coords(location)
    print(f"검색 위치: {location} → 위도 {lat}, 경도 {lon}")
    
    # 주소를 시/도와 시/군/구로 분리
    location_parts = location.split()
    sido = location_parts[0] if len(location_parts) > 0 else ""
    sigungu = location_parts[1] if len(location_parts) > 1 else ""
    
    # 목록 API로 진료과목 필터링 (많이 가져오기)
    params = {
        "serviceKey": SERVICE_KEY,
        "Q0": sido,  # 주소(시도)
        "Q1": sigungu,  # 주소(시군구)
        "QD": dept_code,  # 진료과목
        "pageNo": "1",
        "numOfRows": "100",  # 많이 가져와서 거리 계산
        "_type": "json"
    }
    
    url = f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"
    print(f"API 호출: 목록 검색 (진료과목 필터)")
    
    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode('utf-8')
            data = json.loads(response_text)
            
            if isinstance(data, dict) and "response" in data:
                header = data["response"].get("header", {})
                result_code = header.get("resultCode")
                
                if result_code != "00":
                    print(f"API 오류: {header.get('resultMsg')}")
                    return []
                
                body = data["response"].get("body", {})
                total_count = body.get("totalCount", 0)
                print(f"진료과목 필터 결과: {total_count}개")
                
                items = body.get("items", "")
                
                if isinstance(items, str) and items == "":
                    return []
                
                if isinstance(items, dict) and "item" in items:
                    item_data = items["item"]
                    
                    if isinstance(item_data, dict):
                        all_hospitals = [item_data]
                    elif isinstance(item_data, list):
                        all_hospitals = item_data
                    else:
                        return []
                    
                    # 거리 계산 및 정렬
                    for hospital in all_hospitals:
                        # 위경도 필드명
                        h_lat = hospital.get("wgs84Lat", 0)
                        h_lon = hospital.get("wgs84Lon", 0)
                        
                        if h_lat and h_lon:
                            distance = calculate_distance(lat, lon, float(h_lat), float(h_lon))
                            hospital["distance"] = distance
                        else:
                            hospital["distance"] = 999  # 좌표 없으면 멀리
                    
                    # 진료과목으로 필터링 (병원 이름 기반)
                    # API의 QD 파라미터가 제대로 작동하지 않아서 추가 필터링 필요
                    dept_filtered = []
                    for hospital in all_hospitals:
                        name = hospital.get("dutyName", "")
                        
                        # 진료과목이 병원 이름에 포함되어 있는지 확인
                        if department in name:
                            dept_filtered.append(hospital)
                    
                    # 필터링된 결과가 없으면 전체 사용 (종합병원 등)
                    if dept_filtered:
                        all_hospitals = dept_filtered
                        print(f"진료과목 이름 필터링: {len(all_hospitals)}개")
                    
                    # 거리순 정렬
                    all_hospitals.sort(key=lambda x: x.get("distance", 999))
                    
                    # 가까운 병원만 (10km 이내)
                    filtered = [h for h in all_hospitals if h.get("distance", 999) <= 10]
                    
                    print(f"10km 이내 병원: {len(filtered)}개")
                    return filtered[:10]
            
            return []
    
    except Exception as e:
        print(f"API 호출 오류: {str(e)}")
        return []


def format_hospital_info(hospitals: List[Dict[str, Any]]) -> str:
    """병원 정보를 슬랙 메시지 형식으로 변환"""
    
    if not hospitals:
        return "검색 결과가 없습니다. 장소나 진료과목을 확인해주세요."
    
    message = f"🏥 *검색 결과: {len(hospitals)}개 병원 (거리순)*\n\n"
    
    for idx, hospital in enumerate(hospitals[:5], 1):  # 최대 5개만 표시
        name = hospital.get("dutyName", hospital.get("dutyEmcls", "정보 없음"))
        addr = hospital.get("dutyAddr", hospital.get("dutyMapimg", "주소 정보 없음"))
        tel = hospital.get("dutyTel1", hospital.get("dutyTel3", "전화번호 없음"))
        distance = hospital.get("distance", 0)
        
        message += f"*{idx}. {name}*\n"
        message += f"📍 주소: {addr}\n"
        message += f"📞 전화: {tel}\n"
        message += f"🚶 거리: 약 {distance:.2f}km\n\n"
    
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
