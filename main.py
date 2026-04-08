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

@app.post("/generate-caption")
async def generate_caption(file: UploadFile = File(...)):
    # 이미지 읽기
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert("RGB")

    # BLIP 전처리
    inputs = processor(image, return_tensors="pt").to(device)

    # 캡션 생성 (이미지를 설명하는 문장 생성)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(out[0], skip_special_tokens=True)

    return {
        "filename": file.filename,
        "caption": caption  # 예: "a cat sitting on a wooden table"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)