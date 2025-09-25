
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import os
import time
from urllib.parse import urljoin

class ComprehensiveNLPAnalyzer:
    """
    Complete NLP Text Analysis System for Web Articles

    This system:
    1. Extracts article content from URLs
    2. Performs sentiment analysis using positive/negative word dictionaries
    3. Calculates readability metrics (FOG Index, complexity, etc.)
    4. Counts linguistic features (syllables, pronouns, etc.)
    5. Outputs results in specified Excel format
    """

    def __init__(self):
        self.positive_words = set()
        self.negative_words = set()
        self.stopwords = set()

    def load_word_lists(self):
        """Load all word lists and stopwords from files"""

        # Load positive words
        try:
            with open("C:/Users/HP/Downloads/NLP Project/MasterDictionary/positive-words.txt", 'r', encoding='utf-8') as f:
                self.positive_words = set(word.strip().lower() for word in f.readlines() if word.strip())
            print(f"Loaded {len(self.positive_words)} positive words")
        except Exception as e:
            print(f"Error loading positive words: {e}")

        # Load negative words
        paste_files = ["C:/Users/HP/Downloads/NLP Project/MasterDictionary/negative-words.txt"]
        for paste_file in paste_files:
            try:
                with open(paste_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = re.findall(r'\b\w+\b', content.lower())
                    self.negative_words.update(words)
                print(f"Loaded negative words from {paste_file}")
                break
            except Exception:
                continue

        print(f"Loaded {len(self.negative_words)} negative words")

        # Load stopwords
        stopword_files = [
            "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_Auditor.txt", "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_DatesandNumbers.txt",
            "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_Generic.txt", "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_GenericLong.txt",
            "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_Geographic.txt", "C:/Users/HP/Downloads/NLP Project/StopWords/StopWords_Names.txt"
        ]

        for stop_file in stopword_files:
            try:
                with open(stop_file, 'r', encoding='utf-8') as f:
                    words = f.read().split()
                    self.stopwords.update(word.lower() for word in words)
            except Exception as e:
                print(f"Error loading {stop_file}: {e}")

        # Add currency stopwords
        currency_stopwords = [
            'AFGHANI', 'ARIARY', 'BAHT', 'BALBOA', 'BIRR', 'BOLIVAR', 'BOLIVIANO', 
            'CEDI', 'COLON', 'CÓRDOBA', 'DALASI', 'DENAR', 'DINAR', 'DIRHAM', 
            'DOBRA', 'DONG', 'DRAM', 'ESCUDO', 'EURO', 'FLORIN', 'FORINT', 
            'GOURDE', 'GUARANI', 'GULDEN', 'HRYVNIA', 'KINA', 'KIP', 'KORUNA',
            'KRONA', 'KRONE', 'KROON', 'KUNA', 'KWACHA', 'KWANZA', 'KYAT',
            'LARI', 'LATS', 'LEK', 'LEMPIRA', 'LEONE', 'LEU', 'LEV', 'LILANGENI',
            'LIRA', 'LITAS', 'LOTI', 'MANAT', 'METICAL', 'NAIRA', 'NAKFA',
            'SHEQEL', 'NGULTRUM', 'NUEVO', 'SOL', 'OUGUIYA', 'PATACA', 'PESO',
            'POUND', 'PULA', 'QUETZAL', 'RAND', 'REAL', 'RENMINBI', 'RIAL',
            'RIEL', 'RINGGIT', 'RIYAL', 'RUBLE', 'RUFIYAA', 'RUPEE', 'RUPIAH',
            'SHILLING', 'SOM', 'SOMONI', 'TAKA', 'TALA', 'TENGE', 'TUGRIK',
            'VATU', 'WON', 'YEN', 'ZLOTY'
        ]

        self.stopwords.update(word.lower() for word in currency_stopwords)
        print(f"Total stopwords loaded: {len(self.stopwords)}")

    def extract_article_text(self, url):
        """Extract article text from URL using BeautifulSoup"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract title
            title = ""
            for tag in ['h1', 'title', '.entry-title', '.post-title']:
                if tag.startswith('.'):
                    element = soup.find(class_=tag[1:])
                else:
                    element = soup.find(tag)
                if element:
                    title = element.get_text().strip()
                    break

            # Extract article content
            article_text = ""
            content_selectors = [
                'article', '.post-content', '.entry-content', 
                '.article-content', '.content', 'main'
            ]

            for selector in content_selectors:
                if selector.startswith('.'):
                    elements = soup.find_all(class_=selector[1:])
                else:
                    elements = soup.find_all(selector)

                if elements:
                    article_text = ' '.join([elem.get_text() for elem in elements])
                    break

            if not article_text:
                paragraphs = soup.find_all('p')
                article_text = ' '.join([p.get_text() for p in paragraphs])

            # Clean text
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            title = re.sub(r'\s+', ' ', title).strip()

            return title, article_text

        except Exception as e:
            print(f"Error extracting from {url}: {str(e)}")
            return "", ""

    def count_syllables(self, word):
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

        if word.endswith('e'):
            syllable_count -= 1

        return max(1, syllable_count)

    def is_complex_word(self, word):
        """Check if word is complex (>2 syllables)"""
        return self.count_syllables(word) > 2

    def clean_text(self, text):
        """Clean text by removing stopwords"""
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in self.stopwords]

    def calculate_sentiment_scores(self, text):
        """Calculate sentiment analysis scores"""
        cleaned_words = self.clean_text(text)

        positive_score = sum(1 for word in cleaned_words if word in self.positive_words)
        negative_score = sum(1 for word in cleaned_words if word in self.negative_words)

        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(cleaned_words) + 0.000001)

        return positive_score, negative_score, polarity_score, subjectivity_score

    def calculate_readability_metrics(self, text):
        """Calculate readability and linguistic metrics"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = re.findall(r'\b\w+\b', text)

        if not sentences or not words:
            return {
                'avg_sentence_length': 0, 'percentage_complex_words': 0,
                'fog_index': 0, 'avg_words_per_sentence': 0,
                'complex_word_count': 0, 'word_count': 0,
                'syllables_per_word': 0, 'avg_word_length': 0
            }

        complex_words = [word for word in words if self.is_complex_word(word)]
        complex_word_count = len(complex_words)
        word_count = len(words)

        avg_sentence_length = len(words) / len(sentences)
        percentage_complex_words = (complex_word_count / word_count) * 100
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

        total_syllables = sum(self.count_syllables(word) for word in words)
        syllables_per_word = total_syllables / word_count
        avg_word_length = sum(len(word) for word in words) / word_count

        return {
            'avg_sentence_length': avg_sentence_length,
            'percentage_complex_words': percentage_complex_words,
            'fog_index': fog_index,
            'avg_words_per_sentence': avg_sentence_length,
            'complex_word_count': complex_word_count,
            'word_count': word_count,
            'syllables_per_word': syllables_per_word,
            'avg_word_length': avg_word_length
        }

    def count_personal_pronouns(self, text):
        """Count personal pronouns"""
        personal_pronouns = ['i', 'we', 'my', 'ours', 'us']
        words = re.findall(r'\b\w+\b', text.lower())
        return sum(1 for word in words if word in personal_pronouns)

    def analyze_article(self, url_id, url):
        """Complete analysis of single article"""
        print(f"Analyzing {url_id}...")

        title, content = self.extract_article_text(url)

        # Save extracted text
        if content:
            os.makedirs('extracted_articles', exist_ok=True)
            with open(f'extracted_articles/{url_id}.txt', 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n\nContent:\n{content}")

        if content:
            pos_score, neg_score, pol_score, subj_score = self.calculate_sentiment_scores(content)
            readability = self.calculate_readability_metrics(content)
            pronouns = self.count_personal_pronouns(content)

            return {
                'URL_ID': url_id, 'URL': url,
                'POSITIVE SCORE': pos_score, 'NEGATIVE SCORE': neg_score,
                'POLARITY SCORE': pol_score, 'SUBJECTIVITY SCORE': subj_score,
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
            return {
                'URL_ID': url_id, 'URL': url,
                'POSITIVE SCORE': 0, 'NEGATIVE SCORE': 0, 'POLARITY SCORE': 0,
                'SUBJECTIVITY SCORE': 0, 'AVG SENTENCE LENGTH': 0,
                'PERCENTAGE OF COMPLEX WORDS': 0, 'FOG INDEX': 0,
                'AVG NUMBER OF WORDS PER SENTENCE': 0, 'COMPLEX WORD COUNT': 0,
                'WORD COUNT': 0, 'SYLLABLE PER WORD': 0, 'PERSONAL PRONOUNS': 0,
                'AVG WORD LENGTH': 0
            }

    def process_all_articles(self, input_file= r"C:/Users/HP/Downloads/NLP Project/Input.xlsx", output_file= "Output.xlsx"):
        """Process all articles and generate final results"""

        print("Loading input data...")
        input_df = pd.read_excel(input_file)

        print("Loading word lists...")
        self.load_word_lists()

        print(f"Processing {len(input_df)} articles...")
        all_results = []

        for i, row in input_df.iterrows():
            url_id = row['URL_ID']
            url = row['URL']

            try:
                result = self.analyze_article(url_id, url)
                all_results.append(result)
                time.sleep(0.5)  # Be respectful to servers

                if (i + 1) % 10 == 0:
                    print(f"Completed {i + 1}/{len(input_df)} articles")

            except Exception as e:
                print(f"Error processing {url_id}: {e}")
                all_results.append({
                    'URL_ID': url_id, 'URL': url,
                    'POSITIVE SCORE': 0, 'NEGATIVE SCORE': 0, 'POLARITY SCORE': 0,
                    'SUBJECTIVITY SCORE': 0, 'AVG SENTENCE LENGTH': 0,
                    'PERCENTAGE OF COMPLEX WORDS': 0, 'FOG INDEX': 0,
                    'AVG NUMBER OF WORDS PER SENTENCE': 0, 'COMPLEX WORD COUNT': 0,
                    'WORD COUNT': 0, 'SYLLABLE PER WORD': 0, 'PERSONAL PRONOUNS': 0,
                    'AVG WORD LENGTH': 0
                })

        # Save results
        import os
        my_directory = "C:/Users/HP/Downloads/NLP Project/Results"
        os.makedirs(my_directory, exist_ok=True)
        # just the file name
        

        results_df = pd.DataFrame(all_results)
        results_df.to_excel(f"{my_directory}/{output_file}", index=False)



        print(f"\n=== ANALYSIS COMPLETE ===")
        print(f"Results saved to:{output_file}")
        print(f"Articles processed: {len(results_df)}")
        print(f"Articles with content: {sum(1 for _, row in results_df.iterrows() if row['WORD COUNT'] > 0)}")

        return results_df

# Main execution
if __name__ == "__main__":
    analyzer = ComprehensiveNLPAnalyzer()
    results = analyzer.process_all_articles()

    # Display summary statistics
    print("\n=== SUMMARY STATISTICS ===")
    numeric_cols = [col for col in results.columns if col not in ['URL_ID', 'URL']]
    for col in numeric_cols:
        print(f"{col}: Mean={results[col].mean():.4f}, Range=({results[col].min():.4f}-{results[col].max():.4f})")
