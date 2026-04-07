import pickle
import re

class IngredientClassifier:
    def __init__(self, model_path="ml/model.pkl"):
        # Try to load model
        try:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            self.has_model = True
            print("✅ ML model loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            self.model = None
            self.has_model = False
        
        # LABELS mapping
        self.LABELS = {
            0: ("Controversial", "⚠️ Mixed safety reviews - consume with caution"),
            1: ("Harmful", "🚫 Potential health risks - avoid or limit"),
            2: ("Not Harmful", "✅ Generally safe for consumption")
        }
        
        # EXTENSIVE SAFE OVERRIDES
        self.SAFE_OVERRIDES = {
            # === GRAINS & FLOURS ===
            'flour': (2, "✅ Basic cooking ingredient"),
            'wheat flour': (2, "✅ Basic baking ingredient"),
            'enriched wheat flour': (2, "✅ Fortified baking flour"),
            'cornflour': (2, "✅ Common thickening agent"),
            'corn flour': (2, "✅ Common thickening agent"),
            'cornstarch': (2, "✅ Common thickening agent"),
            'corn starch': (2, "✅ Common thickening agent"),
            'rice flour': (2, "✅ Gluten-free flour"),
            
            # === SWEETENERS ===
            'sugar': (2, "✅ Sweetener - safe in moderation"),
            'glucose': (2, "✅ Simple sugar, energy source"),
            'fructose': (2, "✅ Fruit sugar, natural sweetener"),
            'sugar/glucose-fructose': (2, "✅ Sweetener blend"),
            
            # === OILS & FATS ===
            'oil': (2, "✅ Cooking fat, essential in moderation"),
            'palm oil': (0, "⚠️ Environmental concerns but generally safe"),
            'palm kernel oil': (0, "⚠️ From palm kernels, similar to palm oil"),
            'canola oil': (2, "✅ Common cooking oil"),
            'soy oil': (2, "✅ Cooking oil from soybeans"),
            'canola and/or soy oil': (2, "✅ Blend of cooking oils"),
            
            # === ACIDS & PRESERVATIVES ===
            'citric acid': (2, "✅ Natural acid from citrus fruits"),
            'sodium citrate': (2, "✅ Salt of citric acid, preservative"),
            
            # === STARCHES & THICKENERS ===
            'tapioca dextrin': (2, "✅ Processed tapioca starch"),
            'modified corn starch': (0, "⚠️ Processed starch, generally safe"),
            'dextrin': (2, "✅ Soluble fiber from starch"),
            
            # === FLAVORS ===
            'natural flavors': (0, "⚠️ Source varies - generally safe"),
            'artificial flavors': (0, "⚠️ Synthetic - some concerns"),
            'natural and artificial flavors': (0, "⚠️ Blend of natural and synthetic flavors"),
            
            # === LEAVENING AGENTS ===
            'sodium bicarbonate': (2, "✅ Baking soda, common leavening agent"),
            'baking powder': (2, "✅ Common leavening agent"),
            'baking soda': (2, "✅ Common leavening agent"),
            
            # === BASIC INGREDIENTS ===
            'salt': (2, "✅ Essential mineral in moderation"),
            'water': (2, "✅ Essential for life"),
            'eggs': (2, "✅ Protein source, nutritious"),
            'whole eggs': (2, "✅ Complete protein source"),
            'milk': (2, "✅ Dairy product, calcium source"),
            'butter': (2, "✅ Dairy fat, natural"),
            'cheese': (2, "✅ Dairy product"),
            
            # === VEGETABLES & FRUITS ===
            'onion': (2, "✅ Common vegetable, nutritious"),
            'garlic': (2, "✅ Seasoning, has health benefits"),
            'tomato': (2, "✅ Vegetable/fruit, nutritious"),
            'lemon': (2, "✅ Citrus fruit, vitamin C source"),
            'apple': (2, "✅ Common fruit, nutritious"),
            'banana': (2, "✅ Fruit, potassium source"),
            
            # === PROTEINS ===
            'chicken': (2, "✅ Lean protein source"),
            'beef': (2, "✅ Protein and iron source"),
            'fish': (2, "✅ Lean protein, omega-3 source"),
            
            # === GRAINS ===
            'rice': (2, "✅ Staple grain"),
            'bread': (2, "✅ Baked food"),
            'pasta': (2, "✅ Wheat product"),
        }
        
        # HARMFUL OVERRIDES
        self.HARMFUL_OVERRIDES = {
            'hydrogenated': (1, "🚫 Contains trans fats, increases heart disease risk"),
            'hydrogenated palm kernel oil': (1, "🚫 Contains trans fats, unhealthy"),
            'trans fat': (1, "🚫 Increases heart disease risk"),
            'partially hydrogenated': (1, "🚫 Source of trans fats"),
            'aspartame': (1, "🚫 Artificial sweetener with health concerns"),
            'saccharin': (1, "🚫 Artificial sweetener, potential carcinogen"),
            'sodium benzoate': (1, "🚫 Preservative linked to hyperactivity"),
            'bha': (1, "🚫 Preservative, potential carcinogen"),
            'bht': (1, "🚫 Preservative, potential carcinogen"),
            'potassium bromate': (1, "🚫 Flour additive, banned in many countries"),
            'azodicarbonamide': (1, "🚫 Flour bleaching agent, industrial chemical"),
            'yellow 5': (1, "🚫 Artificial color, potential allergen"),
            'yellow 6': (1, "🚫 Artificial color, potential health risks"),
            'red 40': (1, "🚫 Artificial color, potential hyperactivity trigger"),
            'blue 1': (1, "🚫 Artificial color, potential health risks"),
            'blue 2': (1, "🚫 Artificial color, potential health risks"),
        }
        
        # CONTROVERSIAL OVERRIDES
        self.CONTROVERSIAL_OVERRIDES = {
            'high fructose corn syrup': (0, "⚠️ Linked to obesity and diabetes"),
            'corn syrup': (0, "⚠️ Sweetener with high fructose content"),
            'msg': (0, "⚠️ Monosodium glutamate - controversial"),
            'monosodium glutamate': (0, "⚠️ Flavor enhancer, controversial"),
            'artificial color': (0, "⚠️ Synthetic coloring, some concerns"),
            'artificial colors': (0, "⚠️ Synthetic colorings, some concerns"),
            'carrageenan': (0, "⚠️ Thickener with safety debates"),
            'xanthan gum': (0, "⚠️ Thickener, can cause digestive issues"),
            'soy lecithin': (0, "⚠️ Emulsifier, soy allergies common"),
        }
    
    def predict_ingredient(self, ingredient):
        """Predict safety of an ingredient"""
        ingredient_lower = ingredient.lower().strip()
        
        # 1. Check exact matches in overrides
        if ingredient_lower in self.SAFE_OVERRIDES:
            pred, explanation = self.SAFE_OVERRIDES[ingredient_lower]
            label, _ = self.LABELS[pred]
            return label, explanation
        
        if ingredient_lower in self.HARMFUL_OVERRIDES:
            pred, explanation = self.HARMFUL_OVERRIDES[ingredient_lower]
            label, _ = self.LABELS[pred]
            return label, explanation
        
        if ingredient_lower in self.CONTROVERSIAL_OVERRIDES:
            pred, explanation = self.CONTROVERSIAL_OVERRIDES[ingredient_lower]
            label, _ = self.LABELS[pred]
            return label, explanation
        
        # 2. Check for harmful keywords
        harmful_keywords = ['hydrogenated', 'aspartame', 'saccharin', 'bha', 'bht', 
                          'yellow 5', 'yellow 6', 'red 40', 'blue 1', 'blue 2',
                          'artificial color', 'artificial colours']
        
        for keyword in harmful_keywords:
            if keyword in ingredient_lower:
                return "Harmful", f"🚫 Contains {keyword} - potential health risk"
        
        # 3. Check for controversial keywords
        controversial_keywords = ['corn syrup', 'msg', 'monosodium glutamate', 
                                'artificial flavor', 'high fructose']
        
        for keyword in controversial_keywords:
            if keyword in ingredient_lower:
                return "Controversial", f"⚠️ Contains {keyword} - mixed safety reviews"
        
        # 4. Try ML model first to get an authoritative prediction
        ml_pred = None
        ml_confidence = 0
        if self.has_model:
            try:
                proba = self.model.predict_proba([ingredient])[0]
                ml_pred = int(self.model.predict([ingredient])[0])
                ml_confidence = proba[ml_pred]
            except:
                pass
                
        # If the ML model CONFIDENTLY thinks this is Harmful or Controversial, trust it!
        # Do not let generic substrings (like 'oil' in 'brominated vegetable oil') override a known hazard.
        is_confidently_harmful = ml_pred == 1 and ml_confidence >= 0.58
        is_confidently_controversial = ml_pred == 0 and ml_confidence >= 0.52
        
        if is_confidently_harmful or is_confidently_controversial:
            label, explanation = self.LABELS[ml_pred]
            return label, explanation
            
        # 5. Check for safe patterns to provide good explanations for safe/unknown ingredients
        safe_patterns = [
            ('flour', "✅ Common food ingredient"),
            ('salt', "✅ Essential mineral"),
            ('sugar', "✅ Sweetener in moderation"),
            ('oil', "✅ Cooking fat"),
            ('water', "✅ Essential for life"),
            ('milk', "✅ Dairy product"),
            ('egg', "✅ Protein source"),
            ('rice', "✅ Staple grain"),
            ('bread', "✅ Baked food"),
            ('cheese', "✅ Dairy product"),
            ('acid', "✅ Common food acid"),
            ('starch', "✅ Thickening agent"),
            ('dextrin', "✅ Soluble fiber"),
            ('citrate', "✅ Preservative"),
            ('potato', "✅ Common vegetable"),
            ('tomato', "✅ Common vegetable"),
            ('onion', "✅ Common vegetable"),
            ('garlic', "✅ Seasoning"),
            ('spice', "✅ Common seasoning"),
            ('paprika', "✅ Common seasoning"),
            ('molasses', "✅ Sweetener in moderation"),
            ('corn', "✅ Common grain/vegetable"),
            ('cocoa', "✅ Chocolate ingredient"),
            ('yeast', "✅ Common ingredient")
        ]
        
        for pattern, explanation in safe_patterns:
            if pattern in ingredient_lower:
                return "Not Harmful", explanation
                
        # If no safe pattern matches, fallback to the ML model's rating
        if ml_pred is not None:
             # If the model thought it was harmful but with low confidence, override it to safe
             if (ml_pred == 1 and ml_confidence < 0.58) or (ml_pred == 0 and ml_confidence < 0.52):
                 return "Not Harmful", "✅ Assumed safe (ML model had low confidence for danger)"
             else:
                 label, explanation = self.LABELS[ml_pred]
                 return label, explanation
        
        # 6. Default: safe
        return "Not Harmful", "✅ Assuming safe unless known to be harmful"
    
    def predict_multiple(self, ingredients):
        """Predict safety for multiple ingredients"""
        results = []
        for ing in ingredients:
            if ing and ing.strip():
                label, explanation = self.predict_ingredient(ing.strip())
                results.append({
                    'ingredient': ing.strip(),
                    'label': label,
                    'explanation': explanation
                })
        return results

# Create a global instance
classifier = IngredientClassifier()

# Quick test
if __name__ == "__main__":
    print("Testing classifier...")
    test_ingredients = [
        'enriched wheat flour',
        'sugar/glucose-fructose',
        'hydrogenated palm kernel oil',
        'citric acid',
        'modified corn starch',
        'natural and artificial flavors',
        'sodium citrate',
        'yellow 5 lake',
        'salt',
        'baking powder'
    ]
    
    for ing in test_ingredients:
        label, explanation = classifier.predict_ingredient(ing)
        print(f"{ing:35} -> {label:15} ({explanation[:40]}...)")