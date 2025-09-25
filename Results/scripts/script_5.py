# Now let's create the main analysis pipeline that processes all URLs

def analyze_single_article(url_id, url, positive_words, negative_words, stopwords):
    """
    Analyze a single article and return all metrics
    """
    print(f"Processing {url_id}: {url}")
    
    # Extract article text
    title, content = extract_article_text(url)
    
    # Save extracted text to file
    if content:
        with open(f"{url_id}.txt", 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n\nContent:\n{content}")
        print(f"  Saved to {url_id}.txt")
    else:
        print(f"  Failed to extract content")
        content = ""
    
    # Calculate all metrics
    if content:
        # Sentiment analysis
        pos_score, neg_score, pol_score, subj_score = calculate_sentiment_scores(
            content, positive_words, negative_words, stopwords
        )
        
        # Readability metrics
        readability = calculate_readability_metrics(content)
        
        # Personal pronouns
        pronouns = count_personal_pronouns(content)
        
        results = {
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': pos_score,
            'NEGATIVE SCORE': neg_score,
            'POLARITY SCORE': pol_score,
            'SUBJECTIVITY SCORE': subj_score,
            'AVG SENTENCE LENGTH': readability['avg_sentence_length'],
            'PERCENTAGE OF COMPLEX WORDS': readability['percentage_complex_words'],
            'FOG INDEX': readability['fog_index'],
            'AVG NUMBER OF WORDS PER SENTENCE': readability['avg_words_per_sentence'],
            'COMPLEX WORD COUNT': readability['complex_word_count'],
            'WORD COUNT': readability['word_count'],
            'SYLLABLE PER WORD': readability['syllables_per_word'],
            'PERSONAL PRONOUNS': pronouns,
            'AVG WORD LENGTH': readability['avg_word_length']
        }
        
    else:
        # If no content extracted, fill with zeros
        results = {
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': 0,
            'NEGATIVE SCORE': 0,
            'POLARITY SCORE': 0,
            'SUBJECTIVITY SCORE': 0,
            'AVG SENTENCE LENGTH': 0,
            'PERCENTAGE OF COMPLEX WORDS': 0,
            'FOG INDEX': 0,
            'AVG NUMBER OF WORDS PER SENTENCE': 0,
            'COMPLEX WORD COUNT': 0,
            'WORD COUNT': 0,
            'SYLLABLE PER WORD': 0,
            'PERSONAL PRONOUNS': 0,
            'AVG WORD LENGTH': 0
        }
    
    return results

# Process first 5 URLs as a test
print("Processing first 5 URLs as test...")
test_results = []

for i in range(min(5, len(input_df))):
    url_id = input_df.iloc[i]['URL_ID']
    url = input_df.iloc[i]['URL']
    
    try:
        result = analyze_single_article(url_id, url, positive_words, negative_words, stopwords)
        test_results.append(result)
        
        # Small delay to be respectful to the server
        time.sleep(1)
        
    except Exception as e:
        print(f"Error processing {url_id}: {str(e)}")
        # Add empty result
        test_results.append({
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': 0,
            'NEGATIVE SCORE': 0,
            'POLARITY SCORE': 0,
            'SUBJECTIVITY SCORE': 0,
            'AVG SENTENCE LENGTH': 0,
            'PERCENTAGE OF COMPLEX WORDS': 0,
            'FOG INDEX': 0,
            'AVG NUMBER OF WORDS PER SENTENCE': 0,
            'COMPLEX WORD COUNT': 0,
            'WORD COUNT': 0,
            'SYLLABLE PER WORD': 0,
            'PERSONAL PRONOUNS': 0,
            'AVG WORD LENGTH': 0
        })

# Create DataFrame with results
results_df = pd.DataFrame(test_results)
print(f"\nProcessed {len(results_df)} articles")
print("\nSample results:")
print(results_df.head())