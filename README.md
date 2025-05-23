# InstaQuote Collage

Create beautiful, shareable quote images with your own photos and custom text. Supports 1–3 images, bold quote overlays, author attribution, and modern, attractive UI.

## Features
- Upload 1, 2, or 3 images (single image or collage)
- Add a custom quote and author (optional)
- Choose font, font size, alignment, and paint stroke style
- Live preview with instant style updates
- Download the generated image, ready for Instagram or sharing
- Responsive, modern, dark glassmorphism UI

## Tech Stack
- **Frontend:** React.js, Tailwind CSS
- **Backend:** Flask (Python), Pillow, pillow-heif (for HEIC support)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd InstaQuote
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
# If you want HEIC support:
pip install pillow-heif
```

#### Start the Flask server:
```bash
python app.py
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

#### Start the React app:
```bash
npm start
```

---

## Usage
1. Open [http://localhost:3000](http://localhost:3000) in your browser.
2. Upload 1–3 images (JPEG, PNG, HEIC, etc.).
3. Enter your quote and (optionally) the author.
4. Adjust font, size, alignment, and paint stroke style as desired.
5. Click **Generate Collage**.
6. Download your image and share it anywhere!

---

## Example Output
![Example](example-output.jpg)

---

## License
MIT 