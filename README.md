# Diary of a CEO - Podcast recommender (topic/Guests)

## 🧠 Overview
This project analyzes YouTube video comments to uncover **audience sentiment, tone, and engagement patterns** for podcast-style videos.  
It uses modern NLP and small language models to detect nuanced feedback, highlight popular topics, and measure how viewers react to specific themes or guests.

---

## 🚀 Objectives
- Extract meaningful insights from large volumes of comments.  
- Detect sentiment with **context awareness** (including sarcasm and negations).  
- Filter spam, irrelevant, or one-word comments.  
- Categorize videos by **topic** using their titles.  
- Build a pipeline that is **local, scalable, and cost-efficient**.

---

## ⚙️ Tech Stack
**Language:** Python 3.11  
**Environment:** Managed with `uv`  
**IDE:** VS Code  
**Platform:** macOS (M1 Pro)

### Key Libraries
- **pandas**, **numpy** → data handling  
- **spaCy** → lightweight text preprocessing  
- **transformers**, **sentence-transformers** → embeddings and NLP utilities  
- **ollama** → local LLM inference  
- **tqdm** → progress tracking  
- **scikit-learn** → clustering and analysis  
- **dotenv** → environment configuration  

---

## 🧹 Data Cleaning
Before any analysis, each comment undergoes **light cleaning**:
- Removes `@mentions`  
- Removes URLs  
- Removes emojis and non-ASCII characters  
- Converts to lowercase and trims whitespace  
- Drops empty or one-word comments  

The cleaned text is stored separately in a new column to maintain raw data integrity.

---

## 🧠 Sentiment Analysis Workflow
Several model approaches were tested to balance **accuracy**, **speed**, and **scalability**:

| Model | Type | Notes |
|-------|------|-------|
| **RoBERTa (Twitter-based)** | Transformer | Fast but less nuanced |
| **Llama 3.2 (3B)** | Local LLM | Excellent accuracy, slower runtime |
| **Phi 3 Mini** | Local LLM | Lightweight, but slower in practice |
| **OpenRouter (GPT-4o-mini)** | Cloud | High quality, paid, slow |
| **Gemma 2B (final choice)** | Local LLM | Best speed–quality balance for large datasets |

After experimentation, **Gemma 2B** was selected for production because it offers:
- Strong contextual understanding  
- Fast inference on Apple Silicon  
- Zero external cost (runs fully offline)  

---

## 📊 Output Structure
Each processed video generates a DataFrame with:

| Column | Description |
|--------|--------------|
| `channel_name` | YouTube channel name |
| `video_id` | Unique identifier for the video |
| `video_title` | Full title of the video |
| `views` | Number of views |
| `likes` | Number of likes |
| `published_date` | Upload date |
| `comment_text` | Original YouTube comment |
| `cleaned_comment` | Cleaned and normalized text |
| `is_relevant` | 1 = relevant, 0 = spam/irrelevant |
| `sentiment_score` | Float between -1.0 and 1.0 |
| `sentiment_category` | One of: Super Negative, Negative, Neutral, Positive, Super Positive |
| `topic_category` | Extracted topic from the video title |

This structure allows **easy filtering, aggregation, and visualization** for further insights.

---

## ⚡ Performance & Optimization
- Average runtime (**Gemma 2B, local**): ~5–6 minutes per 1,200 comments  
- Fully offline — no API latency or usage costs  
- Optimized for Apple’s Metal GPU backend  
- Supports batching and parallel processing for scalability  

### Key Optimizations
- Light preprocessing only (no heavy lemmatization).  
- Minimal stopword filtering to preserve context.  
- Efficient sentiment prompt optimized for **nuance and sarcasm** detection.  
- Local LLM execution via Ollama for **GPU acceleration**.  

---

## 💰 Cost Comparison

| Method | Speed | Accuracy | Cost | Notes |
|---------|--------|----------|------|-------|
| **Gemma 2B (local)** | ⚡ Fast | 🟢 Good | Free | Ideal for large datasets |
| **Llama 3B (local)** | 🐢 Moderate | 🟢 Excellent | Free | Great accuracy, slower |
| **GPT-4o-mini (OpenRouter)** | 🐌 Slow | 🟢 Excellent | Paid | High quality, not scalable |
| **AWS Bedrock (Claude 3 Haiku)** | ⚡ Scalable | 🟢 High | ~$0.25–$0.40 / 1k comments | Cloud-level performance |

---

## 🧩 Processing Pipeline

### 1. Data Collection
YouTube Data API is used to extract:
- Channel details  
- Video metadata (title, views, likes, published date)  
- All comments and replies (excluding author responses)

### 2. Data Cleaning
Removes noise and standardizes text.

### 3. Relevance Filtering
Flags short or meaningless comments as irrelevant.

### 4. Sentiment Scoring
Local LLM assigns a **sentiment score (-1 to 1)** and category.

### 5. Topic Categorization
Video titles are analyzed once per unique `video_id` to create a **topic category**.

### 6. Output
Final dataset is exported to CSV for later visualization or BI integration.

---

## 🔍 Insights & Use Cases
- Identify **most engaging topics** or guests.  
- Detect **negative audience feedback** trends early.  
- Measure **tone shifts** over time (e.g., more positive or negative sentiment).  
- Support **content strategy** for future videos.  

---

## 🧭 Future Enhancements
- Implement **topic modeling** with BERTopic or KeyBERT for keyword discovery.  
- Add **parallel processing** for million-scale datasets.  
- Integrate **Streamlit dashboard** for sentiment visualization.  
- Experiment with **AWS Bedrock** for large-scale production deployment.

---


## ✅ Summary
This project delivers a **local, high-quality sentiment analysis pipeline** for YouTube comments that:
- Understands **context, sarcasm, and emotional tone**  
- Runs entirely on your **local machine** using small open-source LLMs  
- Scales efficiently to hundreds of thousands of comments  
- Produces structured outputs ready for dashboards or reports  

---

## 🏁 Quick Start (Summary)
1. Clone the repository.  
2. Create a virtual environment using `uv` and sync dependencies.  
3. Add your YouTube API key in `.env`.  
4. Run the notebook to scrape, clean, and analyze comments.  
5. Export results to CSV or visualize in Streamlit/Power BI.

---

**Author:** Anas Riad  
**Project:** *MLE – Diary of a CEO Sentiment Analysis*  
**Focus:** NLP · ML Engineering · LLMs · Data-Driven Insights

