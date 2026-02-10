"""
공공데이터 병원정보 API 엔드포인트 정리

기본 URL: https://apis.data.go.kr/B552657/HsptlAsembySearchService
"""

# 1. 병‧의원 목록정보 조회
# 용도: 시도/시군구/진료요일/기관별/진료과목별로 조회
ENDPOINT_LIST = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncListInfoInqire"
# 파라미터: QZ(시도), Q1(시군구), QD(진료과목), QT(진료시간), pageNo, numOfRows

# 2. 병‧의원 위치정보 조회 ⭐ 추천
# 용도: 경도/위도 기반 반경 내 병원 검색
ENDPOINT_LOCATION = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncLcinfoInqire"
# 파라미터: WGS84_LON(경도), WGS84_LAT(위도), pageNo, numOfRows

# 3. 병‧의원별 기본정보 조회
# 용도: 특정 병원의 상세정보 조회 (병원 ID로 검색)
ENDPOINT_DETAIL = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlBassInfoInqire"
# 파라미터: HPID(병원ID)

# 4. 달빛어린이병원 및 소아전문센터 목록정보 조회
# 용도: 달빛어린이병원 전용
ENDPOINT_BABY_LIST = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyListInfoInqire"
# 파라미터: Q0(주소), Q1(진료과목), QT(진료요일)

# 5. 달빛어린이병원 위치정보 조회
# 용도: 위/경도 기반 달빛어린이병원 검색
ENDPOINT_BABY_LOCATION = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getBabyLcinfoInqire"
# 파라미터: WGS84_LON(경도), WGS84_LAT(위도)

# 6. 병/의원 FullData 내려받기
# 용도: 전체 병의원 정보 다운로드
ENDPOINT_FULLDATA = "https://apis.data.go.kr/B552657/HsptlAsembySearchService/getHsptlMdcncFullDown"
# 파라미터: pageNo, numOfRows


# 사용 예시
def example_usage():
    """각 엔드포인트 사용 예시"""
    
    SERVICE_KEY = "89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28"
    
    # 예시 1: 목록정보 조회 (시도/시군구로 검색)
    url1 = f"{ENDPOINT_LIST}?serviceKey={SERVICE_KEY}&QZ=서울특별시&Q1=강남구&pageNo=1&numOfRows=10&_type=json"
    
    # 예시 2: 위치정보 조회 (위경도로 검색) ⭐ 가장 유용
    # 경기도 성남시 분당구 정자동 좌표: 위도 37.3595, 경도 127.1088
    url2 = f"{ENDPOINT_LOCATION}?serviceKey={SERVICE_KEY}&WGS84_LON=127.1088&WGS84_LAT=37.3595&pageNo=1&numOfRows=10&_type=json"
    
    # 예시 3: 병원 상세정보 조회 (병원ID로 검색)
    url3 = f"{ENDPOINT_DETAIL}?serviceKey={SERVICE_KEY}&HPID=A1200015&_type=json"
    
    # 예시 4: 전체 데이터 다운로드
    url4 = f"{ENDPOINT_FULLDATA}?serviceKey={SERVICE_KEY}&pageNo=1&numOfRows=1000&_type=json"
    
    return {
        "목록조회": url1,
        "위치조회": url2,
        "상세조회": url3,
        "전체다운": url4
    }


# 추천 방식
"""
슬랙 앱에서는 ENDPOINT_LOCATION (위치정보 조회)를 사용하는 것이 가장 좋습니다.

이유:
1. 주소 텍스트를 위경도로 변환 (Geocoding)
2. 위경도 기반으로 반경 내 병원 검색
3. 거리순으로 정렬된 결과 제공

필요한 추가 작업:
- 주소 → 위경도 변환: Kakao Map API, Google Geocoding API 등 사용
"""
