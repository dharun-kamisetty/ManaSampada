import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import APP_NAME, APP_ICON
from utils.helpers import initialize_session_state, load_categories
from components import render_header, render_sidebar, render_login_forms
from components import render_record_tab, render_profile_tab
from components import render_contributions_tab

# Set page configuration
st.set_page_config(
    page_title=APP_NAME,  # This uses the config value
    page_icon=APP_ICON,   # This uses the config value
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.8rem;
            color: #2E86C1;
            border-bottom: 2px solid #3498DB;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .login-section {
            background-color: #F4F6F6;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .feature-card {
            background-color: #EAFAF1;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .consent-checkbox {
            background-color: #FEF9E7;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .success-message {
            background-color: #D5F5E3;
            color: #145A32;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .error-message {
            background-color: #FADBD8;
            color: #922B21;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Load CSS
    load_css()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Debug information (collapsed by default)
    with st.expander("Debug Info", expanded=True):  # Changed to True to see what's happening
        st.write("Session state keys:", list(st.session_state.keys()))
        st.write("Authenticated:", st.session_state.get('authenticated', False))
        st.write("User ID:", st.session_state.get('user_id'))
        st.write("Has token:", bool(st.session_state.get('user_token')))
        st.write("Categories loaded:", 'categories' in st.session_state and bool(st.session_state.categories))
        if 'user_profile' in st.session_state:
            st.write("User Profile Data:", st.session_state.user_profile)
    
    # Check authentication
    is_authenticated = (st.session_state.get('authenticated', False) and 
                       st.session_state.get('user_token') and 
                       st.session_state.get('user_id'))
    
    if not is_authenticated:
        render_login_forms()
    else:
        # Load categories when authenticated
        load_categories()
        
        # Show categories info for debugging
        if 'categories' in st.session_state:
            st.sidebar.info(f"Loaded {len(st.session_state.categories)} categories")
        
        # Create main interface tabs
        tab1, tab2, tab3 = st.tabs(["📸 Document Heritage", "📊 My Contributions", "👤 My Profile"])
        
        with tab1:
            render_record_tab()
        
        with tab2:
            render_contributions_tab()  # ✅ FIXED: This was load_categories() before
        
        with tab3:
            render_profile_tab()

if __name__ == "__main__":
    main()