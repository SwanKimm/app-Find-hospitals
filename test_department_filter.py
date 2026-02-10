"""진료과목 필터링 확인 테스트"""
import urllib.request
import urllib.parse
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"
API_ENDPOINT = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"

# 테스트: 성남시 피부과 검색
print("=== 진료과목 필터링 테스트 ===\n")
print("검색: 성남시 피부과 (D005)")

params = {
    "serviceKey": SERVICE_KEY,
    "Q0": "경기도",
    "Q1": "성남시",
    "QD": "D005",  # 피부과
    "pageNo": "1",
    "numOfRows": "20",
    "_type": "json"
}

url = f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        total = data["response"]["body"].get("totalCount", 0)
        print(f"\n총 검색 결과: {total}개\n")
        
        if total > 0:
            items = data["response"]["body"]["items"]["item"]
            if not isinstance(items, list):
                items = [items]
            
            print("검색된 병원 목록 (진료과목 확인):")
            print("-" * 80)
            
            for idx, item in enumerate(items[:10], 1):
                name = item.get("dutyName", "N/A")
                addr = item.get("dutyAddr", "N/A")
                
                # 피부과 관련 키워드 확인
                is_derma = any(keyword in name for keyword in ["피부", "피부과", "성형", "미용"])
                marker = "✅" if is_derma else "❓"
                
                print(f"{marker} {idx}. {name}")
                print(f"   주소: {addr[:50]}...")
                print()
                
except Exception as e:
    print(f"오류: {e}")

# 테스트 2: 이비인후과
print("\n" + "="*80)
print("\n검색: 성남시 이비인후과 (D013)")

params["QD"] = "D013"  # 이비인후과

url = f"{API_ENDPOINT}?{urllib.parse.urlencode(params)}"

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        total = data["response"]["body"].get("totalCount", 0)
        print(f"\n총 검색 결과: {total}개\n")
        
        if total > 0:
            items = data["response"]["body"]["items"]["item"]
            if not isinstance(items, list):
                items = [items]
            
            print("검색된 병원 목록 (진료과목 확인):")
            print("-" * 80)
            
            for idx, item in enumerate(items[:10], 1):
                name = item.get("dutyName", "N/A")
                addr = item.get("dutyAddr", "N/A")
                
                # 이비인후과 관련 키워드 확인
                is_ent = any(keyword in name for keyword in ["이비인후과", "ENT"])
                marker = "✅" if is_ent else "❓"
                
                print(f"{marker} {idx}. {name}")
                print(f"   주소: {addr[:50]}...")
                print()
                
except Exception as e:
    print(f"오류: {e}")
