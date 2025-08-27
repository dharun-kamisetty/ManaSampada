import streamlit as st
from utils.auth import logout_user

def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/2E86C1/FFFFFF?text=Swecha-Kosam", use_column_width=True)
        st.markdown("## Navigation")
        
        if st.session_state.authenticated:
            st.success(f"Logged in as **{st.session_state.phone}**")
            if st.button("Logout"):
                logout_user()
                st.experimental_rerun()
        else:
            st.info("Please login to access all features")
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- 📸 Document Monuments")
        st.markdown("- 📊 View Leaderboard")
        st.markdown("- 🔍 Discover Content")
        st.markdown("- 👥 User Profile")
        
        st.markdown("---")
        st.markdown("### About Swecha-Kosam")
        st.markdown("Preserving Telugu cultural heritage through community contributions.")