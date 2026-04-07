import os
import re

with open('ml/predict.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. LABELS Block
old_labels = """        self.LABELS = {
            0: ("Not Harmful", "✅ Generally safe for consumption"),
            1: ("Controversial", "⚠️ Mixed safety reviews - consume with caution"),
            2: ("Harmful", "🚫 Potential health risks - avoid or limit")
        }"""
new_labels = """        self.LABELS = {
            0: ("Controversial", "⚠️ Mixed safety reviews - consume with caution"),
            1: ("Harmful", "🚫 Potential health risks - avoid or limit"),
            2: ("Not Harmful", "✅ Generally safe for consumption")
        }"""
code = code.replace(old_labels, new_labels)

# 2. Block Replacements
start_s = code.find('self.SAFE_OVERRIDES = {')
end_s = code.find('self.HARMFUL_OVERRIDES = {')
if start_s != -1 and end_s != -1:
    safe_b = code[start_s:end_s].replace('(0,', '(2,').replace('(1,', '(0,')
    code = code[:start_s] + safe_b + code[end_s:]

start_h = code.find('self.HARMFUL_OVERRIDES = {')
end_h = code.find('self.CONTROVERSIAL_OVERRIDES = {')
if start_h != -1 and end_h != -1:
    harm_b = code[start_h:end_h].replace('(2,', '(1,')
    code = code[:start_h] + harm_b + code[end_h:]

start_c = code.find('self.CONTROVERSIAL_OVERRIDES = {')
end_c = code.find('def predict_ingredient')
if start_c != -1 and end_c != -1:
    cont_b = code[start_c:end_c].replace('(1,', '(0,')
    code = code[:start_c] + cont_b + code[end_c:]

# 3. Model checks
code = code.replace('is_confidently_harmful = ml_pred == 2', 'is_confidently_harmful = ml_pred == 1')
code = code.replace('is_confidently_controversial = ml_pred == 1', 'is_confidently_controversial = ml_pred == 0')
code = code.replace('if ml_pred == 2 or ml_pred == 1:', 'if ml_pred == 1 or ml_pred == 0:')

with open('ml/predict.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("predict.py migrated successfully!")
