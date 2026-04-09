<div align="center">

# 🚀 Filly AI Analysis Server

**BLIP (Bootstrapping Language-Image Pre-training)** 모델을 사용하여 이미지에서 객관적인 **상황(Caption)**과 감성적인 **분위기(Mood)**를 추출하는 AI 작업 서버입니다. 
<br/>
Spring Boot 백엔드 서버와 협력하여 사용자의 사진을 분석하고, 일기 생성을 위한 핵심 메타데이터를 제공합니다.

</div>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
</p>

---

## 🛠 Tech Stack

- **Framework**: `FastAPI`
- **AI Model**: `Salesforce/blip-image-captioning-base` (via Hugging Face)
- **Libraries**: `PyTorch`, `Transformers`, `Pillow`
- **Container**: Docker (`Python 3.12-slim` base)

---

## 📦 Getting Started (Docker)

팀 프로젝트의 환경 일관성을 위해 **도커(Docker) 빌드 및 컨테이너 실행을 권장**합니다. 
로컬에 파이썬이나 관련 의존성 라이브러리를 직접 설치할 필요 없이 빠르게 서버를 띄울 수 있습니다.

### 1. 이미지 빌드

```bash
docker build -t filly-fastapi-server .
```

### 2. 컨테이너 실행

포트 `8000` 번을 사용하여 컨테이너를 백그라운드에서 실행합니다.

```bash
docker run -d -p 8000:8000 --name filly-ai-container filly-fastapi-server
```

> [!TIP]
> **서버 상태 확인하기**
> 
> 브라우저에서 [http://localhost:8000/docs](http://localhost:8000/docs) 에 접속하여 **Swagger UI**가 정상적으로 뜨는지 확인해 보세요!

---

## 🔌 API Specification

### **이미지 분석 (Core Analysis)**

이미지를 서버로 전송하면 AI가 분석한 **캡션**과 **분위기** 데이터를 반환합니다.

- **URL**: `/analyze-core`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`

#### Request Body
| Key | Type | Description |
| :--- | :---: | :--- |
| `file` | `File` | 분석할 이미지 파일 (JPG, PNG 등) |

#### Response Example
```json
{
  "status": "success",
  "data": {
    "caption": "a person sitting at a cafe with a laptop",
    "mood": "peaceful and focused"
  }
}
```

---

## 📂 Project Structure

```text
filly-fastapi/
├── main.py              # FastAPI 엔트리 포인트 및 API 로직
├── Dockerfile           # 도커 빌드 레시피 (Python 3.12 기반)
├── requirements.txt     # 프로젝트에 필요한 패키지 목록
└── ...
```

---

## ⚠️ Troubleshooting

> [!WARNING]
> **1. 8000 포트 충돌 시**
> <br/>
> 이미 8000 포트를 다른 프로세스에서 사용 중이라면, 컨테이너 실행 시 로컬 포트를 변경하여 실행하세요.
> ```bash
> docker run -d -p 8001:8000 --name filly-ai-container filly-fastapi-server
> ```

> [!NOTE]
> **2. 이미지 빌드 에러 (`libgl1` 관련)**
> <br/>
> 일부 환경에서 OpenCV / Pillow 라이브러리 구동에 필요한 시스템 라이브러리(`libgl1`) 문제가 발생할 수 있으나, 현재 프로젝트의 `Dockerfile`은 apt-get을 통해 이 문제를 해결한 버전입니다.

> [!IMPORTANT]
> **3. 모델 로딩 속도 지연**
> <br/>
> 컨테이너를 처음 구동하고 **첫 번째 요청**을 보낼 때, 모델 가중치를 메모리에 로드하는 과정에서 약 10~20초 정도의 지연 시간이 발생할 수 있습니다. 이는 정상적인 로딩 절차입니다. (이후 요청부터는 바로 처리됩니다.)

---

## 🤝 Project Info

- 👤 **Maintainer**: 재모 (Hansung Univ. Web Eng & AI)
- 🎯 **Goal**: 하이퍼로컬 지식 브릿지 및 개인 맞춤형 페르소나 아카이빙 서비스 _'Pebble'_ 지원