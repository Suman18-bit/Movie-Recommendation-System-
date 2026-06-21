# 🎬 Movie Matcher: AI-Powered Recommendation Engine
##> ⚠️ **Disclaimer**  
> You will find the `movies_metadata.csv` file inside the **archive(4)** folder.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org/)

An advanced content-based recommendation system that leverages **Natural Language Processing (NLP)** and **Cosine Similarity** to suggest movies based on plot depth, genre overlap, and thematic taglines.

## 🌟 Key Features

- **🎯 Precision Matching**: Uses TF-IDF (Term Frequency-Inverse Document Frequency) with n-gram ranges (1-3) to capture contextual meaning.
- **⚡ Real-time Discovery**: Instantaneous similarity calculation across thousands of titles.
- **🎨 Modern Dashboard**: Interactive UI featuring movie selection and instant recommendation lists.
- **🧹 Automated Pipeline**: Full text preprocessing including Lemmatization, Stemming, and Stop-word removal.

## 🛠️ Technical Architecture

### **1. Data Preprocessing**
- Handling missing values and malformed CSV rows.
- Feature Engineering: Merging `Title`, `Genres`, and `Taglines` into a unified 'Content DNA'.
- Standard Scaling of popularity and voting metrics.

### **2. NLP & Vectorization**
- **Tokenizer**: Custom NLTK-based cleaning (punctuation/emoji removal).
- **Vector Space**: Transformation of text into high-dimensional TF-IDF vectors.

### **3. Similarity Metric**
- Implementation of **Cosine Similarity** to calculate the distance between movie vectors in the latent space.

## 🚀 Installation & Deployment

### Prerequisites
```bash
pip install streamlit pandas scikit-learn nltk
```

### Running the Application
1. Generate the data artifacts:
   ```bash
   python preprocess.py  # or run the notebook cells
   ```
2. Launch the Streamlit server:
   ```bash
   streamlit run app.py
   ```

## 📸 Application Preview
The app allows users to select a movie from a searchable dropdown and instantly displays the top 7 most similar films with their calculated relevance.

---
*Built with precision for movie enthusiasts.*
