import streamlit as st
from utils.api_client import get_user_records
from utils.helpers import format_date

def render_contributions_tab():
    """Render user contributions tab"""
    st.markdown('<h2 class="sub-header">Your Cultural Heritage Contributions</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to view your contributions")
        return
    
    # Load user contributions
    if 'user_records' not in st.session_state or st.button("Refresh Contributions"):
        with st.spinner("Loading your contributions..."):
            from utils.api_client import get_user_records
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
        st.success(f"You have contributed {len(st.session_state.user_records)} cultural heritage items!")
        display_contributions()
    else:
        st.info("You haven't made any contributions yet. Document your first heritage site in the 'Document Heritage' tab!")

def display_contributions():
    """Display user contributions in a nice format"""
    for i, record in enumerate(st.session_state.user_records):
        with st.expander(f"{record.get('title', 'Untitled Heritage')}", expanded=i == 0):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Type:** {record.get('media_type', 'Unknown')}")
                st.markdown(f"**Category:** {record.get('category_name', 'Unknown')}")
                st.markdown(f"**Language:** {record.get('language', 'Unknown')}")
            
            with col2:
                if record.get('location'):
                    st.markdown(f"**Location:** {record['location']}")
                st.markdown(f"**Uploaded:** {format_date(record.get('created_at'))}")
                if record.get('status'):
                    st.markdown(f"**Status:** {record['status']}")
            
            if record.get('description'):
                st.markdown("**Description:**")
                st.write(record['description'])
            
            st.markdown("---")