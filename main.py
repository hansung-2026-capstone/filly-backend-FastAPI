from fastapi import FastAPI, UploadFile, File
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io

app = FastAPI()

# 1. BLIP 모델 및 프로세서 로드
# "base" 모델은 약 900MB 정도로 성능과 속도의 밸런스가 좋습니다.
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

@app.post("/blip-analyze")
async def blip_analyze(file: UploadFile = File(...)):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # 추출할 핵심 프롬프트 정의
    core_prompts = {
        "caption": "A picture of",
        "mood": "The emotional mood of this photo is"
    }
    
    analysis_results = {}

    with torch.no_grad():
        for key, prompt in core_prompts.items():
            # 이미지와 각 프롬프트를 결합하여 전처리
            inputs = processor(image, prompt, return_tensors="pt").to(device)
            # 결과 생성
            out = model.generate(**inputs, max_new_tokens=30)
            # 디코딩 후 결과 저장
            analysis_results[key] = processor.decode(out[0], skip_special_tokens=True)

    # Spring Boot로 보낼 최종 데이터
    return {
        "status": "success",
        "data": analysis_results # {"caption": "...", "mood": "..."}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)