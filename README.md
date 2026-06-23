<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,28&height=220&section=header&text=🎬%20Movie%20Recommendation%20System&fontSize=42&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=Discover%20Your%20Next%20Favorite%20Film%20with%20AI&descAlignY=60&descAlign=50" width="100%"/>

</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![GitHub](https://img.shields.io/badge/By-Suman18--bit-181717?style=for-the-badge&logo=github)](https://github.com/Suman18-bit)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

</div>

<br/>

<div align="center">

> **🍿 An intelligent movie recommendation engine powered by Machine Learning — wrapped in a sleek Streamlit web app. Just run it and let AI find your next watch!**

</div>

---

## 📌 Table of Contents

- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ How It Works](#️-how-it-works)
- [🚀 Getting Started](#-getting-started)
- [🎯 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

<div align="center">

| 🎭 Feature | 📝 Description |
|:----------:|:--------------|
| 🔍 **Smart Search** | Search movies by title and get instant recommendations |
| 🤖 **ML-Powered** | Uses cosine similarity & vectorization for accurate suggestions |
| 🌐 **Web App** | Beautiful, interactive Streamlit interface — no setup needed to use |
| 🎞️ **Rich Results** | Displays movie posters, titles, and metadata |
| ⚡ **Fast & Lightweight** | Optimized for quick recommendations even on large datasets |

</div>

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

</div>

---

## 📁 Project Structure

```
Movie-Recommendation-System/
│
├── 📓 Movie_Recommendation_system.ipynb   # Full ML notebook + Streamlit app
├── 📦 archive (4).zip                     # Dataset (movies metadata)
└── 📄 README.md                           # You're here!
```

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   📥 Dataset (archive.zip)                              │
│        │                                                │
│        ▼                                                │
│   🔧 Data Preprocessing (Pandas + NumPy)                │
│        │                                                │
│        ▼                                                │
│   🧬 Feature Extraction (TF-IDF / Count Vectorizer)     │
│        │                                                │
│        ▼                                                │
│   📐 Cosine Similarity Matrix                           │
│        │                                                │
│        ▼                                                │
│   🎬 Top-N Movie Recommendations                        │
│        │                                                │
│        ▼                                                │
│   🌐 Streamlit Web App (Interactive UI)                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

The system uses **content-based filtering**:
1. Extracts features from movie genres, keywords, cast, and overview
2. Converts them into numerical vectors
3. Computes cosine similarity between all movies
4. Returns the top similar movies for any given input

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Suman18-bit/Movie-Recommendation-System-.git
cd Movie-Recommendation-System-
```

### 2️⃣ Install Dependencies

```bash
pip install streamlit pandas numpy scikit-learn requests
```

### 3️⃣ Extract the Dataset

```bash
unzip "archive (4).zip"
```

### 4️⃣ Launch the App 🚀

```bash
streamlit run Movie_Recommendation_system.ipynb
```

Or open the notebook directly:

```bash
jupyter notebook Movie_Recommendation_system.ipynb
```

> ✅ **That's it!** The app will open in your browser at `http://localhost:8501`

---

## 🎯 Usage

```
1. 🔎  Type or select a movie title in the search bar
2. 🎯  Click "Get Recommendations"
3. 🍿  Enjoy your personalized list of similar movies!
```

---

## 📸 Demo Preview

```
╔══════════════════════════════════════════════════╗
║         🎬 Movie Recommendation System           ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Enter a movie:  [ Inception          🔽 ]       ║
║                                                  ║
║  [ 🎯 Recommend ]                                ║
║                                                  ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐       ║
║  │ 🎬 Movie │  │ 🎬 Movie │  │ 🎬 Movie │       ║
║  │   #1     │  │   #2     │  │   #3     │       ║
║  └──────────┘  └──────────┘  └──────────┘       ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

---

## 🤝 Contributing

Have ideas to improve the recommendation engine? Contributions are welcome!

```bash
# Fork the repo
# Create your feature branch
git checkout -b feature/AmazingFeature

# Commit your changes
git commit -m 'Add AmazingFeature'

# Push and open a Pull Request
git push origin feature/AmazingFeature
```

---

## 📬 Connect with Me

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-Suman18--bit-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Suman18-bit)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com)
[![Gmail](https://img.shields.io/badge/Gmail-Contact-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:your@email.com)

</div>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,28&height=120&section=footer" width="100%"/>

**🌟 If this project helped you, drop a star — it means the world!**

*Made with ❤️ and 🍿 by [Suman18-bit](https://github.com/Suman18-bit)*

</div>
