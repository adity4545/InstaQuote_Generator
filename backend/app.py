from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import io
import traceback
import pillow_heif
import random
pillow_heif.register_heif_opener()

app = Flask(__name__)
CORS(app)

INSTAGRAM_SIZE = (1080, 1080)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        images = request.files.getlist('images')
        quote = request.form.get('quote', '')
        author = request.form.get('author', '')
        font_size = int(request.form.get('fontSize', 48))
        color = request.form.get('color', '#ffffff')
        align = request.form.get('align', 'center')

        print(f"Received {len(images)} images, quote: '{quote}', author: '{author}', font_size: {font_size}, color: {color}, align: {align}")

        # Accept 1–3 images
        if not (1 <= len(images) <= 3):
            return jsonify({'error': 'Please upload 1, 2, or 3 images.'}), 400

        # Open and resize images
        pil_images = [Image.open(img).convert('RGB').resize(INSTAGRAM_SIZE) for img in images]

        if len(pil_images) == 1:
            # Single image background
            bg = pil_images[0].copy().convert('RGBA')
        else:
            # Collage for 2 or 3 images (polaroid style)
            bg = Image.new('RGBA', INSTAGRAM_SIZE, (245, 245, 245, 255))
            polaroid_size = (420, 520)
            positions = [
                (120, 100, -10),
                (540, 180, 8),
                (320, 480, -5)
            ]
            for i, img in enumerate(pil_images):
                polaroid = Image.new('RGBA', polaroid_size, (255, 255, 255, 255))
                img_resized = img.resize((380, 380)).convert('RGBA')
                polaroid.paste(img_resized, (20, 20))
                shadow = Image.new('RGBA', (polaroid_size[0]+12, polaroid_size[1]+12), (0,0,0,0))
                shadow_draw = ImageDraw.Draw(shadow)
                shadow_draw.rectangle([8,8,polaroid_size[0]+8,polaroid_size[1]+8], fill=(0,0,0,80))
                polaroid_with_shadow = Image.alpha_composite(shadow, Image.new('RGBA', shadow.size, (0,0,0,0)))
                polaroid_with_shadow.paste(polaroid, (6,6), polaroid)
                angle = positions[i][2] if i < len(positions) else random.randint(-12, 12)
                polaroid_with_shadow = polaroid_with_shadow.rotate(angle, expand=1, resample=Image.BICUBIC)
                px = positions[i][0] if i < len(positions) else random.randint(100, 600)
                py = positions[i][1] if i < len(positions) else random.randint(100, 600)
                bg.alpha_composite(polaroid_with_shadow, (px, py))

        # Draw quote and author
        draw = ImageDraw.Draw(bg)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", int(request.form.get('fontSize', 64)))
        except:
            font = ImageFont.load_default()
        quote_text = request.form.get('quote', '')
        # Compose full text with author if present
        full_text = quote_text
        if author:
            full_text += f"\n\n— {author}"

        # Text wrapping for long quotes
        def wrap_text(text, font, max_width):
            lines = []
            for paragraph in text.split('\n'):
                line = ''
                for word in paragraph.split(' '):
                    test_line = f'{line} {word}'.strip()
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    w = bbox[2] - bbox[0]
                    if w > max_width and line:
                        lines.append(line)
                        line = word
                    else:
                        line = test_line
                lines.append(line)
            return lines

        lines = wrap_text(full_text, font, INSTAGRAM_SIZE[0] - 120)
        text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align=request.form.get('align', 'center'))
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (INSTAGRAM_SIZE[0] - text_w) // 2
        y = (INSTAGRAM_SIZE[1] - text_h) // 2

        # Draw semi-transparent rectangle for visibility
        overlay = Image.new('RGBA', bg.size, (0,0,0,0))
        overlay_draw = ImageDraw.Draw(overlay)
        rect_x0 = x - 30
        rect_y0 = y - 30
        rect_x1 = x + text_w + 30
        rect_y1 = y + text_h + 30
        overlay_draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(0,0,0,140))
        bg = Image.alpha_composite(bg, overlay)

        # Draw text with white color and black outline
        draw = ImageDraw.Draw(bg)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx != 0 or dy != 0:
                    draw.multiline_text((x+dx, y+dy), text, font=font, fill='black', align=request.form.get('align', 'center'), spacing=6)
        draw.multiline_text((x, y), text, font=font, fill='white', align=request.form.get('align', 'center'), spacing=6)
        bg = bg.convert('RGB')

        # Save to buffer as JPEG
        buf = io.BytesIO()
        bg.save(buf, format='JPEG', quality=95)
        buf.seek(0)
        return send_file(buf, mimetype='image/jpeg', as_attachment=False, download_name='instaquote.jpg')
    except Exception as e:
        print('Exception in /generate:', e)
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 