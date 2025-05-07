import sqlite3
import requests
from bs4 import BeautifulSoup

# Function to get the title and description from a URL
def get_title_and_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the title of the page
        title = soup.title.string if soup.title else "No title found"

        # Get the description from meta tags
        description = ""
        meta_description = soup.find('meta', attrs={'name': 'description'}) or \
                            soup.find('meta', attrs={'property': 'og:description'})
        
        if meta_description:
            description = meta_description.get('content', 'No description available')
        else:
            # Use first 160 characters of page text as a fallback description
            description = ' '.join(soup.get_text().split()[:30]) + '...'

        return title, description
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return "Error", "Error"

# Function to search for a query and fetch titles and descriptions
def search(query, num):
    # Connect to the database
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    # Search for the query in the database
    cursor.execute("SELECT url FROM urls WHERE url LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    result_dict = {}

    for idx, (url,) in enumerate(results[:num], 1):
        title, description = get_title_and_description(url)
        result_dict[str(idx)] = {
            "url": url,
            "title": title,
            "description": description
        }
    
    conn.close()

    return result_dict