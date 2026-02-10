"""Kakao Geocoding API 테스트"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

KAKAO_API_KEY = "1c40a7e4cd2e0187852872f40b41c698"

def test_geocoding(address):
    """주소를 위경도로 변환"""
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
                addr_name = doc.get("address_name", "")
                
                print(f"✅ 성공: {address}")
                print(f"   → {addr_name}")
                print(f"   → 위도: {lat}, 경도: {lon}\n")
                return (lat, lon)
            else:
                print(f"❌ 결과 없음: {address}\n")
                return None
    
    except Exception as e:
        print(f"❌ 오류: {address}")
        print(f"   → {e}\n")
        return None


# 테스트 주소들
test_addresses = [
    "성남시 성남대로331번길 8",
    "경기도 성남시 분당구 정자동",
    "서울특별시 강남구 테헤란로 152",
    "부산광역시 해운대구 우동",
    "제주특별자치도 제주시 첨단로 242",
]

print("=== Kakao Geocoding API 테스트 ===\n")

for addr in test_addresses:
    test_geocoding(addr)
