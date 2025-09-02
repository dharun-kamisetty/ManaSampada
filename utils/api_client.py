import requests
import uuid
from config import API_BASE_URL
import os

def get_categories(token):
    """Get all available categories"""
    if not token:
        return {"success": False, "error": "No authentication token provided"}
    
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

def get_category_by_id(token, category_id):
    """Get a specific category by ID with better error handling"""
    if not token:
        return {"success": False, "error": "No authentication token provided"}
    
    if not category_id:
        return {"success": False, "error": "No category ID provided"}
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/categories/{category_id}"
        
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Failed to get category: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}
    
def upload_chunk(token, chunk_data, filename, chunk_index, total_chunks, upload_uuid):
    """Upload a file chunk to the API (only binary data)"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Prepare form data for chunk upload - CORRECTED parameter name to upload_uuid
        files = {
            'chunk': (filename, chunk_data, 'application/octet-stream'),
            'chunk_index': (None, str(chunk_index)),
            'total_chunks': (None, str(total_chunks)),
            'upload_uuid': (None, upload_uuid),  # CORRECTED: Changed from upload_usid to upload_uuid
            'filename': (None, filename)
        }
        
        endpoint = f"{API_BASE_URL}/api/v1/records/upload/chunk"
        
        response = requests.post(
            endpoint,
            files=files,
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            return {"success": True, "message": "Chunk uploaded successfully", "data": response.json()}
        else:
            return {"success": False, "error": f"Chunk upload failed: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def finalize_upload(token, title, description, category_id, user_id, media_type, 
                   upload_uuid, filename, total_chunks, language, release_rights="creator",
                   latitude=None, longitude=None, use_uid_filename=True):
    """Finalize the upload and create the record with metadata"""
    try:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        # Prepare form data with CORRECT enum values
        data = {
            "title": title,
            "description": description,
            "category_id": category_id,
            "user_id": user_id,
            "media_type": media_type,  # Should be: 'text', 'audio', 'video' or 'image'
            "upload_uuid": upload_uuid,
            "filename": filename,
            "total_chunks": total_chunks,
            "language": language,  # Should be Indian language codes
            "release_rights": release_rights,  # Should be: 'creator', 'family_or_friend', 'downloaded' or 'NA'
            "use_uid_filename": str(use_uid_filename).lower()
        }
        
        # Add optional fields
        if latitude is not None:
            data["latitude"] = str(latitude)
        if longitude is not None:
            data["longitude"] = str(longitude)
        
        endpoint = f"{API_BASE_URL}/api/v1/records/upload"
        
        response = requests.post(
            endpoint,
            data=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            return {"success": True, "message": "Record created successfully", "data": response.json()}
        else:
            return {"success": False, "error": f"Record creation failed: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}
    
def get_user_records(token, user_id=None, category_id=None, media_type=None, skip=0, limit=100):
    """Get records with filtering options - FIXED VERSION"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        params = {
            "skip": skip,
            "limit": limit
        }
        
        # Add optional filters
        if user_id:
            params["user_id"] = user_id
        if category_id:
            params["category_id"] = category_id
        if media_type:
            params["media_type"] = media_type
        
        endpoint = f"{API_BASE_URL}/api/v1/records"
        
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Failed to get records: {response.status_code} - {response.text}"}
        
    except Exception as e:
        return {"success": False, "error": f"Connection error: {str(e)}"}

def get_user_by_id(token, user_id):
    """Get user profile by ID"""
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