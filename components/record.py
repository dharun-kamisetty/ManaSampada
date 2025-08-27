import streamlit as st
from utils.api_client import create_monument_record, upload_monument_files, process_audio, analyze_content
from utils.api_client import get_categories

def render_record_tab():
    """Render the monument recording interface"""
    st.markdown('<h2 class="sub-header">Document a Monument</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to document monuments")
        return
    
    # Load categories
    load_categories()
    
    # Create interface
    render_capture_interface()
    render_monument_form()

def load_categories():
    """Load categories if not already loaded"""
    if 'categories' not in st.session_state or not st.session_state.categories:
        with st.spinner("Loading categories..."):
            categories_data = get_categories(st.session_state.user_token)
            if categories_data["success"]:
                st.session_state.categories = categories_data["data"]
            else:
                st.session_state.categories = []
                st.error(f"Failed to load categories: {categories_data['error']}")

def render_capture_interface():
    """Render photo and audio capture interface"""
    col1, col2 = st.columns(2)
    
    with col1:
        render_photo_capture()
    
    with col2:
        render_audio_capture()

def render_monument_form():
    """Render monument details form"""
    st.markdown("---")
    st.subheader("Monument Details")
    
    with st.form("monument_form"):
        title = st.text_input("Monument Title*", placeholder="Enter a title for the monument")
        location = st.text_input("Location*", placeholder="Enter the location of the monument")
        
        # Category selection
        category_id = render_category_selector()
        
        description = st.text_area(
            "Description*", 
            placeholder="Describe the monument, its history, significance, etc.",
            height=150
        )
        
        tags = st.text_input("Tags", placeholder="Comma-separated tags (e.g., temple, historical, ancient)")
        
        # Location coordinates
        col_loc1, col_loc2 = st.columns(2)
        with col_loc1:
            latitude = st.number_input("Latitude (optional)", format="%.6f")
        with col_loc2:
            longitude = st.number_input("Longitude (optional)", format="%.6f")
        
        if st.button("📍 Use Current Location"):
            st.info("In a production app, this would use browser geolocation API")
        
        submit_button = st.form_submit_button("Upload Monument Documentation")
        
        if submit_button:
            handle_monument_submission(title, location, description, category_id, tags, latitude, longitude)

# Additional helper functions for record would go here...