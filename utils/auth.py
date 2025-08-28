import requests
from config import API_BASE_URL

def login_user(phone, password):
    """Authenticate user with password"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login",
            json={"phone": phone, "password": password},
            timeout=10
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
            return {"success": False, "error": f"Login failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def send_otp(phone_number):
    """Send OTP to the provided phone number"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login/send-otp",
            json={"phone_number": phone_number},
            timeout=10
        )
        
        if response.status_code == 200:
            return {"success": True, "message": "OTP sent successfully"}
        else:
            return {"success": False, "error": f"Failed to send OTP: {response.status_code} - {response.text}"}
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
            },
            timeout=10
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
            return {"success": False, "error": f"OTP verification failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def validate_token(token):
    """Validate if the token is still valid"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/users/me"
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=5
        )
        
        return response.status_code == 200
        
    except:
        return False