# 1. 파이썬 환경 설정 (가벼운 slim 버전 사용)
FROM python:3.10-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 라이브러리 설치에 필요한 패키지 미리 설치
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# 4. 라이브러리 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 모든 소스 코드와 모델 파일 복사
COPY . .

# 6. FastAPI 서버 실행 (8000포트)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]