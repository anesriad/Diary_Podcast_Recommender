# 🎧 YouTube Comment Intelligence Pipeline

### **Overview**
This system analyzes large volumes of *Diary of a CEO* podcast comments to uncover viewer **sentiment**, **guest mentions**, and **topic interests** — all efficiently and at scale.

---

### **How It Works**

1. **Text Cleaning & Preprocessing**  
   - Removes noise (mentions, emojis, URLs) for clean inputs.  
   - Ensures consistency across thousands of comments.

2. **Sentiment Analysis (Hybrid AI)**  
   - Combines **RoBERTa** (fast, precise) and **Gemma LLM** (context-aware).  
   - Detects nuanced tone (sarcasm, mixed feelings).  
   - Classifies each comment as **Positive**, **Neutral**, or **Negative**.

3. **Engagement Weighting**  
   - Weighs each comment by its like count to reflect real impact.  
   - Produces an **impact-weighted sentiment score** for accurate ranking.

4. **Guest & Topic Extraction**  
   - Identifies real guest names using **spaCy** + LLM fallback.  
   - Detects audience topic requests (e.g., “mental health”, “AI”).  
   - Filters out irrelevant or low-quality results.

5. **Caching & Speed Optimization**  
   - Built-in **SQLite cache** avoids duplicate computation.  
   - Runs tasks in **parallel** and supports **GPU acceleration**.  
   - Reduces processing time from hours to minutes.

---

### **Key Outputs**

| Column | Description |
|---------|-------------|
| `sentiment_bucket` | Positive / Neutral / Negative classification |
| `impact_weighted_sentiment` | Sentiment × engagement weight |
| `guest_mentions` | Guest names detected in comments |
| `topic_requests` | Suggested topics or content ideas |

---

### **Value for Stakeholders**

- 📊 Quantifies audience sentiment and engagement by episode or guest.  
- 🎯 Highlights which guests and topics drive the strongest viewer response.  
- ⚡ Enables data-driven decisions for future content and sponsorships.  
- 💾 Scalable: handles **1M+ comments** efficiently via AWS or local GPU compute.

---

### **In Short**
A **scalable, AI-powered comment analysis pipeline** that transforms unstructured YouTube feedback into actionable audience insights for strategic podcast and content planning.
