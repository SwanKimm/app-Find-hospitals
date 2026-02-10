#!/bin/bash

# AWS Lambda 배포 스크립트

echo "🚀 Lambda 함수 배포 시작..."

# 함수 이름 설정
FUNCTION_NAME="hospital-finder-slack-app"
REGION="ap-northeast-2"  # 서울 리전

# ZIP 파일 생성 (lambda_deploy.py를 lambda_function.py로 복사)
echo "📦 배포 패키지 생성 중..."
cp lambda_deploy.py lambda_function.py
zip function.zip lambda_function.py

# Lambda 함수 업데이트 (이미 생성된 경우)
echo "⬆️  Lambda 함수 업데이트 중..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://function.zip \
    --region $REGION

# 또는 새로 생성하는 경우 (주석 해제하여 사용)
# aws lambda create-function \
#     --function-name $FUNCTION_NAME \
#     --runtime python3.9 \
#     --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
#     --handler lambda_function.lambda_handler \
#     --zip-file fileb://function.zip \
#     --timeout 10 \
#     --region $REGION

echo "✅ 배포 완료!"

# 정리
rm lambda_function.py
rm function.zip

echo ""
echo "📝 다음 단계:"
echo "1. AWS Lambda 콘솔에서 함수 확인"
echo "2. API Gateway 설정"
echo "3. Slack 앱에 API Gateway URL 연결"
