import streamlit as st

def render_header():
    """Render the application header"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🎙️ Swecha-Kosam</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7D6608;">Preserving Telugu stories and voices for future generations</p>', unsafe_allow_html=True)