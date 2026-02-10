"""API 파라미터 테스트 - 다양한 파라미터 조합"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"
BASE_URL = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"

# 전체 데이터에서 하나 가져와서 구조 확인
print("=== 데이터 구조 확인 ===")
params = {
    "serviceKey": SERVICE_KEY,
    "pageNo": "1",
    "numOfRows": "1",
    "_type": "json"
}

url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        item = data["response"]["body"]["items"]["item"]
        print(json.dumps(item, indent=2, ensure_ascii=False))
        print("\n사용 가능한 필드:")
        if isinstance(item, dict):
            for key in item.keys():
                print(f"  - {key}: {item[key]}")
except Exception as e:
    print(f"오류: {e}")
