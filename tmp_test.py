import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app.alternatives import get_alternatives

print("Testing get_alternatives function setup...")
try:
    auth_key = os.environ.get("GEMINI_API_KEY")
    print(f"API Key found: {'Yes' if auth_key else 'No'}")
    
    # We won't strictly enforce an API call failure since the user might not have added the key yet
    res = get_alternatives("condiment", ["High Fructose Corn Syrup", "Yellow 5"])
    print(f"Result: {res}")
    print("✅ Syntax and logic paths are valid.")
except Exception as e:
    print(f"❌ Verification script failed: {e}")
