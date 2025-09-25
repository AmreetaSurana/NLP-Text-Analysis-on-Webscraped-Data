# Now let's load the stopwords and positive/negative word lists
def load_word_lists():
    """Load all the word lists and stopwords"""
    
    # Load positive words
    try:
        with open(r"C:\Users\HP\Downloads\20211030 Test Assignment\MasterDictionary\positive-words.txt", 'r', encoding='utf-8') as f:
            positive_words = set(word.strip().lower() for word in f.readlines() if word.strip())
        print(f"Loaded {len(positive_words)} positive words")
    except Exception as e:
        print(f"Error loading positive words: {e}")
        positive_words = set()
    
    # Load negative words (from paste files)
    negative_words = set()
    paste_files = [r"C:\Users\HP\Downloads\20211030 Test Assignment\MasterDictionary\negative-words.txt"]
    
    for paste_file in paste_files:
        try:
            with open(paste_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by spaces and newlines
                words = re.findall(r'\b\w+\b', content.lower())
                negative_words.update(words)
                print(f"Loaded words from {paste_file}")
                break  # Just need one file since they seem to be duplicates
        except Exception as e:
            continue
    
    print(f"Loaded {len(negative_words)} negative words")
    
    # Load all stopwords
    stopwords = set()
    stopword_files = [
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_Auditor.txt",
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_DatesandNumbers.txt",
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_Generic.txt",
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_GenericLong.txt",
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_Geographic.txt",
        r"C:\Users\HP\Downloads\20211030 Test Assignment\StopWords\StopWords_Names.txt"
    ]
    
    for stop_file in stopword_files:
        try:
            with open(stop_file, 'r', encoding='utf-8') as f:
                words = f.read().split()
                stopwords.update(word.lower() for word in words)
            print(f"Loaded stopwords from {stop_file}")
        except Exception as e:
            print(f"Error loading {stop_file}: {e}")
    
    # Add currency stopwords provided earlier
    currency_stopwords = [
        'AFGHANI', 'ARIARY', 'BAHT', 'BALBOA', 'BIRR', 'BOLIVAR', 'BOLIVIANO', 'CEDI', 'COLON', 
        'CÓRDOBA', 'DALASI', 'DENAR', 'DINAR', 'DIRHAM', 'DOBRA', 'DONG', 'DRAM', 'ESCUDO', 
        'EURO', 'FLORIN', 'FORINT', 'GOURDE', 'GUARANI', 'GULDEN', 'HRYVNIA', 'KINA', 'KIP',
        'KONVERTIBILNA', 'MARKA', 'KORUNA', 'KRONA', 'KRONE', 'KROON', 'KUNA', 'KWACHA', 
        'KWANZA', 'KYAT', 'LARI', 'LATS', 'LEK', 'LEMPIRA', 'LEONE', 'LEU', 'LEV', 'LILANGENI',
        'LIRA', 'LITAS', 'LOTI', 'MANAT', 'METICAL', 'NAIRA', 'NAKFA', 'SHEQEL', 'NGULTRUM',
        'NUEVO', 'SOL', 'OUGUIYA', 'PATACA', 'PESO', 'POUND', 'PULA', 'QUETZAL', 'RAND',
        'REAL', 'RENMINBI', 'RIAL', 'RIEL', 'RINGGIT', 'RIYAL', 'RUBLE', 'RUFIYAA', 'RUPEE',
        'RUPIAH', 'SHILLING', 'SOM', 'SOMONI', 'SPECIAL', 'DRAWING', 'RIGHTS', 'TAKA', 'TALA',
        'TENGE', 'TUGRIK', 'VATU', 'WON', 'YEN', 'ZLOTY'
    ]
    
    stopwords.update(word.lower() for word in currency_stopwords)
    
    print(f"Total stopwords: {len(stopwords)}")
    
    return positive_words, negative_words, stopwords

# Load word lists
positive_words, negative_words, stopwords = load_word_lists()