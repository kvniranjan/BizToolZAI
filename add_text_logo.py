from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

img = Image.open("videos/images/logo_v3_hourglass.jpg").convert("RGBA")
W, H = img.size

# Add canvas padding at the bottom for text
bottom_bar_height = int(H * 0.18)
new_img = Image.new("RGBA", (W, H + bottom_bar_height), (0, 0, 0, 255))
new_img.paste(img, (0, 0))

draw = ImageDraw.Draw(new_img)

# Gradient dark bar at bottom
for i in range(bottom_bar_height):
    alpha = int(200 * (i / bottom_bar_height))
    draw.rectangle([0, H + i, W, H + i + 1], fill=(5, 5, 10, alpha))

# Try fonts
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
font = None
font_size = int(W * 0.085)
for fp in font_paths:
    if os.path.exists(fp):
        font = ImageFont.truetype(fp, size=font_size)
        break
if not font:
    font = ImageFont.load_default()

text = "OBSCURED HISTORY"
bbox = draw.textbbox((0, 0), text, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

# Scale font down if text is too wide
while text_w > W * 0.88 and font_size > 30:
    font_size -= 4
    font = ImageFont.truetype(font_paths[0], size=font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

x = (W - text_w) // 2
y = H + (bottom_bar_height - text_h) // 2

# Shadow
draw.text((x + 3, y + 3), text, font=font, fill=(0, 0, 0, 200))
# Gold text
draw.text((x, y), text, font=font, fill=(218, 180, 100, 255))

# Thin gold divider line above text
draw.rectangle([int(W*0.1), H + 8, int(W*0.9), H + 10], fill=(218, 180, 100, 180))

final = new_img.convert("RGB")
final.save("videos/images/channel_logo_final.jpg", quality=95)
print(f"✅ Done — canvas: {W}x{H + bottom_bar_height}")
