import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from label import hairtype
from prediction import predict_hairtype
from textblob import TextBlob

keyword_df = pd.read_csv("hairtypekeyword.csv")
product_df = pd.read_csv("shampoo_data.csv", index_col=0)
product_df.columns = product_df.columns.str.strip()

product_df["Combined_Text"] = (
    product_df["Product Name"] + " " +
    product_df["HighLight"] + " " +
    product_df["Description"] + " " +
    product_df["Specification"] + " " +
    product_df["feedback"]
)

product_df["Combined_Text"] = product_df["Combined_Text"].str.lower()
product_df["Combined_Text"] = product_df["Combined_Text"].fillna("") 
product_df["Product Cost"] = product_df["Product Cost"].str.replace("₹", "", regex=False)
product_df["Product Cost"] = pd.to_numeric(product_df["Product Cost"], errors="coerce")

def sentiment(text):
    if len(text.strip()) < 10:  
        return 0  
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  

product_df["feedback"] = product_df["feedback"].fillna("").astype(str)
product_df["feedback_Score"] = product_df["feedback"].apply(sentiment)
tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2),max_df=0.8, min_df=2, max_features=5000)
tfidf_matrix = tfidf.fit_transform(product_df["Combined_Text"])

def get_keywords_for_hairtype(hair_type):
    keywords = keyword_df[keyword_df["HairType"] == hair_type]["Keywords"].values[0]
    return keywords

def recommend_products(hair_type, max_price=None, min_feedback=None, top_n=5):
    keywords = get_keywords_for_hairtype(hair_type)
    keywords_vector = tfidf.transform([keywords])
    similarity_scores = cosine_similarity(keywords_vector, tfidf_matrix).flatten()
    product_df["Similarity_Score"] = similarity_scores
    filtered_df = product_df.copy()
    if max_price:
        filtered_df = filtered_df[filtered_df["Product Cost"] <= max_price]
    if min_feedback:
        filtered_df = filtered_df[filtered_df["feedback_Score"] >= min_feedback]
    filtered_df = filtered_df.sort_values(by="Similarity_Score", ascending=False)
    filtered_df = filtered_df.drop_duplicates(subset=["Product Name"])
    recommended_df = filtered_df.head(top_n)
    return recommended_df

