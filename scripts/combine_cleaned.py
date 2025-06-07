import os
import json
import re

def contains_amharic(text):
    # Checks if text contains any Amharic Unicode range
    return bool(re.search(r'[\u1200-\u137F]', text))

def contains_latin_words(text):
    # Returns True if text contains Latin letters (English alphabet)
    return bool(re.search(r'[a-zA-Z]', text))

def combine_cleaned_comments(folder_path='comments_data', output_file='comments_data/combined_cleaned.json'):
    all_comments = []

    # Load and filter all cleaned comment files
    for filename in os.listdir(folder_path):
        if filename.endswith('_cleaned.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                comments = json.load(f)

                # Filter comments: keep only if Amharic and no Latin letters
                filtered = [c for c in comments if contains_amharic(c.get('text', '')) and not contains_latin_words(c.get('text', ''))]

                all_comments.extend(filtered)
            print(f"Loaded {filename}: kept {len(filtered)} comments after filtering")

    # Remove duplicates based on 'text'
    seen_texts = set()
    unique_comments = []
    for comment in all_comments:
        text = comment.get('text', '').strip()
        if text not in seen_texts:
            seen_texts.add(text)
            unique_comments.append(comment)

    # Save combined unique comments
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(unique_comments, out_f, ensure_ascii=False, indent=2)

    print(f"\n✅ Combined and deduplicated {len(unique_comments)} comments saved to {output_file}")

if __name__ == "__main__":
    combine_cleaned_comments()
