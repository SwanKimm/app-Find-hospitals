# 병원 찾기 슬랙 앱

슬랙 슬래시 커맨드를 통해 근처 병원을 검색하는 애플리케이션입니다.

## 기능

- 슬랙에서 `/병원` 명령어로 병원 검색
- 공공데이터포털 API를 활용한 실시간 병원 정보 제공
- AWS Lambda 서버리스 아키텍처

## 사용법

```
/병원 [장소] [진료과목]
```

### 예시

```
/병원 경기도 성남시 분당구 정자동 이비인후과
/병원 서울시 강남구 내과
/병원 부산시 해운대구 정형외과
```

## 지원 진료과목

내과, 소아청소년과, 신경과, 정신건강의학과, 피부과, 외과, 흉부외과, 정형외과, 신경외과, 성형외과, 산부인과, 안과, 이비인후과, 비뇨기과, 영상의학과, 방사선종양학과, 병리과, 진단검사의학과, 결핵과, 재활의학과, 핵의학과, 가정의학과, 응급의학과, 치과, 한의과

## AWS Lambda 배포

### 1. Lambda 함수 생성

1. AWS Lambda 콘솔에서 새 함수 생성
2. 런타임: Python 3.9 이상
3. `lambda_function.py` 코드 업로드

### 2. API Gateway 설정

1. API Gateway에서 REST API 생성
2. POST 메서드 추가
3. Lambda 함수와 연결
4. API 배포

### 3. 슬랙 앱 설정

1. https://api.slack.com/apps 에서 새 앱 생성
2. "Slash Commands" 메뉴에서 `/병원` 명령어 추가
3. Request URL에 API Gateway 엔드포인트 입력
4. 워크스페이스에 앱 설치

### 4. 환경 변수 (선택사항)

Lambda 함수에 환경 변수 설정:
- `SERVICE_KEY`: 공공데이터 API 인증키

## API 정보

- **엔드포인트**: https://apis.data.go.kr/B552657/HsptlAsembySearchService
- **서비스**: 병원정보서비스
- **인증키**: 89d895f43010a59cdcbc901e7aaf913724c1c0e874f4a3c0dc891fc73e927b28

## 로컬 테스트

```python
# test_local.py 실행
python test_local.py
```

## 주의사항

- 공공데이터 API 트래픽 제한 확인 필요
- Lambda 타임아웃 설정 권장: 10초
- API 응답 시간에 따라 슬랙 3초 제한 고려
