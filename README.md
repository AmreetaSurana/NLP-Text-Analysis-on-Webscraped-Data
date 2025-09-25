# NLP Text Analysis Project

## Overview
This project performs comprehensive text analysis on web articles, extracting content and computing various linguistic and sentiment metrics.

## Features
- **Web Scraping**: Extracts article content from URLs using BeautifulSoup
- **Sentiment Analysis**: Calculates positive/negative scores, polarity, and subjectivity
- **Readability Metrics**: FOG Index, complex word percentage, average sentence length
- **Linguistic Features**: Syllable count, personal pronouns, word length analysis
- **Data Processing**: Handles stopwords filtering and text cleaning

## Files Structure
- `complete_nlp_analyzer.py`: Main analysis system
- `Input.xlsx`: URLs to analyze
- `Output-Data-Structure.xlsx`: Expected output format
- `positive-words.txt`: Positive sentiment words
- `paste*.txt`: Negative sentiment words
- `StopWords_*.txt`: Various stopword lists
- `Text-Analysis.docx`: Methodology documentation

## Usage
```python
from complete_nlp_analyzer import ComprehensiveNLPAnalyzer

analyzer = ComprehensiveNLPAnalyzer()
results = analyzer.process_all_articles()
```

## Output Metrics
1. POSITIVE SCORE - Count of positive words
2. NEGATIVE SCORE - Count of negative words  
3. POLARITY SCORE - (Positive - Negative) / (Positive + Negative + 0.000001)
4. SUBJECTIVITY SCORE - (Positive + Negative) / Total Words
5. AVG SENTENCE LENGTH - Average words per sentence
6. PERCENTAGE OF COMPLEX WORDS - % of words with >2 syllables
7. FOG INDEX - Readability measure
8. COMPLEX WORD COUNT - Count of complex words
9. WORD COUNT - Total words in text
10. SYLLABLE PER WORD - Average syllables per word
11. PERSONAL PRONOUNS - Count of personal pronouns
12. AVG WORD LENGTH - Average character length per word

## Requirements
- pandas
- numpy
- requests
- beautifulsoup4
- openpyxl (for Excel file handling)

## Installation
```bash
pip install pandas numpy requests beautifulsoup4 openpyxl
```

## Project Status
✅ Web scraping implementation
✅ Sentiment analysis
✅ Readability calculations  
✅ Text preprocessing
✅ Excel output formatting
✅ Error handling
✅ Batch processing support
