import json
import urllib.parse
import urllib.request
import ssl
import os
from typing import Dict, List, Any
from math import radians, sin, cos, sqrt, atan2

# SSL 인증서 검증 비활성화 (개발 환경용)
ssl._create_default_https_context = ssl._create_unverified_context

# Kakao API 키 (환경변수 또는 직접 설정)
os.environ['KAKAO_API_KEY'] = '1c40a7e4cd2e0187852872f40b41c698'

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
    """
    주소를 위경도로 변환
    1. Kakao Geocoding API 시도
    2. 실패 시 간단한 매칭 사용
    """
    
    # 환경변수에서 Kakao API 키 가져오기
    kakao_key = os.environ.get('KAKAO_API_KEY', '')
    
    if kakao_key:
        # Kakao Geocoding API 사용
        try:
            url = "https://dapi.kakao.com/v2/local/search/address.json"
            params = {"query": address}
            
            request = urllib.request.Request(
                f"{url}?{urllib.parse.urlencode(params)}",
                headers={"Authorization": f"KakaoAK {kakao_key}"}
            )
            
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get("documents"):
                    doc = data["documents"][0]
                    lon = float(doc["x"])
                    lat = float(doc["y"])
                    print(f"Kakao Geocoding: {address} → ({lat}, {lon})")
                    return (lat, lon)
        except Exception as e:
            print(f"Kakao API 오류, 간단한 매칭 사용: {e}")
    
    # Kakao API 실패 시 또는 키가 없으면 간단한 매칭 사용
    LOCATION_DB = {
        "강남구": (37.5172, 127.0473), "서초구": (37.4837, 127.0324),
        "송파구": (37.5145, 127.1059), "성남시": (37.4201, 127.1262),
        "분당구": (37.3595, 127.1088), "수원시": (37.2636, 127.0286),
        "인천": (37.4563, 126.7052), "대전": (36.3504, 127.3845),
        "대구": (35.8714, 128.6014), "부산": (35.1796, 129.0756),
    }
    
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
    
    # 시/도 이름 정규화 (서울시 → 서울특별시)
    sido_map = {
        "서울시": "서울특별시",
        "서울": "서울특별시",
        "부산시": "부산광역시",
        "부산": "부산광역시",
        "대구시": "대구광역시",
        "대구": "대구광역시",
        "인천시": "인천광역시",
        "인천": "인천광역시",
        "광주시": "광주광역시",
        "광주": "광주광역시",
        "대전시": "대전광역시",
        "대전": "대전광역시",
        "울산시": "울산광역시",
        "울산": "울산광역시",
    }
    
    sido = sido_map.get(sido, sido)
    
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
