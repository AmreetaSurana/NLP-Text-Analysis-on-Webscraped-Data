# Now let's create the text analysis functions

def count_syllables(word):
    """Count syllables in a word"""
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    # Handle silent e
    if word.endswith('e'):
        syllable_count -= 1
    
    # Every word has at least 1 syllable
    return max(1, syllable_count)

def is_complex_word(word):
    """Check if a word is complex (more than 2 syllables)"""
    return count_syllables(word) > 2

def clean_text(text, stopwords):
    """Clean text by removing stopwords and punctuation"""
    # Convert to lowercase and extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove stopwords
    cleaned_words = [word for word in words if word not in stopwords]
    
    return cleaned_words

def calculate_sentiment_scores(text, positive_words, negative_words, stopwords):
    """Calculate positive, negative, polarity and subjectivity scores"""
    
    # Clean the text
    cleaned_words = clean_text(text, stopwords)
    
    # Count positive and negative words
    positive_score = sum(1 for word in cleaned_words if word in positive_words)
    negative_score = sum(1 for word in cleaned_words if word in negative_words)
    
    # Calculate polarity score
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    
    # Calculate subjectivity score
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def calculate_readability_metrics(text):
    """Calculate various readability metrics"""
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Extract all words
    words = re.findall(r'\b\w+\b', text)
    
    if not sentences or not words:
        return {
            'avg_sentence_length': 0,
            'percentage_complex_words': 0,
            'fog_index': 0,
            'avg_words_per_sentence': 0,
            'complex_word_count': 0,
            'word_count': 0,
            'syllables_per_word': 0,
            'avg_word_length': 0
        }
    
    # Count complex words
    complex_words = [word for word in words if is_complex_word(word)]
    complex_word_count = len(complex_words)
    
    # Calculate metrics
    word_count = len(words)
    avg_sentence_length = len(words) / len(sentences)
    percentage_complex_words = (complex_word_count / word_count) * 100
    
    # Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    
    # Syllables per word
    total_syllables = sum(count_syllables(word) for word in words)
    syllables_per_word = total_syllables / word_count
    
    # Average word length
    avg_word_length = sum(len(word) for word in words) / word_count
    
    return {
        'avg_sentence_length': avg_sentence_length,
        'percentage_complex_words': percentage_complex_words,
        'fog_index': fog_index,
        'avg_words_per_sentence': avg_sentence_length,  # Same as avg_sentence_length
        'complex_word_count': complex_word_count,
        'word_count': word_count,
        'syllables_per_word': syllables_per_word,
        'avg_word_length': avg_word_length
    }

def count_personal_pronouns(text):
    """Count personal pronouns in text"""
    personal_pronouns = ['i', 'we', 'my', 'ours', 'us']
    words = re.findall(r'\b\w+\b', text.lower())
    
    pronoun_count = sum(1 for word in words if word in personal_pronouns)
    return pronoun_count

# Test the analysis functions on our sample text
print("Testing analysis functions...")

# Read the saved test file
with open('Netclan20241017.txt', 'r', encoding='utf-8') as f:
    sample_text = f.read()

# Extract just the content part (after "Content:")
content_start = sample_text.find("Content:\n")
if content_start != -1:
    sample_content = sample_text[content_start + 9:]  # Skip "Content:\n"
else:
    sample_content = sample_text

print(f"Analyzing text with {len(sample_content)} characters...")

# Calculate sentiment scores
pos_score, neg_score, pol_score, subj_score = calculate_sentiment_scores(
    sample_content, positive_words, negative_words, stopwords
)

print(f"Sentiment Analysis:")
print(f"  Positive Score: {pos_score}")
print(f"  Negative Score: {neg_score}")
print(f"  Polarity Score: {pol_score:.4f}")
print(f"  Subjectivity Score: {subj_score:.4f}")

# Calculate readability metrics
readability = calculate_readability_metrics(sample_content)
print(f"\nReadability Metrics:")
for key, value in readability.items():
    print(f"  {key}: {value:.4f}")

# Count personal pronouns
pronouns = count_personal_pronouns(sample_content)
print(f"  Personal Pronouns: {pronouns}")