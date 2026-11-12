import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_step3_banner(
    input_path="step3.png",
    output_path="step3_banner_16_9.png",
    target_width=1920,
    target_height=1080
):
    """
    꾸그 3단계(거북이 화가) 상세페이지용 16:9 고화질 배너 생성기
    - 거북이 캐릭터와 화면 속 무지개 만다라 그래픽을 100% 살리는 우측 상단 레이아웃
    """
    if not os.path.exists(input_path):
        print(f"❌ '{input_path}' 파일이 없습니다. 사진 이름을 step3.png로 바꿔서 같은 폴더에 넣어주세요.")
        return

    # 1. 원본 이미지 열기
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    # 2. 16:9 비율로 스마트 크롭 및 리사이즈
    target_ratio = target_width / target_height
    img_ratio = w / h

    if img_ratio > target_ratio:
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img_cropped = img.crop((offset, 0, offset + new_w, h))
    else:
        new_h = int(w / target_ratio)
        offset = int((h - new_h) * 0.25)
        img_cropped = img.crop((0, offset, w, offset + new_h))

    base = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # 3. 오버레이 레이어
    overlay = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 4. 한글 폰트 설정
    font_candidates = [
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/NanumGothicBold.ttf",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/NanumGothicBold.ttf",
    ]
    font_path = next((p for p in font_candidates if os.path.exists(p)), None)

    if font_path:
        font_badge = ImageFont.truetype(font_path, 32)
        font_sub = ImageFont.truetype(font_path, 36)
        font_main = ImageFont.truetype(font_path, 54)
        font_callout = ImageFont.truetype(font_path, 34)
    else:
        font_badge = font_sub = font_main = font_callout = ImageFont.load_default()

    # 우측 상단 기준 X좌표 (거북이 머리와 노트북을 완벽히 피하는 위치)
    RIGHT_X = 1120

    def draw_badge(x, y, text, bg_color, text_color):
        bbox = draw.textbbox((x, y), text, font=font_badge)
        pad_x, pad_y = 16, 9
        rect = [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y]
        draw.rounded_rectangle(rect, radius=12, fill=bg_color)
        draw.text((x, y), text, font=font_badge, fill=text_color)
        return rect[2]

    # --- [상단 뱃지 2개] ---
    b1_end = draw_badge(RIGHT_X, 80, "🐢 파이썬 터틀 그래픽", (16, 185, 129, 240), (255, 255, 255, 255))
    draw_badge(b1_end + 18, 80, "단 몇 줄의 코드로 완성!", (245, 158, 11, 240), (255, 255, 255, 255))

    # --- [우측 텍스트 소프트 박스] ---
    title_box = [RIGHT_X - 25, 150, 1860, 360]
    draw.rounded_rectangle(title_box, radius=20, fill=(255, 255, 255, 230))

    draw.text((RIGHT_X, 175), "화면 속 거북이가 내 명령대로 춤춰요!", font=font_sub, fill=(79, 70, 229, 255))
    draw.text((RIGHT_X, 235), "알록달록 신기한 도형 예술 🎨", font=font_main, fill=(15, 23, 42, 255))

    # --- [하단 말풍선] ---
    callout_text = '"아이들의 눈이 가장 반짝이는 하이라이트 시간!"'
    q_bbox = draw.textbbox((RIGHT_X, 395), callout_text, font=font_callout)
    q_rect = [q_bbox[0] - 18, q_bbox[1] - 10, q_bbox[2] + 18, q_bbox[3] + 10]
    draw.rounded_rectangle(q_rect, radius=14, fill=(15, 23, 42, 215))
    draw.text((RIGHT_X, 395), callout_text, font=font_callout, fill=(254, 240, 138, 255))

    # 5. 합성 및 저장
    final_img = Image.alpha_composite(base, overlay).convert("RGB")
    final_img.save(output_path, quality=95)
    print(f"🎉 3단계 거북이 화가 배너 생성 완료: {output_path}")

if __name__ == "__main__":
    create_step3_banner()