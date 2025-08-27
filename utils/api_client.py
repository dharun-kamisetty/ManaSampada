import requests
from config import API_BASE_URL

def get_user_by_id(token, user_id):
    """Get a specific user by ID"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
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

def get_user_contributions(token, user_id, media_type=None):
    """Get user contributions using the dedicated endpoint"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if media_type:
            endpoint = f"{API_BASE_URL}/api/v1/users/{user_id}/contributions/{media_type}"
        else:
            endpoint = f"{API_BASE_URL}/api/v1/users/{user_id}/contributions"
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Failed to get contributions: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def get_categories(token):
    """Get all available categories"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/categories"
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Failed to get categories: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def create_monument_record(token, title, description, location, latitude=None, longitude=None, category_id=None, tags=None):
    """Create a monument record"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "title": title,
            "description": description,
            "location": location,
            "type": "monument",
            "media_type": "image_audio"
        }
        
        if latitude and longitude:
            payload["latitude"] = latitude
            payload["longitude"] = longitude
        
        if category_id:
            payload["category_id"] = category_id
        
        if tags:
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(",")]
            payload["tags"] = tags
        
        endpoint = f"{API_BASE_URL}/api/v1/records/"
        
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            return {"success": True, "data": data, "record_id": data.get("id")}
        else:
            return {"success": False, "error": f"Failed to create record: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def upload_monument_files(token, record_id, image_file, audio_file):
    """Upload files for a monument record"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        files = {
            'image': ('monument.jpg', image_file, 'image/jpeg'),
            'audio': ('recording.webm', audio_file, 'audio/webm')
        }
        
        endpoints = [
            f"{API_BASE_URL}/api/v1/records/{record_id}/upload",
            f"{API_BASE_URL}/api/v1/records/upload",
            f"{API_BASE_URL}/api/v1/records/{record_id}/files"
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.post(
                    endpoint,
                    files=files,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    return {"success": True, "message": "Files uploaded successfully!"}
                elif response.status_code != 404:
                    return {"success": False, "error": f"Upload failed: {response.status_code} - {response.text}"}
            except:
                continue
        
        return {"success": False, "error": "All endpoint attempts failed"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def process_audio(task_token, record_id):
    """Start audio processing for a record"""
    try:
        headers = {
            "Authorization": f"Bearer {task_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/tasks/process-audio/{record_id}"
        
        response = requests.post(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            data = response.json()
            return {"success": True, "data": data, "task_id": data.get("task_id")}
        else:
            return {"success": False, "error": f"Failed to start audio processing: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def analyze_content(task_token, record_id):
    """Start content analysis for a record"""
    try:
        headers = {
            "Authorization": f"Bearer {task_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/tasks/analyze-content/{record_id}"
        
        response = requests.post(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 202]:
            data = response.json()
            return {"success": True, "data": data, "task_id": data.get("task_id")}
        else:
            return {"success": False, "error": f"Failed to start content analysis: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}