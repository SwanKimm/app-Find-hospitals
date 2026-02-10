"""위치 기반 병원 검색 API 테스트"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"

# 위치정보 조회 API
LOCATION_API = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncLcinfoInqire"

# 경기도 성남시 분당구 정자동 좌표
# 정자역 좌표: 위도 37.3595, 경도 127.1088
LAT = 37.3595
LON = 127.1088

print("=== 위치 기반 병원 검색 테스트 ===")
print(f"검색 위치: 위도 {LAT}, 경도 {LON} (정자동)")

# 테스트 1: 위경도만으로 검색
print("\n[테스트 1] 위경도만으로 검색")
params = {
    "serviceKey": SERVICE_KEY,
    "WGS84_LON": str(LON),
    "WGS84_LAT": str(LAT),
    "pageNo": "1",
    "numOfRows": "10",
    "_type": "json"
}

url = f"{LOCATION_API}?{urllib.parse.urlencode(params)}"
print(f"요청 URL: {url[:150]}...")

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        result_code = data["response"]["header"]["resultCode"]
        result_msg = data["response"]["header"]["resultMsg"]
        print(f"응답: {result_code} - {result_msg}")
        
        body = data["response"]["body"]
        total = body.get("totalCount", 0)
        print(f"검색 결과: {total}개")
        
        if total > 0:
            items = body["items"]["item"]
            if not isinstance(items, list):
                items = [items]
            
            print(f"\n가까운 병원 {len(items)}개:")
            for idx, item in enumerate(items[:5], 1):
                name = item.get("dutyName", "N/A")
                addr = item.get("dutyAddr", "N/A")
                tel = item.get("dutyTel1", "N/A")
                lat = item.get("wgs84Lat", 0)
                lon = item.get("wgs84Lon", 0)
                
                # 거리 계산 (간단한 유클리드 거리)
                distance = ((lat - LAT)**2 + (lon - LON)**2)**0.5 * 111  # 대략 km
                
                print(f"\n{idx}. {name}")
                print(f"   주소: {addr}")
                print(f"   전화: {tel}")
                print(f"   거리: 약 {distance:.2f}km")
                
except Exception as e:
    print(f"오류: {e}")

# 테스트 2: 위경도 + 진료과목
print("\n\n[테스트 2] 위경도 + 이비인후과")
params = {
    "serviceKey": SERVICE_KEY,
    "WGS84_LON": str(LON),
    "WGS84_LAT": str(LAT),
    "QD": "D013",  # 이비인후과
    "pageNo": "1",
    "numOfRows": "10",
    "_type": "json"
}

url = f"{LOCATION_API}?{urllib.parse.urlencode(params)}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        result_code = data["response"]["header"]["resultCode"]
        print(f"응답: {result_code}")
        
        body = data["response"]["body"]
        total = body.get("totalCount", 0)
        print(f"이비인후과 검색 결과: {total}개")
        
        if total > 0:
            items = body["items"]["item"]
            if not isinstance(items, list):
                items = [items]
            
            print(f"\n가까운 이비인후과 {len(items)}개:")
            for idx, item in enumerate(items[:3], 1):
                name = item.get("dutyName", "N/A")
                addr = item.get("dutyAddr", "N/A")
                print(f"{idx}. {name} - {addr}")
                
except Exception as e:
    print(f"오류: {e}")
