import streamlit as st
from utils.api_client import get_user_by_id, get_user_contributions
from utils.helpers import format_date

def render_profile_tab():
    """Render the user profile tab"""
    st.markdown('<h2 class="sub-header">Your Profile</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to view your profile")
        return
    
    # Load profile data if needed
    load_profile_data()
    
    # Display profile
    render_profile_info()
    render_contributions()

def load_profile_data():
    """Load user profile and contributions data"""
    if 'user_profile' not in st.session_state or st.button("Refresh Profile"):
        with st.spinner("Loading your profile..."):
            # Load user profile
            profile_data = get_user_by_id(st.session_state.user_token, st.session_state.user_id)
            if profile_data["success"]:
                st.session_state.user_profile = profile_data["data"]
            
            # Load user contributions
            contributions_data = get_user_contributions(
                st.session_state.user_token, 
                st.session_state.user_id,
                media_type="monument"
            )
            if contributions_data["success"]:
                st.session_state.user_records = contributions_data["data"]
                st.session_state.records_loaded = True
            else:
                st.error(f"Failed to load contributions: {contributions_data['error']}")
                st.session_state.user_records = []

def render_profile_info():
    """Render user profile information"""
    user_data = st.session_state.user_profile
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Information")
        render_user_details(user_data)
        render_achievements(user_data)
    
    with col2:
        st.subheader("Your Contributions")
        render_user_contributions()

def render_user_details(user_data):
    """Render user details section"""
    st.markdown(f"**Name:** {user_data.get('name', 'Not provided')}")
    st.markdown(f"**Phone:** {user_data.get('phone', st.session_state.phone)}")
    st.markdown(f"**Email:** {user_data.get('email', 'Not provided')}")
    st.markdown(f"**Gender:** {user_data.get('gender', 'Not specified')}")
    st.markdown(f"**Date of Birth:** {format_date(user_data.get('date_of_birth'))}")
    st.markdown(f"**Place:** {user_data.get('place', 'Not specified')}")
    st.markdown(f"**Member since:** {format_date(user_data.get('created_at'))}")
    st.markdown(f"**Last active:** {format_date(user_data.get('last_login_at'))}")

# Additional helper functions for profile would go here...