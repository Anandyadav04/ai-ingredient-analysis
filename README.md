# RiskRead – AI-Powered Ingredient Safety Analyzer

An intelligent web application that scans packaged food labels, extracts ingredient information using OCR, and analyzes ingredients using Machine Learning to identify potential health risks, allergens, and harmful additives. The system also recommends healthier alternatives for harmful ingredients detected in a product.

---

## 🚀 Features

- OCR-based ingredient extraction from food labels
- Image preprocessing using OpenCV
- AI-powered ingredient safety classification
- Categorizes ingredients into:
  - ✅ Safe
  - ⚠️ Controversial
  - ❌ Harmful
- Suggests healthier alternatives for harmful ingredients
- Supports:
  - Image Upload
  - Text Input
  - Clipboard Pasting
- Interactive dashboard with visual analytics
- Responsive web interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- AJAX

### Backend
- Python
- Flask

### Machine Learning & OCR
- Tesseract OCR
- OpenCV
- Scikit-Learn
- Pandas
- NLTK

---

## ⚙️ Workflow

```text
User Input
   ↓
Image Preprocessing (OpenCV)
   ↓
OCR Extraction (Tesseract OCR)
   ↓
Text Cleaning & NLP Parsing
   ↓
ML Classification
   ↓
Alternative Recommendation Engine
   ↓
Dashboard Results
```

---

## 📂 Project Structure

```bash
RiskRead/
│
├── static/
├── templates/
├── uploads/
├── models/
├── dataset/
├── app.py
├── requirements.txt
└── README.md
```

---

## 📥 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/riskread.git
cd riskread
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```

#### Linux/Mac
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔍 Install Tesseract OCR

### Windows
Download and install:
https://github.com/UB-Mannheim/tesseract/wiki

### Linux

```bash
sudo apt install tesseract-ocr
```

### Verify Installation

```bash
tesseract --version
```

---

## ▶️ Run the Project

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---


## 🔮 Future Enhancements

- Barcode scanning
- Real-time camera scanning
- Personalized allergy alerts
- Mobile app integration
- Cloud ingredient database
- Multilingual OCR support

---

## 📜 License

This project is developed for academic and educational purposes.
