import os
import json
from groq import Groq

def get_alternatives(category, harmful_ingredients):
    if not category:
        return []

    # Fallback/Debug print
    print(f"DEBUG: Getting alternatives for {category} avoiding {harmful_ingredients}")
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("⚠️ GROQ_API_KEY not found in environment variables. Provide one in a .env file.")
        return []

    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
        The user is scanning a product vaguely in this category: '{category}'.
        We detected these controversial or harmful ingredients in it: {', '.join(harmful_ingredients)}.
        
        Please return EXACTLY 3 healthy, highly-rated brand alternatives for this category that DO NOT contain those ingredients.
        Provide the response strictly as a valid JSON array of objects, with absolutely NO markdown formatting block ticks like ```json or extra conversational text. Just the array.
        Each object must have exactly these keys: 
        - "name" (product name)
        - "brand" (brand name)
        - "reason" (short 1-sentence reason highlighting why it's safer)
        """
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        
        text = completion.choices[0].message.content.strip()
        
        # Additional strip logic in case LLM ignores instructions
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        return data[:3]
    except Exception as e:
        print(f"⚠️ Error calling Groq API: {e}")
        return []
