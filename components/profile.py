import streamlit as st
from utils.api_client import get_user_by_id, get_user_records
from utils.helpers import format_date

def render_profile_tab():
    """Render the user profile tab"""
    st.markdown('<h2 class="sub-header">Your Profile</h2>', unsafe_allow_html=True)
    
    if not st.session_state.authenticated:
        st.warning("Please login to view your profile")
        return
    
    # Load profile data
    load_profile_data()
    
    # Display profile
    render_profile_info()

def load_profile_data():
    """Load user profile data"""
    if 'user_profile' not in st.session_state or st.button("Refresh Profile"):
        with st.spinner("Loading your profile..."):
            profile_data = get_user_by_id(st.session_state.user_token, st.session_state.user_id)
            
            if profile_data["success"]:
                st.session_state.user_profile = profile_data["data"]
            else:
                st.error(f"Failed to load profile: {profile_data['error']}")
                st.session_state.user_profile = {}


def render_profile_info():
    """Render user profile information"""
    user_data = st.session_state.get('user_profile', {})
    
    # DEBUG: Show what we're trying to display
    st.write("User Data to Display:", user_data)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Profile Information")
        
        # Display user details - handle missing data gracefully
        st.markdown(f"**Name:** {user_data.get('name', st.session_state.get('name'))}")
        st.markdown(f"**Phone:** {user_data.get('phone', st.session_state.get('phone', 'Not provided'))}")
        st.markdown(f"**Email:** {user_data.get('email', 'Not provided')}")
        st.markdown(f"**User ID:** `{user_data.get('id', st.session_state.get('user_id', 'N/A'))}`")

        
        # Contribution count
        contributions = len(st.session_state.get('user_records', []))
        st.markdown(f"**Contributions:** {contributions}")
        
        # Member since
        if user_data.get('created_at'):
            st.markdown(f"**Member since:** {format_date(user_data.get('created_at'))}")
        
        # Login method
        st.markdown(f"**Login method:** {st.session_state.get('login_method', 'Unknown')}")
    
    with col2:
        st.subheader("Additional Information")
        
        # Display additional user info if available
        if user_data.get('gender'):
            st.markdown(f"**Gender:** {user_data['gender']}")
        if user_data.get('date_of_birth'):
            st.markdown(f"**Date of Birth:** {user_data['date_of_birth']}")
        if user_data.get('place'):
            st.markdown(f"**Place:** {user_data['place']}")
        if user_data.get('last_login_at'):
            st.markdown(f"**Last Login:** {format_date(user_data['last_login_at'])}")
        
        st.markdown("---")
        st.subheader("Account Actions")
        
        if st.button("🔄 Refresh All Data"):
            # Clear cached data
            for key in ['user_profile', 'user_records', 'categories']:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()