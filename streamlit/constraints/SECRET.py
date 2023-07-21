from attribute import get_textunes_secret
secrets = get_textunes_secret()

OPENAI_API = secrets['openai_api_key']
MUSICGEN_CATEGORY_URL = secrets['musicgen_category_url']
MUSICGEN_ANALYSIS_URL = secrets['musicgen_analysis_url']
TEXT_ANALYSIS_URL = secrets['text_analysis_url']
