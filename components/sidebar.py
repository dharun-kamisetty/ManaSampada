import streamlit as st


def render_sidebar():
    """Render the application sidebar"""
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50/2E86C1/FFFFFF?text=Swecha-Kosam", use_column_width=True)
        st.markdown("## Navigation")
        
        if st.session_state.authenticated:
            st.success(f"Logged in as **{st.session_state.name}**")
            
        else:
            st.info("Please login to access all features")
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- 📸 Document Monuments")
        st.markdown("- 📊 View Leaderboard")
        st.markdown("- 🔍 Discover Content")
        st.markdown("- 👥 User Profile")
        
        st.markdown("---")
        st.markdown("### About Mana-Sampada")
        st.markdown("Preserving our cultural heritage through community contributions.")