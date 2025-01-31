import re

# Function to remove sentences containing any of the specified patterns
def remove_sentences(input_file, output_file, patterns):
    with open(input_file, 'r') as file:
        content = file.read()

    # Regular expression to match sentences, accounting for possible sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', content)  # Split by sentence-ending punctuation

    # Debugging: Print total number of sentences
    print(f"Total sentences found: {len(sentences)}")

    # Filter sentences that do not contain any of the specified patterns
    filtered_sentences = [
        sentence for sentence in sentences if not any(re.search(pattern, sentence) for pattern in patterns)
    ]
    
    # Debugging: Print filtered sentences count
    print(f"Sentences remaining after filtering: {len(filtered_sentences)}")

    # Join the sentences back together
    cleaned_content = ' '.join(filtered_sentences)

    # Debugging: Print first 500 characters of the cleaned content
    print(f"Cleaned content preview: {cleaned_content[:500]}")

    # Write the cleaned content to the output file
    with open(output_file, 'w') as file:
        file.write(cleaned_content)

# Example usage:
input_file = 'profile_links.txt'
output_file = 'cleaned_profile_links.txt'
patterns = [
    'https://read.cv/about/supporters', 'https://read.cv/explore', 'https://read.cv/explore/activity', 
    'https://read.cv/about', 'https://read.cv/sites/about', 'https://read.cv/a-new-chapter', 'https://read.cv/open-roles'
]

remove_sentences(input_file, output_file, patterns)