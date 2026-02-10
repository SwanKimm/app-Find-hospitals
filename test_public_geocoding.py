"""공공데이터 Geocoding API 테스트"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# 이미 사용 중인 공공데이터 API 키
SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"

def test_geocoding(address):
    """주소로 병원 검색 후 첫 번째 병원의 좌표 사용"""
    url = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"
    
    # 주소에서 시/구 추출
    parts = address.split()
    sido = parts[0] if len(parts) > 0 else ""
    sigungu = parts[1] if len(parts) > 1 else ""
    
    params = {
        "serviceKey": SERVICE_KEY,
        "Q0": sido,
        "Q1": sigungu,
        "pageNo": "1",
        "numOfRows": "1",
        "_type": "json"
    }
    
    try:
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        with urllib.request.urlopen(full_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data["response"]["header"]["resultCode"] == "00":
                body = data["response"]["body"]
                if body.get("totalCount", 0) > 0:
                    items = body["items"]["item"]
                    if isinstance(items, list):
                        item = items[0]
                    else:
                        item = items
                    
                    lat = item.get("wgs84Lat")
                    lon = item.get("wgs84Lon")
                    name = item.get("dutyName")
                    
                    if lat and lon:
                        print(f"✅ 성공: {address}")
                        print(f"   → 참조 병원: {name}")
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
    "경기도 성남시",
    "서울특별시 강남구",
    "부산광역시 해운대구",
]

print("=== 공공데이터 API로 지역 좌표 추출 ===\n")

for addr in test_addresses:
    test_geocoding(addr)
