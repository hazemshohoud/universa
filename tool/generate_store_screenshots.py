import os
from PIL import Image, ImageDraw, ImageFont

SCREEN_DIR = r"D:\flutter\universa-app-main\screens"
IPHONE_DIR = os.path.join(SCREEN_DIR, "iphone")
IPAD_DIR = os.path.join(SCREEN_DIR, "ipad")

os.makedirs(IPHONE_DIR, exist_ok=True)
os.makedirs(IPAD_DIR, exist_ok=True)

# Fonts
FONT_REGULAR = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
if not os.path.exists(FONT_BOLD):
    FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
if not os.path.exists(FONT_REGULAR):
    FONT_REGULAR = r"C:\Windows\Fonts\arial.ttf"

def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size)

def clean_source_image(file_key, img):
    w, h = img.size
    img = img.copy()
    
    # 1. If video screen, remove floating Android toolbar at left (starts with 9725)
    if file_key.startswith("9725"):
        patch = img.crop((0, 270, 32, 350)).resize((32, 145))
        img.paste(patch, (0, 110))
    
    # 2. Crop out old non-iOS status bar (top 44px) and old bottom line (bottom 20px)
    content_top = 44
    content_bottom = 980
    
    cropped = img.crop((0, content_top, w, content_bottom))
    return cropped

def draw_iphone_status_bar(canvas):
    draw = ImageDraw.Draw(canvas, 'RGBA')
    W = 1179
    
    # 1. Dynamic Island
    island_w = 372
    island_h = 104
    island_x = (W - island_w) // 2
    island_y = 35
    island_r = island_h // 2
    
    # Subtle rim glow
    draw.rounded_rectangle(
        [island_x - 1, island_y - 1, island_x + island_w + 1, island_y + island_h + 1],
        radius=island_r + 1,
        fill=(25, 25, 32, 160)
    )
    # Island pill (True Black)
    draw.rounded_rectangle(
        [island_x, island_y, island_x + island_w, island_y + island_h],
        radius=island_r,
        fill=(0, 0, 0, 255)
    )
    # Camera lens reflection
    cam_x = island_x + island_w - 55
    cam_y = island_y + island_h // 2
    draw.ellipse([cam_x - 14, cam_y - 14, cam_x + 14, cam_y + 14], fill=(12, 15, 25, 255))
    draw.ellipse([cam_x - 7, cam_y - 7, cam_x + 7, cam_y + 7], fill=(22, 28, 45, 255))
    draw.ellipse([cam_x - 3, cam_y - 3, cam_x + 3, cam_y + 3], fill=(8, 10, 18, 255))

    # 2. Time: 9:41
    time_font = get_font(46, bold=True)
    draw.text((112, 63), "9:41", font=time_font, fill=(255, 255, 255, 255))

    # 3. Cellular Signal Bars
    cell_x = W - 285
    cell_base_y = 104
    bar_w = 6.5
    bar_gap = 4.5
    bar_heights = [12, 19, 26, 33]
    for i, bh in enumerate(bar_heights):
        bx = cell_x + i * (bar_w + bar_gap)
        by = cell_base_y - bh
        draw.rounded_rectangle([bx, by, bx + bar_w, cell_base_y], radius=3, fill=(255, 255, 255, 255))

    # 4. Wi-Fi Icon
    wifi_center_x = W - 215
    wifi_center_y = 92
    draw.ellipse([wifi_center_x - 3.5, wifi_center_y + 6, wifi_center_x + 3.5, wifi_center_y + 13], fill=(255, 255, 255, 255))
    draw.arc([wifi_center_x - 13, wifi_center_y - 3, wifi_center_x + 13, wifi_center_y + 23], start=215, end=325, fill=(255, 255, 255, 255), width=4)
    draw.arc([wifi_center_x - 22, wifi_center_y - 12, wifi_center_x + 22, wifi_center_y + 32], start=215, end=325, fill=(255, 255, 255, 255), width=4)
    draw.arc([wifi_center_x - 31, wifi_center_y - 21, wifi_center_x + 31, wifi_center_y + 41], start=215, end=325, fill=(255, 255, 255, 255), width=4)

    # 5. Battery Icon
    batt_x = W - 145
    batt_y = 73
    batt_w = 75
    batt_h = 36
    batt_r = 10
    draw.rounded_rectangle([batt_x, batt_y, batt_x + batt_w, batt_y + batt_h], radius=batt_r, outline=(255, 255, 255, 120), width=3)
    draw.rounded_rectangle([batt_x + batt_w + 1, batt_y + 11, batt_x + batt_w + 5, batt_y + batt_h - 11], radius=2, fill=(255, 255, 255, 120))
    draw.rounded_rectangle([batt_x + 5, batt_y + 5, batt_x + batt_w - 5, batt_y + batt_h - 5], radius=6, fill=(255, 255, 255, 255))

def draw_iphone_home_indicator(canvas):
    draw = ImageDraw.Draw(canvas, 'RGBA')
    W, H = canvas.size
    bar_w = 420
    bar_h = 14
    bar_r = 7
    bar_x = (W - bar_w) // 2
    bar_y = H - 30
    draw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=bar_r, fill=(255, 255, 255, 210))

def draw_ipad_status_bar(canvas):
    draw = ImageDraw.Draw(canvas, 'RGBA')
    W = 2048
    
    # 1. Left side: Authentic iPad Date and Time
    font_ipad = get_font(42, bold=True)
    draw.text((55, 36), "09:41  Wed 21 Oct", font=font_ipad, fill=(255, 255, 255, 255))
    
    # 2. Right side: Wi-Fi Icon
    wifi_center_x = W - 235
    wifi_center_y = 57
    draw.ellipse([wifi_center_x - 4, wifi_center_y + 8, wifi_center_x + 4, wifi_center_y + 16], fill=(255, 255, 255, 255))
    draw.arc([wifi_center_x - 16, wifi_center_y - 3, wifi_center_x + 16, wifi_center_y + 29], start=215, end=325, fill=(255, 255, 255, 255), width=5)
    draw.arc([wifi_center_x - 27, wifi_center_y - 14, wifi_center_x + 27, wifi_center_y + 40], start=215, end=325, fill=(255, 255, 255, 255), width=5)
    draw.arc([wifi_center_x - 38, wifi_center_y - 25, wifi_center_x + 38, wifi_center_y + 51], start=215, end=325, fill=(255, 255, 255, 255), width=5)

    # 3. Right side: Official Green Battery Capsule with percentage (100% or 92%)
    batt_x = W - 165
    batt_y = 38
    batt_w = 110
    batt_h = 44
    batt_r = 22
    
    # Green capsule (Apple official battery green: #34C759)
    draw.rounded_rectangle([batt_x, batt_y, batt_x + batt_w, batt_y + batt_h], radius=batt_r, fill=(52, 199, 89, 255))
    # Terminal bump
    draw.rounded_rectangle([batt_x + batt_w + 1, batt_y + 14, batt_x + batt_w + 6, batt_y + batt_h - 14], radius=3, fill=(100, 100, 110, 255))
    
    # Battery text: 100% or 92%
    font_batt = get_font(28, bold=True)
    draw.text((batt_x + 18, batt_y + 4), "100", font=font_batt, fill=(255, 255, 255, 255))
    
    # Lightning bolt or percent symbol
    font_pct = get_font(20, bold=True)
    draw.text((batt_x + 68, batt_y + 9), "%", font=font_pct, fill=(255, 255, 255, 255))

def draw_ipad_home_indicator(canvas):
    draw = ImageDraw.Draw(canvas, 'RGBA')
    W, H = canvas.size
    ipad_bar_w = 620
    ipad_bar_h = 14
    ipad_bar_r = 7
    ipad_bar_x = (W - ipad_bar_w) // 2
    ipad_bar_y = H - 26
    draw.rounded_rectangle(
        [ipad_bar_x, ipad_bar_y, ipad_bar_x + ipad_bar_w, ipad_bar_y + ipad_bar_h],
        radius=ipad_bar_r,
        fill=(255, 255, 255, 210)
    )

def generate_iphone_screenshot(source_path, out_path):
    orig = Image.open(source_path).convert('RGB')
    filename = os.path.basename(source_path)
    cleaned = clean_source_image(filename, orig)
    
    TARGET_W = 1179
    TARGET_H = 2556
    STATUS_H = 140
    BOTTOM_H = 65
    CONTENT_H = TARGET_H - STATUS_H - BOTTOM_H
    
    scaled_content = cleaned.resize((TARGET_W, CONTENT_H), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (TARGET_W, TARGET_H))
    
    # Determine top background color
    if filename.startswith("eb75"):
        # Dark navy app background to prevent any red bleed
        top_color = (25, 26, 46)
    else:
        top_color = scaled_content.getpixel((TARGET_W // 2, 2))
        
    bottom_color = scaled_content.getpixel((TARGET_W // 2, CONTENT_H - 2))
    
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, TARGET_W, STATUS_H], fill=top_color)
    draw.rectangle([0, TARGET_H - BOTTOM_H, TARGET_W, TARGET_H], fill=bottom_color)
    
    canvas.paste(scaled_content, (0, STATUS_H))
    
    draw_iphone_status_bar(canvas)
    draw_iphone_home_indicator(canvas)
    
    canvas.save(out_path, format='PNG', optimize=True)
    print(f"Generated iPhone screenshot: {out_path} ({TARGET_W}x{TARGET_H})")

def generate_ipad_screenshot(source_path, out_path):
    orig = Image.open(source_path).convert('RGB')
    filename = os.path.basename(source_path)
    cleaned = clean_source_image(filename, orig)
    
    TARGET_W = 2048
    TARGET_H = 2732
    STATUS_H = 110
    BOTTOM_H = 60
    CONTENT_H = TARGET_H - STATUS_H - BOTTOM_H
    
    scaled_content = cleaned.resize((TARGET_W, CONTENT_H), Image.Resampling.LANCZOS)
    canvas = Image.new('RGB', (TARGET_W, TARGET_H))
    
    if filename.startswith("eb75"):
        top_color = (25, 26, 46)
    else:
        top_color = scaled_content.getpixel((TARGET_W // 2, 2))
        
    bottom_color = scaled_content.getpixel((TARGET_W // 2, CONTENT_H - 2))
    
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, TARGET_W, STATUS_H], fill=top_color)
    draw.rectangle([0, TARGET_H - BOTTOM_H, TARGET_W, TARGET_H], fill=bottom_color)
    
    canvas.paste(scaled_content, (0, STATUS_H))
    
    draw_ipad_status_bar(canvas)
    draw_ipad_home_indicator(canvas)
    
    canvas.save(out_path, format='PNG', optimize=True)
    print(f"Generated iPad screenshot: {out_path} ({TARGET_W}x{TARGET_H})")

def main():
    screens = [
        ("9a62d8fcf2272a5c98eda5455d9725da051ea867.png", "1_home.png"),
        ("eb7518628d26d826b34ccbecba1b9e514bb64495.png", "2_courses.png"),
        ("9725cf1aacb96d5b735bfa2b94f948b3f8fa62e1.png", "3_video.png"),
        ("93e1bd4510ec8b22d15f81e90783719c50943152.png", "4_offline.png"),
    ]
    
    print("Generating iPhone screenshots...")
    for src_file, out_file in screens:
        src_path = os.path.join(SCREEN_DIR, src_file)
        out_path = os.path.join(IPHONE_DIR, out_file)
        generate_iphone_screenshot(src_path, out_path)
        
    print("\nGenerating iPad screenshots...")
    for src_file, out_file in screens:
        src_path = os.path.join(SCREEN_DIR, src_file)
        out_path = os.path.join(IPAD_DIR, out_file)
        generate_ipad_screenshot(src_path, out_path)
        
    print("\nSUCCESS: All 4 iPhone and 4 iPad screenshots generated!")

if __name__ == "__main__":
    main()
