# AWS Lambda 배포 가이드

## 필요한 파일

**단 하나의 파일만 필요합니다:**
- `lambda_deploy.py` → Lambda에 `lambda_function.py`로 업로드

## 배포 방법

### 방법 1: AWS CLI 사용 (자동)

```bash
# 배포 스크립트 실행
chmod +x deploy.sh
./deploy.sh
```

### 방법 2: AWS 콘솔 사용 (수동)

1. **Lambda 함수 생성**
   - AWS Lambda 콘솔 접속
   - "함수 생성" 클릭
   - 함수 이름: `hospital-finder-slack-app`
   - 런타임: Python 3.9 이상
   - 실행 역할: 기본 Lambda 권한

2. **코드 업로드**
   ```bash
   # lambda_deploy.py를 lambda_function.py로 복사
   cp lambda_deploy.py lambda_function.py
   
   # ZIP 파일 생성
   zip function.zip lambda_function.py
   ```
   
   - Lambda 콘솔에서 "업로드" → "function.zip" 선택

3. **설정 조정**
   - 타임아웃: 10초
   - 메모리: 128MB (기본값)

4. **환경 변수 설정 (선택사항 - 정확한 주소 검색)**
   
   Kakao Map API를 사용하면 모든 주소를 정확하게 위경도로 변환할 수 있습니다.
   
   **Kakao API 키 발급:**
   1. https://developers.kakao.com/ 접속
   2. "내 애플리케이션" → "애플리케이션 추가하기"
   3. 앱 이름 입력 후 생성
   4. "REST API 키" 복사
   
   **Lambda 환경 변수 설정:**
   - 키: `KAKAO_API_KEY`
   - 값: 발급받은 REST API 키
   
   **주의:** Kakao API 키가 없어도 작동하지만, 주요 지역만 지원됩니다.

## API Gateway 설정

1. **REST API 생성**
   - API Gateway 콘솔 접속
   - "REST API" 생성
   - API 이름: `hospital-finder-api`

2. **리소스 및 메서드 추가**
   - 리소스 생성: `/slack`
   - POST 메서드 추가
   - 통합 유형: Lambda 함수
   - Lambda 함수: `hospital-finder-slack-app` 선택

3. **API 배포**
   - "배포" 클릭
   - 스테이지 이름: `prod`
   - 배포 URL 복사 (예: `https://xxxxx.execute-api.ap-northeast-2.amazonaws.com/prod/slack`)

## Slack 앱 설정

1. **Slack 앱 생성**
   - https://api.slack.com/apps 접속
   - "Create New App" 클릭
   - "From scratch" 선택
   - App Name: `병원 찾기`
   - Workspace 선택

2. **Slash Command 추가**
   - "Slash Commands" 메뉴
   - "Create New Command" 클릭
   - Command: `/병원`
   - Request URL: API Gateway URL 입력
   - Short Description: `근처 병원 찾기`
   - Usage Hint: `[장소] [진료과목]`

3. **앱 설치**
   - "Install App" 메뉴
   - "Install to Workspace" 클릭
   - 권한 승인

## 테스트

Slack에서 다음과 같이 테스트:

```
/병원 성남시 성남대로331번길 8 이비인후과
/병원 경기도 성남시 분당구 정자동 피부과
/병원 서울특별시 강남구 내과
```

## 문제 해결

### Lambda 타임아웃
- Lambda 설정에서 타임아웃을 10초로 증가

### Slack 3초 제한
- API 응답이 3초 이상 걸리면 Slack이 타임아웃
- 해결: Lambda에서 즉시 응답 후 비동기로 메시지 전송 (고급)

### SSL 인증서 오류
- Lambda 환경에서는 보통 발생하지 않음
- 발생 시: `ssl._create_default_https_context = ssl._create_unverified_context` 이미 포함됨

## 비용

- **Lambda**: 월 100만 요청까지 무료
- **API Gateway**: 월 100만 요청까지 무료
- **공공데이터 API**: 무료 (일일 트래픽 제한 있음)

## 모니터링

- CloudWatch Logs에서 Lambda 로그 확인
- 오류 발생 시 로그에서 원인 파악

## 업데이트

코드 수정 후:

```bash
./deploy.sh
```

또는 AWS 콘솔에서 새 ZIP 파일 업로드
