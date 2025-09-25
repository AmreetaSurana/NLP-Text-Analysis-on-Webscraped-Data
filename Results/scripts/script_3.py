# Create web scraper to extract article content
def extract_article_text(url):
    """
    Extract article text from URL using BeautifulSoup
    Returns title and article text as tuple
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find article title
        title = ""
        title_tags = ['h1', 'title', '.entry-title', '.post-title', '.article-title']
        
        for tag in title_tags:
            if tag.startswith('.'):
                element = soup.find(class_=tag[1:])
            else:
                element = soup.find(tag)
            
            if element:
                title = element.get_text().strip()
                break
        
        # Try to find main article content
        article_text = ""
        
        # Common article content selectors
        content_selectors = [
            'article', '.post-content', '.entry-content', '.article-content',
            '.content', 'main', '.main-content', '[role="main"]'
        ]
        
        for selector in content_selectors:
            if selector.startswith('.'):
                elements = soup.find_all(class_=selector[1:])
            elif selector.startswith('['):
                elements = soup.find_all(attrs={'role': 'main'})
            else:
                elements = soup.find_all(selector)
            
            if elements:
                article_text = ' '.join([elem.get_text() for elem in elements])
                break
        
        # If no specific article content found, get all paragraph text
        if not article_text:
            paragraphs = soup.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
        
        # Clean the text
        article_text = re.sub(r'\s+', ' ', article_text).strip()
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title, article_text
        
    except Exception as e:
        print(f"Error extracting from {url}: {str(e)}")
        return "", ""

# Test the scraper with the first URL
test_url = input_df.iloc[0]['URL']
test_url_id = input_df.iloc[0]['URL_ID']

print(f"Testing scraper with URL: {test_url}")
title, content = extract_article_text(test_url)

print(f"\nExtracted title: {title[:100]}...")
print(f"Content length: {len(content)} characters")
print(f"Content preview: {content[:200]}...")

# Save extracted content to file
if content:
    with open(f"{test_url_id}.txt", 'w', encoding='utf-8') as f:
        f.write(f"Title: {title}\n\nContent:\n{content}")
    print(f"Saved content to {test_url_id}.txt")