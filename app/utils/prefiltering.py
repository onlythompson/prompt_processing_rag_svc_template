from typing import List, Dict
import re

def prefilter_documents(documents: List[Dict], keywords: List[str]) -> List[Dict]:
    """
    Prefilter documents based on the presence of specified keywords.
    """
    filtered_docs = []
    for doc in documents:
        content = doc['content'].lower()
        if any(keyword.lower() in content for keyword in keywords):
            filtered_docs.append(doc)
    return filtered_docs

def preprocess_query(query: str) -> str:
    """
    Preprocess the query by removing special characters and extra whitespace.
    """
    # Remove special characters
    query = re.sub(r'[^\w\s]', '', query)
    # Remove extra whitespace
    query = ' '.join(query.split())
    return query.lower()