import streamlit as st
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

def render_features_preview():
    """Render features preview for non-authenticated users"""
    st.markdown('<h2 class="sub-header">Welcome to Swecha-Kosam</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p>Join us in preserving Telugu cultural heritage for future generations.</p>
        <p>Document monuments, record stories, and help build a rich cultural archive.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Document Monuments")
        st.markdown("Capture photos and record descriptions of cultural sites")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Leaderboard")
        st.markdown("See top contributors and track your progress")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Discover")
        st.markdown("Explore documented monuments and stories")
        st.markdown('</div>', unsafe_allow_html=True)

# Additional helper functions for login would go here...