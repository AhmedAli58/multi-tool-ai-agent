import requests
import streamlit as st
from langchain.tools import tool


@tool
def news(topic: str) -> str:
    """Get latest news headlines for a topic."""
    try:
        api_key = st.secrets["NEWS_API_KEY"]
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": topic,
            "apiKey": api_key,
            "pageSize": 5,
            "sortBy": "publishedAt",
            "language": "en"
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        articles = r.json().get("articles", [])
        if not articles:
            return "No news found for " + topic
        lines = ["News about " + topic + ":"]
        for i, a in enumerate(articles, 1):
            source = a.get("source", {}).get("name", "Unknown")
            title = a.get("title", "No title")
            url2 = a.get("url", "")
            lines.append(str(i) + ". [" + source + "] " + title + "\n   " + url2)
        return "\n\n".join(lines)
    except Exception as e:
        return "News error: " + str(e)