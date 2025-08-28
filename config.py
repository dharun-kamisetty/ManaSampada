# Configuration settings
API_BASE_URL = "https://api.corpus.swecha.org"
APP_NAME = "Mana-Sampada"
APP_ICON = "📸"

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
    'text_content': None,
    'email': None,
    'name': None,
    'gender': None,
    'date_of_birth': None,
    'place': None
}

# Content types
CONTENT_TYPES = [
    "temple", "mosque", "church", "synagogue", "gurudwara",
    "monument", "historical_building", "artifact", "cultural_item",
    "traditional_art", "folk_music", "dance_form", "craft",
    "culinary_heritage", "literary_work", "ritual", "festival",
    "natural_heritage", "archaeological_site", "other"
]

# Languages
LANGUAGES = [
    "assamese", "bengali", "bodo", "dogri", "gujarati", "hindi", "kannada", 
    "kashmiri", "konkani", "maithili", "malayalam", "marathi", "meitei", 
    "nepali", "odia", "punjabi", "sanskrit", "santali", "sindhi", "tamil", 
    "telugu", "urdu"
]

RELEASE_RIGHTS = ["creator", "family_or_friend", "downloaded", "NA"]

MEDIA_TYPES = ["text", "audio", "video", "image"]
