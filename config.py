# Configuration settings
API_BASE_URL = "https://api.corpus.swecha.org"
APP_NAME = "Swecha-Kosam"
APP_ICON = "🎙️"

# Session state defaults
SESSION_DEFAULTS = {
    'authenticated': False,
    'username': None,
    'user_token': None,
    'phone': None,
    'user_id': None,
    'otp_sent': False,
    'login_method': None,
    'user_profile': {},
    'user_records': [],
    'categories': [],
    'records_page': 1,
    'records_per_page': 5,
    'contributions': 0,
    'captured_image': None,
    'audio_recorded': None,
    'email': None,
    'name': None,
    'gender': None,
    'date_of_birth': None,
    'place': None
}