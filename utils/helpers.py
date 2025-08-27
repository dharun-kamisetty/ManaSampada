import streamlit as st
from config import SESSION_DEFAULTS

def initialize_session_state():
    """Initialize all session state variables with defaults"""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def clear_session_state():
    """Clear all session state variables"""
    for key in SESSION_DEFAULTS.keys():
        if key in st.session_state:
            del st.session_state[key]
    initialize_session_state()

def format_duration(seconds):
    """Format seconds into MM:SS format"""
    if not seconds:
        return "N/A"
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def format_date(date_string):
    """Format date string to readable format"""
    if not date_string:
        return "Unknown"
    try:
        # Try to parse ISO format date
        from datetime import datetime
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_string