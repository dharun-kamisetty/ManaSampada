import streamlit as st
import groq
import json
from typing import Optional

def get_groq_client():
    """Initialize Groq client with API key from secrets"""
    try:
        client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])
        return client
    except Exception as e:
        st.error(f"AI service temporarily unavailable")
        return None

def get_cultural_insight(heritage_data: dict) -> Optional[str]:
    """
    Get AI-powered insights about cultural heritage items
    """
    try:
        client = get_groq_client()
        if not client:
            return None
        
        prompt = f"""
        Provide concise cultural insights about this Indian heritage item:
        
        Title: {heritage_data.get('title', 'Unknown')}
        Description: {heritage_data.get('description', 'No description')}
        Type: {heritage_data.get('content_type', 'Unknown')}
        Location: {heritage_data.get('location', 'Unknown location')}
        
        Focus on: historical context, cultural significance, and preservation importance.
        Keep response under 150 words.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception:
        return None

def get_ai_chat_response(user_query: str) -> str:
    """
    Get AI response for cultural heritage questions (clean version)
    """
    try:
        client = get_groq_client()
        if not client:
            return "I'm currently unavailable. Please try again later."
        
        system_prompt = """
        You are an AI assistant specializing in Indian cultural heritage. 
        Provide accurate, respectful, and concise information about:
        - Indian temples, mosques, churches, and religious sites
        - Cultural traditions and historical significance
        - Preservation methods and best practices
        
        Keep responses informative but brief (under 200 words).
        Be respectful of all cultures and religions.
        """
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        return response.choices[0].message.content
        
    except Exception:
        return "I'm unable to respond at the moment. Please try again later."