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
    
    st.markdown('<h1 class="main-header"> 📸 Mana-Sampada</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7D6608;">Preserving Indias Cultural Heritage for Future Generations</p>', unsafe_allow_html=True)

def load_categories():
    """Load categories - using only sample data"""
    sample_categories = [
        {
            "name": "local_history",
            "title": "Local History",
            "published": True,
            "created_at": "2025-06-30T03:50:12.383000",
            "description": "Compiling historical events and figures significant to your region.",
            "id": "ab7f2757-ccdf-4ef6-9850-2cdfe6e1b422",
            "rank": 19,
            "updated_at": "2025-06-30T03:50:12.383000"
        },
        {
            "name": "culture", 
            "title": "Culture",
            "published": True,
            "created_at": "2025-06-14T06:55:08.952958",
            "description": "Cultural traditions, customs, and heritage",
            "id": "ab9fa2ce-1f83-4e91-b89d-cca18e8b301e",
            "rank": 11,
            "updated_at": "2025-06-14T06:55:08.953174"
        },
        {
            "name": "images",
            "title": "Images", 
            "published": True,
            "created_at": "2025-06-14T06:55:08.325970",
            "description": "Visual content, pictures, and graphic materials",
            "id": "4366cab1-031e-4b37-816b-311ee34461a9",
            "rank": 10,
            "updated_at": "2025-06-14T06:55:08.326328"
        }
    ]
    
    st.session_state.categories = sample_categories