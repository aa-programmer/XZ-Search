from flask import Flask, jsonify, request
import flask_cors
import sqlite3
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

flask_cors.CORS(app)  # Enable CORS for all routes

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

# Route to search for query and return results as JSON
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Get the query from URL parameters
    if not query:
        return jsonify({"error": "Query is required!"}), 400

    # Connect to the database
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    # Search for the query in the database
    cursor.execute("SELECT url FROM urls WHERE url LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    # Prepare a list of results with title and description
    search_results = []
    for idx, (url,) in enumerate(results[:5], 1):  # Show top 5 results
        title, description = get_title_and_description(url)
        search_results.append({
            "title": title,
            "description": description,
            "url": url
        })

    conn.close()

    # Return the results as JSON
    return jsonify({"results": search_results})

if __name__ == '__main__':
    app.run(debug=True)
