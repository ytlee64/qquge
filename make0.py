import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_gguge_thumbnail(
    input_path="image.png",
    output_path="thumbnail_16_9.png",
    target_width=1920,
    target_height=1080
):
    """
    꾸그(Gguge) 파이썬 맛보기 클래스용 16:9 고화질 썸네일 자동 생성기
    - 비율: 16:9 (1920x1080)
    - 레이아웃: 우측 상단 텍스트 배치 (좌측 아이의 표정과 노트북 그래픽을 100% 살림)
    """
    if not os.path.exists(input_path):
        print(f"❌ '{input_path}' 파일이 없습니다. 같은 폴더에 사진을 두고 이름을 image.png로 바꿔주세요.")
        return

    # 1. 원본 이미지 열기
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    # 2. 16:9 비율로 크롭(Crop) 및 리사이즈
    target_ratio = target_width / target_height  # 16 / 9
    img_ratio = w / h

    if img_ratio > target_ratio:
        # 가로가 더 긴 경우: 좌우를 자름
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img_cropped = img.crop((offset, 0, offset + new_w, h))
    else:
        # 세로가 더 긴 경우: 상단 아이 얼굴과 화면을 살리기 위해 위쪽 중심 크롭
        new_h = int(w / target_ratio)
        offset = int((h - new_h) * 0.25)
        img_cropped = img.crop((0, offset, w, offset + new_h))

    # 1920x1080 고화질로 리사이즈
    base = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # 3. 오버레이 드로잉 레이어 생성
    overlay = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 4. 한글 폰트 자동 탐색 (Windows / Mac / Linux)
    font_candidates = [
        # Windows
        "C:/Windows/Fonts/malgunbd.ttf",   # 맑은 고딕 굵게
        "C:/Windows/Fonts/malgun.ttf",     # 맑은 고딕
        "C:/Windows/Fonts/NanumGothicBold.ttf",
        # Mac
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/NanumGothicBold.ttf",
        # Linux
        "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    ]
    
    font_path = None
    for path in font_candidates:
        if os.path.exists(path):
            font_path = path
            break

    if font_path:
        font_badge = ImageFont.truetype(font_path, 32)
        font_sub = ImageFont.truetype(font_path, 38)
        font_main = ImageFont.truetype(font_path, 58)
        font_callout = ImageFont.truetype(font_path, 36)
    else:
        print("⚠️ 한글 시스템 폰트를 찾지 못해 기본 폰트로 대체합니다.")
        font_badge = font_sub = font_main = font_callout = ImageFont.load_default()

    # --- [우측 상단 시작 X좌표 기준점] ---
    RIGHT_X = 1040

    # 뱃지 드로잉 헬퍼
    def draw_badge(x, y, text, bg_color, text_color):
        bbox = draw.textbbox((x, y), text, font=font_badge)
        pad_x, pad_y = 16, 9
        rect = [bbox[0] - pad_x, bbox[1] - pad_y, bbox[2] + pad_x, bbox[3] + pad_y]
        draw.rounded_rectangle(rect, radius=12, fill=bg_color)
        draw.text((x, y), text, font=font_badge, fill=text_color)
        return rect[2]  # 오른쪽 끝 좌표 반환

    # --- [우측 상단 뱃지 4개] ---
    badge1_end = draw_badge(RIGHT_X, 70, "★ 5.0 만점 후기", (245, 158, 11, 235), (255, 255, 255, 255))
    draw_badge(badge1_end + 18, 70, "원격 1:1 설치 지원", (14, 165, 233, 235), (255, 255, 255, 255))
    
    badge3_end = draw_badge(RIGHT_X, 140, "초3~중1 추천", (99, 102, 241, 235), (255, 255, 255, 255))
    draw_badge(badge3_end + 18, 140, "10,000원 체험", (16, 185, 129, 235), (255, 255, 255, 255))

    # --- [우측 메인 타이틀 배경 소프트 박스] ---
    title_box = [RIGHT_X - 25, 215, 1860, 440]
    draw.rounded_rectangle(title_box, radius=20, fill=(255, 255, 255, 225))

    # 서브 카피
    draw.text((RIGHT_X, 240), "단 40분 만에 끝내는!", font=font_sub, fill=(79, 70, 229, 255))

    # 메인 카피
    draw.text((RIGHT_X, 310), "파이썬 첫걸음 & 거북이 그림", font=font_main, fill=(15, 23, 42, 255))

    # --- [하단 말풍선 뱃지] ---
    quote_text = '"엄마, 코딩이 이렇게 재밌는 거였어?!"'
    q_bbox = draw.textbbox((RIGHT_X, 475), quote_text, font=font_callout)
    q_rect = [q_bbox[0] - 18, q_bbox[1] - 10, q_bbox[2] + 18, q_bbox[3] + 10]
    draw.rounded_rectangle(q_rect, radius=14, fill=(15, 23, 42, 215))
    draw.text((RIGHT_X, 475), quote_text, font=font_callout, fill=(254, 240, 138, 255))

    # 5. 합성 및 저장
    final_img = Image.alpha_composite(base, overlay).convert("RGB")
    final_img.save(output_path, quality=95)
    print(f"🎉 축하합니다! 우측 상단 텍스트 배치 썸네일 생성 완료: {output_path}")

if __name__ == "__main__":
    create_gguge_thumbnail()
