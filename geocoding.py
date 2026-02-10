"""주소를 위경도로 변환하는 Geocoding 모듈"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Kakao REST API 키 (무료, 하루 300,000건)
# 발급: https://developers.kakao.com/
KAKAO_API_KEY = "YOUR_KAKAO_API_KEY"  # 사용자가 발급받아야 함


def address_to_coords_kakao(address: str) -> tuple:
    """
    Kakao Map API를 사용하여 주소를 위경도로 변환
    
    Args:
        address: 주소 문자열 (예: "경기도 성남시 분당구 정자동")
    
    Returns:
        (latitude, longitude) 튜플, 실패시 (None, None)
    """
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    
    request = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("documents"):
                doc = data["documents"][0]
                lon = float(doc["x"])
                lat = float(doc["y"])
                return (lat, lon)
            
            return (None, None)
    
    except Exception as e:
        print(f"Geocoding 오류: {e}")
        return (None, None)


def address_to_coords_simple(address: str) -> tuple:
    """
    간단한 주소 매칭 (API 없이 사용)
    주요 지역의 대표 좌표를 반환
    
    Args:
        address: 주소 문자열
    
    Returns:
        (latitude, longitude) 튜플
    """
    # 주요 지역 좌표 데이터베이스
    LOCATION_DB = {
        # 서울
        "강남구": (37.5172, 127.0473),
        "서초구": (37.4837, 127.0324),
        "송파구": (37.5145, 127.1059),
        "강동구": (37.5301, 127.1238),
        "종로구": (37.5735, 126.9792),
        "중구": (37.5641, 126.9979),
        "용산구": (37.5326, 126.9905),
        "성동구": (37.5634, 127.0368),
        "광진구": (37.5384, 127.0822),
        "동대문구": (37.5744, 127.0396),
        "중랑구": (37.6063, 127.0925),
        "성북구": (37.5894, 127.0167),
        "강북구": (37.6396, 127.0257),
        "도봉구": (37.6688, 127.0471),
        "노원구": (37.6542, 127.0568),
        "은평구": (37.6027, 126.9291),
        "서대문구": (37.5791, 126.9368),
        "마포구": (37.5663, 126.9019),
        "양천구": (37.5170, 126.8664),
        "강서구": (37.5509, 126.8495),
        "구로구": (37.4954, 126.8874),
        "금천구": (37.4519, 126.9020),
        "영등포구": (37.5264, 126.8962),
        "동작구": (37.5124, 126.9393),
        "관악구": (37.4784, 126.9516),
        
        # 경기도
        "수원시": (37.2636, 127.0286),
        "성남시": (37.4201, 127.1262),
        "분당구": (37.3595, 127.1088),
        "수정구": (37.4500, 127.1469),
        "중원구": (37.4370, 127.1547),
        "용인시": (37.2410, 127.1776),
        "안양시": (37.3943, 126.9568),
        "부천시": (37.5034, 126.7660),
        "광명시": (37.4786, 126.8644),
        "평택시": (36.9921, 127.1129),
        "안산시": (37.3219, 126.8309),
        "고양시": (37.6584, 126.8320),
        "과천시": (37.4292, 127.0137),
        "구리시": (37.5943, 127.1296),
        "남양주시": (37.6361, 127.2168),
        "의정부시": (37.7381, 127.0338),
        
        # 인천
        "인천": (37.4563, 126.7052),
        "남동구": (37.4475, 126.7314),
        "연수구": (37.4106, 126.6784),
        "부평구": (37.5069, 126.7219),
        
        # 기타 주요 도시
        "대전": (36.3504, 127.3845),
        "대구": (35.8714, 128.6014),
        "부산": (35.1796, 129.0756),
        "광주": (35.1595, 126.8526),
        "울산": (35.5384, 129.3114),
        "세종": (36.4800, 127.2890),
    }
    
    # 주소에서 구/시 찾기
    for location, coords in LOCATION_DB.items():
        if location in address:
            return coords
    
    # 기본값: 서울시청
    return (37.5665, 126.9780)


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    두 좌표 간의 거리 계산 (Haversine formula)
    
    Returns:
        거리 (km)
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # 지구 반지름 (km)
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c


# 테스트
if __name__ == "__main__":
    test_addresses = [
        "경기도 성남시 분당구 정자동",
        "서울특별시 강남구",
        "경기도 수원시",
    ]
    
    print("=== 주소 → 위경도 변환 테스트 ===\n")
    for addr in test_addresses:
        lat, lon = address_to_coords_simple(addr)
        print(f"{addr}")
        print(f"  → 위도: {lat}, 경도: {lon}\n")
