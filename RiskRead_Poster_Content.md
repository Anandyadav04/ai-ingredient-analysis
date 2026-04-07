# RiskRead: AI-Powered Ingredient Safety Analyzer
**(Poster Content Draft)**

---
## 1. Header Details
**Title:** RiskRead: AI-Powered Ingredient Safety Analyzer
**Group No.:** [INSERT GROUP NO]
**Group Members:**
1. [INSERT MEMBER 1]
2. [INSERT MEMBER 2]
3. [INSERT MEMBER 3]
**Name of the Guide:** [INSERT GUIDE NAME]

---
## 2. Introduction
Reading food labels is challenging due to complex chemical names and small print. **RiskRead** is an intelligent web application that simplifies this process. By leveraging Optical Character Recognition (OCR) and Machine Learning (ML), it scans product labels, extracts ingredient lists, and instantly analyzes them for potential health risks, allergens, and nutritional concerns.

---
## 3. Problem Definition
- **Consumer Confusion:** Average consumers lack deep chemical knowledge to understand complex ingredient lists on packaged goods.
- **Manual Effort:** Searching for each ingredient individually is time-consuming and prone to errors.
- **Lack of Transparency:** Static databases are often hard to navigate or lack localized product context.
- **Health Risks:** Unidentified allergens or harmful additives can pose serious health risks.

---
## 4. Objectives
- **Automated Extraction:** Develop a system to extract text from product label images with high accuracy.
- **Instant Classification:** Classify ingredients into 'Safe', 'Controversial', or 'Harmful' categories using ML.
- **User-Friendly Interface:** Provide an accessible web platform for instant analysis on desktop and mobile.
- **Education:** Empower users with scientific insights to make healthier consumption choices.

---
## 5. Scope
- **Input Methods:** Text entry, Image Upload (PNG/JPG), and Clipboard Pasting.
- **Domain:** Focuses on packaged Food products.
- **Output:** Classified list of ingredients, safety ratings, and detailed explanations.
- **Platform:** Web-based application built with Flask.

---
## 6. Workflow / System Architecture
**(Suggested Diagram Flow)**
1.  **User Input**: User uploads image or enters text via Web Interface.
2.  **Preprocessing**: Image is rescaled and thresholded (OpenCV) to improve quality.
3.  **OCR Engine**: Tesseract OCR extracts raw text strings from the image.
4.  **NLP Pipeline**: Text is cleaned, parsed, and split into individual ingredients.
5.  **ML Classifier**: The model predicts the safety label (Safe/Controversial/Harmful) for each ingredient.
6.  **Response**: Results are displayed on the dashboard with visual charts.

---
## 7. Technology Stack
**Frontend:**
- HTML5, CSS3 (Custom Responsive Design)
- JavaScript (Dynamic interactions, AJAX)

**Backend:**
- **Language:** Python
- **Framework:** Flask (Web Framework)

**Machine Learning & OCR:**
- **OCR:** Tesseract OCR (Text Extraction)
- **Image Processing:** OpenCV (Preprocessing)
- **ML Libraries:** Scikit-Learn (Classification Models), Pandas, NLTK

---
## 8. Features
- **Multi-Modal Input:** Supports file upload, text input, and clipboard pasting for seamless UX.
- **Advanced Preprocessing:** Auto-scaling and adaptive thresholding for cleaner text extraction.
- **Intelligent Parsing:** Handles complex strings, removes "contains" warnings, and cleans gibberish.
- **Safety Classification:** Categorizes ingredients based on trained health impact models.
- **Visual Analytics:** Interactive dashboard with statistics and color-coded safety indicators.

---
## 9. SDG Mapping
- **SDG 3: Good Health and Well-being**
  - Promotes awareness of hazardous substances, supporting healthier lifestyles.
- **SDG 12: Responsible Consumption and Production**
  - Empowers consumers to demand transparency and make informed choices about product contents.

---
## 10. References
1. **Flask Documentation:** https://flask.palletsprojects.com/
2. **Tesseract OCR:** https://github.com/tesseract-ocr/tesseract
3. **Scikit-learn:** https://scikit-learn.org/
4. **Foodvisor-NYU Dataset:** Source for labeled ingredient data used in training.
