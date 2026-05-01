from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_news():
    url = "https://www.thedailystar.net/todays-news"
    # Professional User-Agent to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_data = []
        
        # Selection logic for The Daily Star headlines
        for item in soup.select('h3 a, h4 a')[:15]:
            title = item.get_text().strip()
            link = item.get('href')
            
            # Ensure links are absolute
            if link and not link.startswith('http'):
                link = "https://www.thedailystar.net" + link
            
            # Filter to ensure we only get actual headlines (usually longer than 3 words)
            if len(title.split()) > 3:
                news_data.append({'title': title, 'link': link})
                
        return news_data
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# Modern UI Design
HTML_DESIGN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AXIO | Live News Feed</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #f8f9fa; color: #212529; }
        
        .navbar { 
            background: #001a33; 
            color: #ffffff; 
            padding: 20px; 
            text-align: center; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
            position: sticky; 
            top: 0; 
            z-index: 1000;
        }
        .navbar h1 { font-size: 36px; letter-spacing: 5px; font-weight: 800; text-transform: uppercase; }
        
        .container { max-width: 850px; margin: 30px auto; padding: 0 20px; }
        
        .status-bar { 
            color: #e63946; 
            font-weight: 700; 
            margin-bottom: 20px; 
            display: flex; 
            align-items: center; 
            gap: 8px;
        }
        
        .news-card { 
            background: #ffffff; 
            margin-bottom: 15px; 
            padding: 22px; 
            border-radius: 12px; 
            border-left: 8px solid #001a33; 
            transition: all 0.3s ease; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.06); 
        }
        .news-card:hover { 
            transform: translateY(-4px); 
            box-shadow: 0 8px 20px rgba(0,0,0,0.12); 
            border-left-color: #e63946;
        }
        
        .news-card a { 
            text-decoration: none; 
            color: #001a33; 
            font-size: 19px; 
            font-weight: 600; 
            line-height: 1.5; 
        }
        
        .footer { 
            text-align: center; 
            padding: 40px 0; 
            color: #6c757d; 
            font-size: 14px; 
            border-top: 1px solid #dee2e6; 
            margin-top: 40px; 
        }
        
        .empty-state { text-align: center; padding: 60px 0; color: #adb5bd; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>AXIO</h1>
    </div>
    
    <div class="container">
        <div class="status-bar">
            <span>●</span> LIVE: Latest Updates from The Daily Star
        </div>
        
        {% if news_list %}
            {% for news in news_list %}
            <div class="news-card">
                <a href="{{ news.link }}" target="_blank">{{ news.title }}</a>
            </div>
            {% endfor %}
        {% else %}
            <div class="empty-state">
                <h3>No headlines found.</h3>
                <p>Checking for latest news... Please refresh the page.</p>
            </div>
        {% endif %}
    </div>
    
    <div class="footer">
        <p>&copy; 2026 AXIO News Portal</p>
        <p>Built with Python & Flask via Termux</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    latest_news = fetch_news()
    return render_template_string(HTML_DESIGN, news_list=latest_news)

if __name__ == '__main__':
    # Run server on port 8080
    app.run(host='0.0.0.0', port=8080)


