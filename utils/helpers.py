import streamlit as st
from config import SESSION_DEFAULTS
from datetime import datetime
import uuid

def generate_upload_uuid():
    """Generate a unique UUID for file uploads"""
    return str(uuid.uuid4())

def initialize_session_state():
    """Initialize all session state variables with defaults"""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value

def clear_session_state():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    initialize_session_state()

def check_authentication():
    """Check if the user is properly authenticated"""
    if (st.session_state.authenticated and 
        st.session_state.user_token and 
        st.session_state.user_id):
        
        from utils.auth import validate_token
        if not validate_token(st.session_state.user_token):
            clear_session_state()
            return False
        
        return True
    return False

def load_categories():
    """Load categories - using the specific sample categories provided"""
    sample_categories = [
        {
            "name": "local_history",
            "title": "Local History", 
            "description": "Compiling historical events and figures significant to your region.",
            "id": "ab7f2757-ccdf-4ef6-9850-2cdfe6e1b422",
            "published": True,
            "rank": 19
        },
        {
            "name": "culture",
            "title": "Culture",
            "description": "Cultural traditions, customs, and heritage", 
            "id": "ab9fa2ce-1f83-4e91-b89d-cca18e8b301e",
            "published": True,
            "rank": 11
        },
        {
            "name": "images", 
            "title": "Images",
            "description": "Visual content, pictures, and graphic materials",
            "id": "4366cab1-031e-4b37-816b-311ee34461a9",
            "published": True,
            "rank": 10
        },
        {
            "name": "architecture",
            "title": "Architecture",
            "description": "Buildings, structures, and architectural designs",
            "id": "94a13c20-8a03-45da-8829-10e2fe1e61a1",
            "published": True,
            "rank": 8
        },
        {
            "name": "places",
            "title": "Places",
            "description": "Locations, landmarks, and geographical content",
            "id": "96e5104f-c786-4928-b932-f59f5b4ddbf0",
            "published": True,
            "rank": 4
        }
    ]
    
    import streamlit as st
    st.session_state.categories = sample_categories
    return True

def format_date(date_string):
    """Format date string to readable format"""
    if not date_string:
        return "Unknown"
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_string

def generate_upload_uuid():
    """Generate a unique UUID for file uploads"""
    return str(uuid.uuid4())