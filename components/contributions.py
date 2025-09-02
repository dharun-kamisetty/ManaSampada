import streamlit as st
from utils.api_client import get_user_records
from utils.helpers import format_date, load_categories

def render_contributions_tab():
    """Render user contributions tab using our fixed categories"""
    st.markdown('<h2 class="sub-header">Your Cultural Heritage Contributions</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to view your contributions")
        return
    
    # Load our fixed categories
    load_categories()
    
    # Load user contributions
    if 'user_records' not in st.session_state or st.button("🔄 Refresh Contributions"):
        with st.spinner("Loading your contributions..."):
            contributions_data = get_user_records(
                st.session_state.user_token, 
                user_id=st.session_state.user_id,
                limit=20
            )
            if contributions_data["success"]:
                st.session_state.user_records = contributions_data["data"]
            else:
                st.session_state.user_records = []
                st.error(f"Failed to load contributions: {contributions_data['error']}")
    
    # Display contributions
    if st.session_state.get('user_records'):
        st.success(f"📊 You have contributed {len(st.session_state.user_records)} cultural heritage items!")
        display_contributions()
    else:
        st.info("You haven't made any contributions yet. Document your first heritage site!")
        
        if st.button("📸 Document Your First Heritage Site"):
            st.session_state.current_tab = "Document Heritage"
            st.experimental_rerun()

def display_contributions():
    """Display user contributions using our fixed categories"""
    for i, record in enumerate(st.session_state.user_records):
        with st.expander(f"{record.get('title', 'Untitled Heritage')}", expanded=i == 0):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Media Type:** {record.get('media_type', 'Unknown')}")
                
                # Use our enhanced category name lookup
                category_name = get_category_name(record.get('category_id'))
                st.markdown(f"**Category:** {category_name}")
                
                st.markdown(f"**Language:** {record.get('language', 'Unknown')}")
                st.markdown(f"**Status:** {record.get('status', 'pending').title()}")
            
            with col2:
                # Handle location data
                location = record.get('location')
                if location:
                    if isinstance(location, dict):
                        lat = location.get('latitude')
                        lon = location.get('longitude')
                        if lat is not None and lon is not None:
                            st.markdown(f"**Coordinates:** {lat:.6f}, {lon:.6f}")
                    else:
                        st.markdown(f"**Location:** {location}")
                
                st.markdown(f"**Uploaded:** {format_date(record.get('created_at'))}")
                
                if record.get('file_name'):
                    st.markdown(f"**File:** {record['file_name']}")
            
            # Description
            if record.get('description'):
                st.markdown("**Description:**")
                st.write(record['description'])
            
            # Additional fields
            if record.get('file_url'):
                st.markdown(f"**File URL:** [View File]({record['file_url']})")
            
            if record.get('duration_seconds'):
                mins = record['duration_seconds'] // 60
                secs = record['duration_seconds'] % 60
                st.markdown(f"**Duration:** {mins} minutes {secs} seconds")
            
            if record.get('release_rights'):
                st.markdown(f"**Usage Rights:** {record['release_rights'].title()}")
            
            st.markdown("---")


def get_category_name(category_id):
    """Convert category ID to category name using our fixed categories"""
    if not category_id:
        return "Uncategorized"
    
    # Check our fixed categories
    fixed_categories = {
        "ab7f2757-ccdf-4ef6-9850-2cdfe6e1b422": "Local History",
        "ab9fa2ce-1f83-4e91-b89d-cca18e8b301e": "Culture",
        "4366cab1-031e-4b37-816b-311ee34461a9": "Images", 
        "94a13c20-8a03-45da-8829-10e2fe1e61a1": "Architecture",
        "96e5104f-c786-4928-b932-f59f5b4ddbf0": "Places"
    }
    
    return fixed_categories.get(category_id, f"Category ({str(category_id)[:8]}...)")