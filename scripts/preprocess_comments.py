
import os
import json
import re

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove emojis and special chars (basic Amharic preservation)
    text = re.sub(r'[^\w\s።፣፤፥፦፧፨]', '', text)
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def preprocess_file(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as f:
        comments = json.load(f)
    
    cleaned_comments = []
    for comment in comments:
        text = comment.get('text', '')
        cleaned = clean_text(text)
        if len(cleaned) > 3:
            cleaned_comments.append({'text': cleaned, 'original': text})
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned_comments, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {input_filepath}: {len(comments)} -> {len(cleaned_comments)} cleaned")

def preprocess_all_comments(folder_path='comments_data'):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and not filename.endswith('_cleaned.json'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, filename.replace('.json', '_cleaned.json'))
            preprocess_file(input_path, output_path)

if __name__ == "__main__":
    preprocess_all_comments()
