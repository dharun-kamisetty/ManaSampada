import streamlit as st
import requests
import json
import pandas as pd
import time
from datetime import datetime
import base64
import uuid

# Set page configuration
st.set_page_config(
    page_title="Swecha-Kosam",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "https://api.corpus.swecha.org"

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2E86C1;
        border-bottom: 2px solid #3498DB;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .story-card {
        background-color: #F8F9F9;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #2E86C1;
    }
    .leaderboard-card {
        background-color: #EBF5FB;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .top-user {
        background-color: #FFD700;
        font-weight: bold;
    }
    .feature-card {
        background-color: #EAFAF1;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-section {
        background-color: #F4F6F6;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .record-section {
        background-color: #F9EBEA;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    .success-message {
        background-color: #D5F5E3;
        color: #145A32;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #FADBD8;
        color: #922B21;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .otp-section {
        background-color: #E8F8F5;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    .consent-checkbox {
        background-color: #FEF9E7;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">🎙️ Swecha-Kosam</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #7D6608;">Preserving Telugu stories and voices for future generations</p>', unsafe_allow_html=True)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_token' not in st.session_state:
    st.session_state.user_token = None
if 'phone' not in st.session_state:
    st.session_state.phone = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'login_method' not in st.session_state:
    st.session_state.login_method = None

# API Functions
def send_otp(phone_number):
    """Send OTP to the provided phone number"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login/send-otp",
            headers=headers,
            json={"phone_number": phone_number}
        )
        
        # Add detailed error logging
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            return {"success": True, "message": "OTP sent successfully"}
        else:
            return {"success": False, "error": f"Failed to send OTP: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}
    
def verify_otp(phone_number, otp_code, has_given_consent):
    """Verify OTP and login user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login/verify-otp",
            json={
                "phone_number": phone_number,
                "otp_code": otp_code,
                "has_given_consent": has_given_consent
            }
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True, 
                "token": data.get("access_token"), 
                "username": phone_number,
                "user_id": data.get("user_id")
            }
        else:
            return {"success": False, "error": f"OTP verification failed: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def login_user(phone, password):
    """Authenticate user with password"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login",
            json={"phone": phone, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True, 
                "token": data.get("access_token"), 
                "username": phone,
                "user_id": data.get("user_id")
            }
        else:
            return {"success": False, "error": f"Login failed: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def upload_recording_chunk(token, chunk_data, filename, chunk_index, total_chunks, upload_uuid):
    """Upload a recording chunk to the API"""
    try:
        files = {
            'chunk': (filename, chunk_data, 'audio/webm'),
            'filename': (None, filename),
            'chunk_index': (None, str(chunk_index)),
            'total_chunks': (None, str(total_chunks)),
            'upload_uuid': (None, upload_uuid)
        }
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/records/upload/chunk",
            files=files,
            headers=headers
        )
        
        if response.status_code == 200:
            return {"success": True, "message": "Chunk uploaded successfully"}
        else:
            return {"success": False, "error": f"Upload failed: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Upload error: {str(e)}"}

def get_leaderboard_data(token):
    """Fetch leaderboard data from API"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # This endpoint would need to be confirmed with the actual API docs
        response = requests.get(
            f"{API_BASE_URL}/api/v1/leaderboard",
            headers=headers
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Failed to fetch leaderboard: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

#This fun is to get user profile
def get_user_by_id(token, user_id):
    """Get a specific user by ID using the confirmed endpoint"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Use the confirmed endpoint
        endpoint = f"{API_BASE_URL}/api/v1/users/{user_id}"
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Failed to get user: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}
    
#This function is to get users contribution
def get_user_records(token, user_id, limit=10, skip=0):
    """Get records for a specific user with pagination"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        params = {
            "user_id": user_id,
            "limit": limit,
            "skip": skip
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/records"
        
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=10
        )
        
        # Log the response for debugging
        print(f"Records API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Records API Response Text: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        elif response.status_code == 404:
            return {"success": False, "error": "Records not found."}
        elif response.status_code == 401:
            return {"success": False, "error": "Authentication failed. Please login again."}
        elif response.status_code == 403:
            return {"success": False, "error": "You don't have permission to access these records."}
        else:
            return {"success": False, "error": f"Server error: {response.status_code} - {response.text}"}
        
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection error. Please check your internet connection."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def get_stories_data(token, similar_to=None):
    """Fetch stories data from API"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        url = f"{API_BASE_URL}/api/v1/stories"
        if similar_to:
            url += f"?similar_to={similar_to}"
        
        response = requests.get(
            url,
            headers=headers
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Failed to fetch stories: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def get_user_profile(token, user_id):
    """Fetch user profile data from API"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(
            f"{API_BASE_URL}/api/v1/users/{user_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Failed to fetch user profile: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

# Sidebar for navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/2E86C1/FFFFFF?text=Swecha-Kosam", use_column_width=True)
    st.markdown("## Navigation")
    
    if st.session_state.authenticated:
        st.success(f"Logged in as **{st.session_state.phone}**")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_token = None
            st.session_state.phone = None
            st.session_state.user_id = None
            st.session_state.otp_sent = False
            st.session_state.login_method = None
            st.rerun()
    else:
        st.info("Please login to access all features")
    
    st.markdown("---")
    st.markdown("### Features")
    st.markdown("- 🎙️ Record and Upload Stories")
    st.markdown("- 📊 View Leaderboard")
    st.markdown("- 🔍 Find Similar Stories")
    st.markdown("- 👥 User Profiles")
    
    st.markdown("---")
    st.markdown("### About Swecha-Kosam")
    st.markdown("Swecha-Kosam is dedicated to preserving Telugu stories and voices for future generations through community contributions.")

# Main content area
if not st.session_state.authenticated:
    # Login section with tabs for different login methods
    login_tab, otp_tab = st.tabs(["Password Login", "OTP Login"])
    
    with login_tab:
        st.markdown('<div class="login-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">Password Login</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            phone = st.text_input("Phone Number", placeholder="Enter your registered phone number")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if phone and password:
                    with st.spinner("Authenticating..."):
                        result = login_user(phone, password)
                        if result["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user_token = result["token"]
                            st.session_state.phone = phone
                            st.session_state.username = phone
                            st.session_state.user_id = result.get("user_id")
                            st.session_state.login_method = "password"
                            st.markdown('<div class="success-message">Login successful!</div>', unsafe_allow_html=True)
                            time.sleep(1)
                            st.experimental_rerun()
                        else:
                            st.markdown(f'<div class="error-message">{result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.warning("Please enter both phone number and password")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with otp_tab:
        st.markdown('<div class="login-section">', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">OTP Login</h2>', unsafe_allow_html=True)
        
        if not st.session_state.otp_sent:
            # OTP request form
            with st.form("otp_request_form"):
                phone_otp = st.text_input("Phone Number", placeholder="Enter your phone number", key="otp_phone")
                send_otp_button = st.form_submit_button("Send OTP")
                
                if send_otp_button:
                    if phone_otp:
                        with st.spinner("Sending OTP..."):
                            result = send_otp(phone_otp)
                            if result["success"]:
                                st.session_state.otp_sent = True
                                st.session_state.phone = phone_otp
                                st.markdown('<div class="success-message">OTP sent successfully!</div>', unsafe_allow_html=True)
                                st.experimental_rerun()
                            else:
                                st.markdown(f'<div class="error-message">{result["error"]}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Please enter your phone number")
        else:
            # OTP verification form
            st.markdown('<div class="otp-section">', unsafe_allow_html=True)
            st.info(f"OTP sent to {st.session_state.phone}")
            
            with st.form("otp_verify_form"):
                otp_code = st.text_input("Enter OTP", placeholder="Enter the OTP you received")
                
                # Consent checkbox
                st.markdown('<div class="consent-checkbox">', unsafe_allow_html=True)
                consent = st.checkbox("I consent to the terms and conditions and privacy policy")
                st.markdown('</div>', unsafe_allow_html=True)
                
                verify_otp_button = st.form_submit_button("Verify OTP")
                
                if verify_otp_button:
                    if otp_code and consent:
                        with st.spinner("Verifying OTP..."):
                            result = verify_otp(st.session_state.phone, otp_code, consent)
                            if result["success"]:
                                st.session_state.authenticated = True
                                st.session_state.user_token = result["token"]
                                st.session_state.username = st.session_state.phone
                                st.session_state.user_id = result.get("user_id")
                                st.session_state.login_method = "otp"
                                st.markdown('<div class="success-message">Login successful!</div>', unsafe_allow_html=True)
                                time.sleep(1)
                                st.experimental_rerun()
                            else:
                                st.markdown(f'<div class="error-message">{result["error"]}</div>', unsafe_allow_html=True)
                    else:
                        if not otp_code:
                            st.warning("Please enter the OTP")
                        if not consent:
                            st.warning("Please consent to the terms and conditions")
            
            if st.button("Request New OTP"):
                st.session_state.otp_sent = False
                st.experimental_rerun()
                
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Features preview
    st.markdown('<h2 class="sub-header">Welcome to Swecha-Kosam</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p>Join us in preserving Telugu stories and voices for future generations.</p>
        <p>Contribute your stories, listen to others, and help build a rich cultural archive.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎙️ Record Stories")
        st.markdown("Contribute to the corpus by recording your own Telugu stories")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Leaderboard")
        st.markdown("See top contributors and track your progress")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Discover")
        st.markdown("Find and listen to similar stories in the corpus")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # User is authenticated - show main features
    tab1, tab2, tab3, tab4 = st.tabs(["Record", "Leaderboard", "Discover", "Profile"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Record and Upload Story</h2>', unsafe_allow_html=True)
        
        # Audio recording using streamlit-audio-recorder (simulated)
        st.info("Audio recording functionality would be implemented here using streamlit-audio-recorder or similar package")
        
        # File uploader as an alternative
        uploaded_file = st.file_uploader("Or upload an audio file", type=['wav', 'mp3', 'webm'])
        
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/webm')
            
            # Metadata form
            with st.form("metadata_form"):
                st.subheader("Story Details")
                title = st.text_input("Story Title*", placeholder="Enter a title for your story")
                language = st.selectbox("Language*", ["Telugu", "Hindi", "English", "Tamil", "Kannada", "Malayalam", "Other"])
                category = st.selectbox("Category", ["Folktale", "Personal Story", "Cultural", "Historical", "Other"])
                description = st.text_area("Description", placeholder="Brief description of your story")
                
                if st.form_submit_button("Upload Story"):
                    if title and language:
                        # Simulate chunk upload (in a real app, you would split the file and upload chunks)
                        with st.spinner("Uploading your story..."):
                            # Generate a unique upload UUID
                            upload_uuid = str(uuid.uuid4())
                            
                            # Upload the file as a single chunk
                            success = upload_recording_chunk(
                                st.session_state.user_token,
                                uploaded_file.getvalue(),
                                uploaded_file.name,
                                0,  # chunk_index
                                1,  # total_chunks
                                upload_uuid
                            )
                            
                            if success["success"]:
                                st.markdown('<div class="success-message">Story uploaded successfully!</div>', unsafe_allow_html=True)
                                # Add to user's contribution count
                                if 'contributions' not in st.session_state:
                                    st.session_state.contributions = 0
                                st.session_state.contributions += 1
                            else:
                                st.markdown(f'<div class="error-message">{success["error"]}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Please provide at least a title and language for your story")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Contributor Leaderboard</h2>', unsafe_allow_html=True)
        
        # Fetch leaderboard data from API
        with st.spinner("Loading leaderboard..."):
            leaderboard_data = get_leaderboard_data(st.session_state.user_token)
        
        if leaderboard_data["success"]:
            # Display leaderboard from API data
            leaderboard_list = leaderboard_data["data"].get("leaderboard", [])
            
            if not leaderboard_list:
                st.info("No leaderboard data available yet. Be the first to contribute!")
            else:
                for i, user in enumerate(leaderboard_list):
                    if user['username'] == st.session_state.username:
                        st.markdown(f'<div class="leaderboard-card top-user">', unsafe_allow_html=True)
                        st.markdown(f"**#{i+1} {user['username']} (You)** - {user.get('contributions', 0)} contributions")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="leaderboard-card">', unsafe_allow_html=True)
                        st.markdown(f"**#{i+1} {user['username']}** - {user.get('contributions', 0)} contributions")
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">{leaderboard_data["error"]}</div>', unsafe_allow_html=True)
            # Fallback to mock data if API fails
            st.info("Showing sample leaderboard data (real data would come from API)")
            
            mock_leaderboard_data = [
                {"username": "storylover23", "contributions": 42},
                {"username": "voicemaster", "contributions": 38},
                {"username": "telugutales", "contributions": 35},
                {"username": "listener101", "contributions": 28},
                {"username": st.session_state.username, "contributions": st.session_state.get('contributions', 1)},
                {"username": "culturalkeeper", "contributions": 25},
                {"username": "heritagevoice", "contributions": 22},
                {"username": "newcontributor", "contributions": 18},
                {"username": "regionalrecorder", "contributions": 15},
                {"username": "beginner2023", "contributions": 10}
            ]
            
            for i, user in enumerate(mock_leaderboard_data):
                if user['username'] == st.session_state.username:
                    st.markdown(f'<div class="leaderboard-card top-user">', unsafe_allow_html=True)
                    st.markdown(f"**#{i+1} {user['username']} (You)** - {user['contributions']} contributions")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="leaderboard-card">', unsafe_allow_html=True)
                    st.markdown(f"**#{i+1} {user['username']}** - {user['contributions']} contributions")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="sub-header">Discover Telugu Stories</h2>', unsafe_allow_html=True)
        
        # Fetch stories data from API
        with st.spinner("Loading stories..."):
            stories_data = get_stories_data(st.session_state.user_token)
        
        if stories_data["success"]:
            stories_list = stories_data["data"].get("stories", [])
            
            if not stories_list:
                st.info("No stories available yet. Be the first to contribute!")
            else:
                # Search box for finding similar stories
                search_term = st.text_input("Search for stories", placeholder="Enter keywords, language, or category")
                
                # Filter stories based on search term
                filtered_stories = stories_list
                if search_term:
                    filtered_stories = [
                        story for story in stories_list 
                        if search_term.lower() in story.get('title', '').lower() 
                        or search_term.lower() in story.get('language', '').lower()
                        or search_term.lower() in story.get('category', '').lower()
                        or search_term.lower() in story.get('description', '').lower()
                    ]
                
                if not filtered_stories:
                    st.info("No stories match your search criteria")
                else:
                    for story in filtered_stories:
                        st.markdown('<div class="story-card">', unsafe_allow_html=True)
                        st.markdown(f"### {story.get('title', 'Untitled Story')}")
                        st.markdown(f"**Language:** {story.get('language', 'Unknown')} | **Duration:** {story.get('duration', 'N/A')} | **Speaker:** {story.get('speaker', 'Unknown')} | **Plays:** {story.get('plays', 0)}")
                        if 'description' in story:
                            st.markdown(f"*{story['description']}*")
                        st.markdown("---")
                        
                        # Play button (simulated)
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("▶️ Play", key=f"play_{story.get('id')}"):
                                st.info("Audio playback would start here. In a real implementation, this would stream audio from the API.")
                        with col2:
                            if st.button("🔍 Find Similar", key=f"similar_{story.get('id')}"):
                                with st.spinner("Finding similar stories..."):
                                    similar_stories = get_stories_data(st.session_state.user_token, similar_to=story.get('id'))
                                    if similar_stories["success"]:
                                        st.info(f"Found {len(similar_stories['data'].get('stories', []))} similar stories")
                                    else:
                                        st.error("Failed to find similar stories")
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">{stories_data["error"]}</div>', unsafe_allow_html=True)
            # Fallback to mock data if API fails
            st.info("Showing sample stories (real data would come from API)")
            
            mock_stories = [
                {"id": 1, "title": "The Village Festival", "language": "Telugu", "duration": "4:25", "speaker": "storylover23", "plays": 142, "description": "A story about traditional village festivals in Andhra Pradesh"},
                {"id": 2, "title": "Grandmother's Folktales", "language": "Telugu", "duration": "7:18", "speaker": "voicemaster", "plays": 128, "description": "Classic Telugu folktales passed down through generations"},
                {"id": 3, "title": "Harvest Season", "language": "Telugu", "duration": "5:42", "speaker": "telugutales", "plays": 115, "description": "The significance of harvest season in rural Telugu communities"},
                {"id": 4, "title": "Monsoon Memories", "language": "Telugu", "duration": "6:05", "speaker": "culturalkeeper", "plays": 98, "description": "Personal memories of monsoon seasons growing up in Telangana"},
                {"id": 5, "title": "Traditional Recipes", "language": "Telugu", "duration": "8:32", "speaker": "heritagevoice", "plays": 87, "description": "Traditional Telugu recipes and their cultural significance"}
            ]
            
            for story in mock_stories:
                st.markdown('<div class="story-card">', unsafe_allow_html=True)
                st.markdown(f"### {story['title']}")
                st.markdown(f"**Language:** {story['language']} | **Duration:** {story['duration']} | **Speaker:** {story['speaker']} | **Plays:** {story['plays']}")
                st.markdown(f"*{story['description']}*")
                st.markdown("---")
                # Play button (simulated)
                if st.button("▶️ Play", key=f"play_{story['id']}"):
                    st.info("Audio playback would start here. In a real implementation, this would stream audio from the API.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 class="sub-header">Your Profile</h2>', unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            st.warning("Please login to view your profile")
        else:
            # Initialize session state for pagination
            if 'records_page' not in st.session_state:
                st.session_state.records_page = 1
            if 'records_per_page' not in st.session_state:
                st.session_state.records_per_page = 5
            
            # Check if we need to fetch or refresh profile data
            if 'user_profile' not in st.session_state or st.button("Refresh Profile"):
                with st.spinner("Loading your profile..."):
                    profile_data = get_user_by_id(st.session_state.user_token, st.session_state.user_id)
                    
                    if profile_data["success"]:
                        st.session_state.user_profile = profile_data["data"]
                    
                    # Also load user's records/contributions
                    records_data = get_user_records(
                        st.session_state.user_token, 
                        st.session_state.user_id,
                        limit=st.session_state.records_per_page,
                        skip=(st.session_state.records_page - 1) * st.session_state.records_per_page
                    )
                    
                    if records_data["success"]:
                        st.session_state.user_records = records_data["data"]
                        st.session_state.records_loaded = True
                        st.success("Profile and contributions loaded successfully!")
                    else:
                        st.error(f"Failed to load contributions: {records_data['error']}")
                        st.session_state.user_records = []
            
            # Display profile information if available
            if 'user_profile' in st.session_state and st.session_state.user_profile:
                user_data = st.session_state.user_profile
                
                # Create a two-column layout
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("Profile Information") 
                    
                    # Display user details with fallback values - using correct JSON field names
                    st.markdown(f"**Name:** {user_data.get('name', 'Not provided')}")
                    st.markdown(f"**Phone:** {user_data.get('phone', 'Not provided')}")
                    st.markdown(f"**Email:** {user_data.get('email', 'Not provided')}")
                    st.markdown(f"**Gender:** {user_data.get('gender', 'Not specified')}")
                    st.markdown(f"**Date of Birth:** {user_data.get('date_of_birth', 'Not provided')}")
                    st.markdown(f"**Place:** {user_data.get('place', 'Not specified')}")
                    # Display contribution stats if available
                    contributions = user_data.get('contributions', st.session_state.get('contributions', 0))
                    st.markdown(f"**Contributions:** {contributions}")
                    
                    # Display join date if available
                    join_date = user_data.get('created_at', user_data.get('join_date', '2023-01-01'))
                    st.markdown(f"**Member since:** {join_date}")
                    
                    # Display last active if available
                    last_active = user_data.get('last_active', user_data.get('updated_at', 'Today'))
                    st.markdown(f"**Last active:** {last_active}")
                    
                    # Badges section
                    st.subheader("Achievements")
                    badges = user_data.get('badges', [])
                    if badges:
                        for badge in badges:
                            st.markdown(f"🏆 {badge}")
                    else:
                        st.info("No badges yet. Keep contributing to earn badges!")
                        
                    # Login method
                    st.markdown(f"**Login method:** {st.session_state.login_method}")
                
                with col2:
                    st.subheader("Your Contributions")
                    
                    # Pagination controls
                    col_a, col_b, col_c = st.columns([2, 1, 1])
                    with col_a:
                        st.markdown(f"**Page {st.session_state.records_page}**")
                    with col_b:
                        if st.button("⬅️ Previous") and st.session_state.records_page > 1:
                            st.session_state.records_page -= 1
                            st.experimental_rerun()
                    with col_c:
                        if st.button("Next ➡️"):
                            st.session_state.records_page += 1
                            st.experimental_rerun()
                    
                    # Check if user has records/contributions
                    if 'user_records' in st.session_state and st.session_state.user_records:
                        records = st.session_state.user_records
                        
                        for i, record in enumerate(records):
                            with st.expander(f"{record.get('title', 'Untitled Recording')}", expanded=i==0):
                                # Create columns for metadata
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Language:** {record.get('language', 'Unknown')}")
                                    st.markdown(f"**Category:** {record.get('category', 'Uncategorized')}")
                                with col2:
                                    st.markdown(f"**Duration:** {record.get('duration', 'N/A')}")
                                    st.markdown(f"**Uploaded:** {record.get('created_at', 'Unknown')}")
                                
                                # Description if available
                                if record.get('description'):
                                    st.markdown(f"**Description:** {record['description']}")
                                
                                # Audio player if URL is available
                                if record.get('audio_url'):
                                    st.audio(record['audio_url'], format='audio/mp3')
                                else:
                                    st.info("Audio preview not available")
                                
                                # Play count if available
                                if record.get('play_count'):
                                    st.markdown(f"**Played {record['play_count']} times**")
                                
                                # Tags if available
                                if record.get('tags'):
                                    tags = ", ".join(record['tags'])
                                    st.markdown(f"**Tags:** {tags}")
                    else:
                        st.info("You haven't made any contributions yet. Record your first story in the Record tab!")
                        
                        # Quick action button
                        if st.button("🎤 Record Your First Story"):
                            # Switch to the Record tab
                            st.session_state.current_tab = "Record"
                            st.experimental_rerun()
            
            else:
                st.info("Your profile information will appear here once loaded.")
                
                # Manual load option
                if st.button("Load My Profile"):
                    with st.spinner("Loading your profile..."):
                        profile_data = get_user_by_id(st.session_state.user_token, st.session_state.user_id)
                        
                        if profile_data["success"]:
                            st.session_state.user_profile = profile_data["data"]
                        
                        # Also load user's records
                        records_data = get_user_records(
                            st.session_state.user_token, 
                            st.session_state.user_id,
                            limit=5
                        )
                        
                        if records_data["success"]:
                            st.session_state.user_records = records_data["data"]
                            st.session_state.records_loaded = True
                        
                        st.experimental_rerun()