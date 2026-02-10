"""Vworld Geocoding API 테스트 (공공데이터, 무료)"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Vworld API 키 (무료, 신청: https://www.vworld.kr/dev/v4dv_geocoderguide2_s001.do)
# 임시로 공개 키 사용 (실제로는 발급받아야 함)
VWORLD_API_KEY = "CEB6176B-D7DC-35EB-9C1B-65E1B1AB59DE"  # 예시 키

def test_geocoding(address):
    """주소를 위경도로 변환"""
    url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "version": "2.0",
        "crs": "epsg:4326",
        "address": address,
        "format": "json",
        "type": "parcel",
        "key": VWORLD_API_KEY
    }
    
    try:
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("response", {}).get("status") == "OK":
                result = data["response"]["result"]
                if result and "point" in result:
                    lon = float(result["point"]["x"])
                    lat = float(result["point"]["y"])
                    
                    print(f"✅ 성공: {address}")
                    print(f"   → 위도: {lat}, 경도: {lon}\n")
                    return (lat, lon)
            
            print(f"❌ 결과 없음: {address}\n")
            return None
    
    except Exception as e:
        print(f"❌ 오류: {address}")
        print(f"   → {e}\n")
        return None


# 테스트 주소들
test_addresses = [
    "경기도 성남시 분당구 성남대로331번길 8",
    "경기도 성남시 분당구 정자동",
    "서울특별시 강남구 테헤란로 152",
]

print("=== Vworld Geocoding API 테스트 ===\n")

for addr in test_addresses:
    test_geocoding(addr)
