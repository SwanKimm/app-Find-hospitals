"""API 파라미터 테스트"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"
BASE_URL = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"

# 테스트 1: 진료과목 없이 시도만
print("=== 테스트 1: 경기도 전체 ===")
params = {
    "serviceKey": SERVICE_KEY,
    "QZ": "경기도",
    "pageNo": "1",
    "numOfRows": "5",
    "_type": "json"
}

url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        total = data["response"]["body"].get("totalCount", 0)
        print(f"결과: {total}개")
        if total > 0:
            print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"오류: {e}")

# 테스트 2: 서울 + 진료과목
print("\n=== 테스트 2: 서울 + 이비인후과 ===")
params = {
    "serviceKey": SERVICE_KEY,
    "QZ": "서울특별시",
    "QD": "13",
    "pageNo": "1",
    "numOfRows": "5",
    "_type": "json"
}

url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        total = data["response"]["body"].get("totalCount", 0)
        print(f"결과: {total}개")
        if total > 0:
            print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"오류: {e}")

# 테스트 3: 파라미터 없이
print("\n=== 테스트 3: 파라미터 없이 전체 조회 ===")
params = {
    "serviceKey": SERVICE_KEY,
    "pageNo": "1",
    "numOfRows": "5",
    "_type": "json"
}

url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        total = data["response"]["body"].get("totalCount", 0)
        print(f"결과: {total}개")
        if total > 0:
            items = data["response"]["body"]["items"]["item"]
            if isinstance(items, list):
                print(f"첫 번째 병원: {items[0].get('dutyName', 'N/A')}")
            else:
                print(f"병원: {items.get('dutyName', 'N/A')}")
except Exception as e:
    print(f"오류: {e}")
