import streamlit as st
import requests
import os
from utils.helpers import generate_upload_uuid
from utils.api_client import get_categories, get_category_by_id, upload_chunk, finalize_upload
from config import LANGUAGES, RELEASE_RIGHTS
import time

def render_record_tab():
    """Render the cultural heritage recording interface with proper chunked upload"""
    st.markdown('<h2 class="sub-header">Document Cultural Heritage</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to document cultural heritage")
        return
    
    # Load categories with error handling
    if 'categories' not in st.session_state or not st.session_state.categories:
        from utils.helpers import load_categories
        success = load_categories()
        if not success:
            st.error("Failed to load categories. Please try refreshing the page.")
            if st.button("🔄 Refresh Categories"):
                if 'categories' in st.session_state:
                    del st.session_state.categories
                st.experimental_rerun()
            return
    
    # Create interface
    render_media_capture_interface()
    render_heritage_form()

def render_category_selector():
    """Render category selection dropdown"""
    if not st.session_state.get('categories'):
        st.info("Loading categories...")
        return None
    
    # Create category options
    category_options = {}
    for category in st.session_state.categories:
        display_name = f"{category.get('title', category.get('name'))} - {category.get('description', '')}"
        category_options[category['id']] = display_name
    
    if not category_options:
        st.warning("No categories available. Please try again later.")
        return None
    
    category_id = st.selectbox(
        "Category*", 
        options=list(category_options.keys()),
        format_func=lambda x: category_options[x][:80] + "..." if len(category_options[x]) > 80 else category_options[x],
        help="Select the most appropriate category for your heritage site"
    )
    
    return category_id

def render_media_capture_interface():
    """Render media capture interface"""
    st.subheader("1. Capture Image of Heritage Site")
    
    # Image capture
    captured_image = st.camera_input("Take a photo of the temple, mosque, church, or other cultural site", key="heritage_camera")
    
    # File upload alternative
    uploaded_file = st.file_uploader("Or upload an image file", type=["jpg", "jpeg", "png"])
    
    if captured_image is not None:
        st.session_state.captured_image = captured_image
        st.success("✅ Photo captured successfully!")
        st.image(captured_image, use_column_width=True, caption="Captured Image")
    elif uploaded_file is not None:
        st.session_state.captured_image = uploaded_file
        st.success("✅ File uploaded successfully!")
        st.image(uploaded_file, use_column_width=True, caption="Uploaded Image")
    elif st.session_state.get('captured_image'):
        st.image(st.session_state.captured_image, use_column_width=True, caption="Previously captured image")
        if st.button("🗑️ Clear Image"):
            st.session_state.captured_image = None
            st.experimental_rerun()

def render_heritage_form():
    """Render cultural heritage details form"""
    st.markdown("---")
    st.subheader("2. Add Details")
    
    with st.form("heritage_form"):
        # Basic information
        title = st.text_input("Title*", placeholder="Name of the heritage site (e.g., Ancient Temple, Historic Mosque)")
        
        # Category selection
        category_id = render_category_selector()
        
        # Language selection - CORRECTED to use Indian languages
        language = st.selectbox("Language*", 
                               options=LANGUAGES,
                               format_func=lambda x: x.capitalize(),
                               help="Select the language for your description")
        
        # Description
        description = st.text_area("Description*", 
                                 placeholder="Describe the heritage site, its history, significance, architectural features, cultural importance...",
                                 height=100)
        
        # Location information
        location = st.text_input("Location*", placeholder="Village, City, District, State")
        
        # Coordinates (optional)
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input("Latitude (optional)", format="%.6f")
        with col2:
            longitude = st.number_input("Longitude (optional)", format="%.6f")
        
        # Additional information
        significance = st.text_area("Cultural Significance (optional)", 
                                  placeholder="Why is this heritage important to the community?",
                                  height=60)
        
        tags = st.text_input("Tags (optional)", placeholder="Comma-separated tags: ancient, temple, sculpture, history")
        
        # Consent - CORRECTED release rights options
        st.markdown('<div class="consent-checkbox">', unsafe_allow_html=True)
        release_rights = st.selectbox("Usage Rights*", 
                                    options=RELEASE_RIGHTS,
                                    format_func=lambda x: {
                                        "creator": "I created this content",
                                        "family_or_friend": "From family or friend", 
                                        "downloaded": "Downloaded from source",
                                        "NA": "Not applicable/Not sure"
                                    }[x],
                                    help="How can others use your contribution?")
        st.markdown('</div>', unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("Upload to Cultural Heritage Database")
        
        if submit_button:
            handle_heritage_submission(title, description, category_id, language, location, 
                                     latitude, longitude, significance, tags, release_rights)
def handle_heritage_submission(title, description, category_id, language, location, 
                             latitude, longitude, significance, tags, release_rights):
    """Handle heritage form submission with proper chunked upload"""
    # Validation
    if not title or not description or not category_id or not language or not location:
        st.error("Please fill in all required fields (marked with *)")
        return
    
    if not st.session_state.get('captured_image'):
        st.error("Please capture or upload an image first")
        return
    
    # Prepare additional description
    full_description = description
    if significance:
        full_description += f"\n\nCultural Significance: {significance}"
    if tags:
        full_description += f"\n\nTags: {tags}"
    
    # Generate upload UUID
    upload_uuid = generate_upload_uuid()
    filename = f"heritage_{upload_uuid}.jpg"
    
    # Get image data
    try:
        if hasattr(st.session_state.captured_image, 'getvalue'):
            # From camera
            image_data = st.session_state.captured_image.getvalue()
        else:
            # From file upload
            st.session_state.captured_image.seek(0)
            image_data = st.session_state.captured_image.read()
    except Exception as e:
        st.error(f"Error reading image: {str(e)}")
        return
    
    # Create a progress bar and status area
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Upload the record with proper chunked process
    try:
        status_text.info("🔄 Starting upload process...")
        progress_bar.progress(10)
        
        # Step 1: Upload the image as a single chunk
        chunk_result = upload_chunk(
            token=st.session_state.user_token,
            chunk_data=image_data,
            filename=filename,
            chunk_index=0,
            total_chunks=1,
            upload_uuid=upload_uuid
        )
        
        if not chunk_result["success"]:
            status_text.error(f"❌ Image upload failed: {chunk_result['error']}")
            return
        
        progress_bar.progress(50)
        status_text.info("📝 Creating record with metadata...")
        
        # Step 2: Finalize the upload with metadata
        finalize_result = finalize_upload(
            token=st.session_state.user_token,
            title=title,
            description=full_description,
            category_id=category_id,
            user_id=st.session_state.user_id,
            media_type="image",
            upload_uuid=upload_uuid,
            filename=filename,
            total_chunks=1,
            language=language,
            release_rights=release_rights,
            latitude=latitude if latitude != 0 else None,
            longitude=longitude if longitude != 0 else None,
            use_uid_filename=True
        )
        
        if not finalize_result["success"]:
            status_text.error(f"❌ Record creation failed: {finalize_result['error']}")
            return
        
        progress_bar.progress(100)
        status_text.success("✅ Cultural heritage documented successfully!")
        
        # Show success details
        st.balloons()
        
        # Update contribution count
        if 'contributions' not in st.session_state:
            st.session_state.contributions = 0
        st.session_state.contributions += 1
        
        # Show what was uploaded - with proper error handling
        st.info(f"**Uploaded:** {title}")
        st.info(f"**Location:** {location}")
        
        # Get category name safely
        try:
            category_result = get_category_by_id(st.session_state.user_token, category_id)
            if category_result["success"]:
                category_name = category_result["data"].get("title", category_result["data"].get("name", "Unknown Category"))
                st.info(f"**Category:** {category_name}")
            else:
                st.info(f"**Category ID:** {category_id}")
        except:
            st.info(f"**Category ID:** {category_id}")
        
        # Clear the form after success
        time.sleep(2)
        st.session_state.captured_image = None
        st.experimental_rerun()
            
    except Exception as e:
        status_text.error(f"❌ Unexpected error: {str(e)}")
        progress_bar.progress(0)