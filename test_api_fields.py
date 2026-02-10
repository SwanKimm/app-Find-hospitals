"""API 응답 필드 확인"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"
API_ENDPOINT = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"

params = {
    "serviceKey": SERVICE_KEY,
    "Q0": "경기도",
    "Q1": "성남시",
    "QD": "D013",  # 이비인후과
    "pageNo": "1",
    "numOfRows": "1",
    "_type": "json"
}

url = f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data["response"]["body"].get("totalCount", 0) > 0:
            item = data["response"]["body"]["items"]["item"]
            if isinstance(item, list):
                item = item[0]
            
            print("=== API 응답 필드 전체 ===\n")
            print(json.dumps(item, indent=2, ensure_ascii=False))
            
            print("\n\n=== 진료과목 관련 필드 찾기 ===")
            for key, value in item.items():
                if any(keyword in key.lower() for keyword in ["duty", "dept", "subject", "dgsbj"]):
                    print(f"{key}: {value}")
                    
except Exception as e:
    print(f"오류: {e}")
