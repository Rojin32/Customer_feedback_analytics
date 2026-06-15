import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
st.set_page_config(
    page_title="Customer Feedback Dashboard",
    layout="wide"
)

st.title("Customer Feedback Analytics Dashboard")

conn = sqlite3.connect("feedback.db")

df = pd.read_sql_query(
    "SELECT * FROM feedback",
    conn
)

conn.close()

#-- Metrics ---
st.header("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_feedback = len(df)

positive = len(
    df[df["sentiment"] == "Positive"]
)

negative = len(
    df[df["sentiment"] == "Negative"]
)

avg_rating = round(
    df["rating"].mean(),
    2
)

col1.metric(
    "Total Feedback",
    total_feedback
)

col2.metric(
    "Positive Reviews",
    positive
)

col3.metric(
    "Negative Reviews",
    negative
)

col4.metric(
    "Average Rating",
    avg_rating
)

#-- Feedback Table ---
st.header("All Feedback")

st.dataframe(df)


#-- Sentiment Distribution ---
st.header("Sentiment Distribution")
sentiment_counts = df["sentiment"].value_counts()
fig, ax = plt.subplots()
ax.pie(
    sentiment_counts,
    labels=sentiment_counts.index,
    autopct="%1.1f%%",
    
    startangle=90
)
ax.set_title("Sentiment Distribution")
st.pyplot(fig)

#-- Rating Distribution ---
st.header("Rating Distribution")
rating_counts = df["rating"].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(
    rating_counts.index,
    rating_counts.values,
    color="skyblue"
)
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
ax.set_title("Rating Distribution")
st.pyplot(fig)


#-- Feedback Over Time ---  
st.header("Daily Feedback Trend")

df["timestamp"] = pd.to_datetime(df["timestamp"])

daily_feedback = (
    df.groupby(
        df["timestamp"].dt.date
    ).size()
)

fig3, ax3 = plt.subplots()

ax3.plot(
    daily_feedback.index,
    daily_feedback.values
)

ax3.set_xlabel("Date")

ax3.set_ylabel("Reviews")

ax3.set_title("Feedback Over Time")

plt.xticks(rotation=45)

st.pyplot(fig3)



#-- Product Comparison ---
st.header("Product Comparison")

product_rating = (
    df.groupby("product_name")["rating"]
    .mean()
    .sort_values(ascending=False)
)

fig4, ax4 = plt.subplots()

ax4.bar(
    product_rating.index,
    product_rating.values
)

ax4.set_xlabel("Product")

ax4.set_ylabel("Average Rating")

ax4.set_title("Average Product Rating")

plt.xticks(rotation=45)

st.pyplot(fig4)


#-- Top Complaint Keywords ---

st.header("Top Complaint Keywords")

negative_reviews = df[
    df["sentiment"] == "Negative"
]

text = " ".join(
    negative_reviews["feedback"]
    .astype(str)
)

words = re.findall(
    r'\b[a-zA-Z]+\b',
    text.lower()
)

stopwords = {
    "the","is","a","an","and",
    "to","of","in","for","on",
    "it","this","that","was"
}

words = [
    word
    for word in words
    if word not in stopwords
]

top_words = Counter(words).most_common(10)

keyword_df = pd.DataFrame(
    top_words,
    columns=["Keyword","Count"]
)

st.dataframe(keyword_df)





