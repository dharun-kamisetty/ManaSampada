import streamlit as st
import time
from utils.auth import login_user, send_otp, verify_otp

def render_login_forms():
    """Render login forms (password and OTP)"""
    if not st.session_state.authenticated:
        login_tab, otp_tab = st.tabs(["Password Login", "OTP Login"])
        
        with login_tab:
            render_password_login()
        
        with otp_tab:
            render_otp_login()
        
        render_features_preview()
    else:
        st.success(f"Welcome back, {st.session_state.phone}!")

def render_password_login():
    """Render password login form"""
    st.markdown('<div class="login-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Password Login</h2>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        phone = st.text_input("Phone Number", placeholder="Enter your registered phone number")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            handle_password_login(phone, password)
    st.markdown('</div>', unsafe_allow_html=True)

def render_otp_login():
    """Render OTP login form"""
    st.markdown('<div class="login-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">OTP Login</h2>', unsafe_allow_html=True)
    
    if not st.session_state.otp_sent:
        render_otp_request()
    else:
        render_otp_verification()
    st.markdown('</div>', unsafe_allow_html=True)

def render_otp_request():
    """Render OTP request form"""
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
                        st.success("OTP sent successfully!")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to send OTP: {result['error']}")
            else:
                st.warning("Please enter your phone number")

def render_otp_verification():
    """Render OTP verification form"""
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
                        
                        # Clear any cached data
                        if 'categories' in st.session_state:
                            del st.session_state.categories
                        if 'user_records' in st.session_state:
                            del st.session_state.user_records
                        if 'user_profile' in st.session_state:
                            del st.session_state.user_profile
                        
                        st.success("Login successful!")
                        time.sleep(1)
                        st.experimental_rerun()
                    else:
                        st.error(f"OTP verification failed: {result['error']}")
            else:
                if not otp_code:
                    st.warning("Please enter the OTP")
                if not consent:
                    st.warning("Please consent to the terms and conditions")
    
    if st.button("Request New OTP"):
        st.session_state.otp_sent = False
        st.experimental_rerun()

def handle_password_login(phone, password):
    """Handle password login submission"""
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
                
                # Clear any cached data
                if 'categories' in st.session_state:
                    del st.session_state.categories
                if 'user_records' in st.session_state:
                    del st.session_state.user_records
                if 'user_profile' in st.session_state:
                    del st.session_state.user_profile
                
                st.success("Login successful!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error(f"Login failed: {result['error']}")
    else:
        st.warning("Please enter both phone number and password")

def render_features_preview():
    """Render features preview for non-authenticated users"""
    st.markdown('<h2 class="sub-header">Welcome to Swecha-Kosam</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p>Preserve cultural heritage by documenting temples, mosques, churches, and other significant places.</p>
        <p>Capture images, record audio descriptions, and share your cultural discoveries.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Capture Heritage")
        st.markdown("Document cultural sites with photos and descriptions")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎙️ Record Stories")
        st.markdown("Preserve oral histories and cultural narratives")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🌍 Share Culture")
        st.markdown("Contribute to a growing database of cultural heritage")
        st.markdown('</div>', unsafe_allow_html=True)