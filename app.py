from flask import Flask, render_template_string
import requests

app = Flask(__name__)

def fetch_news():
    # Using a different open-source news feed
    url = "https://ok.surf/api/v1/cors/news-feed"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # We will take news from the 'Business' or 'World' section
        raw_news = data.get('World', [])
        news_list = []
        
        for item in raw_news[:15]:
            news_list.append({
                'title': item.get('title'),
                'link': item.get('sourceUrl')
            })
        return news_list
    except Exception as e:
        print(f"Error: {e}")
        return []

HTML_DESIGN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AXIO | Global News</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #1c1e21; }
        .header { background: #001f3f; color: white; padding: 30px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .header h1 { font-size: 40px; letter-spacing: 8px; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 15px; }
        .card { 
            background: white; 
            margin-bottom: 15px; 
            padding: 20px; 
            border-radius: 10px; 
            border-left: 8px solid #e63946;
            transition: 0.3s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
        .card a { text-decoration: none; color: #001f3f; font-size: 18px; font-weight: bold; }
        .footer { text-align: center; margin-top: 50px; color: #777; font-size: 14px; padding-bottom: 30px; }
    </style>
</head>
<body>
    <div class="header"><h1>AXIO</h1></div>
    <div class="container">
        <p style="margin-bottom:15px; color:#e63946;"><b>● LIVE WORLD UPDATES</b></p>
        {% if news_list %}
            {% for news in news_list %}
            <div class="card">
                <a href="{{ news.link }}" target="_blank">{{ news.title }}</a>
            </div>
            {% endfor %}
        {% else %}
            <div style="background:white; padding:40px; border-radius:10px; text-align:center;">
                <p>Connecting to global servers... Please check your internet and refresh.</p>
            </div>
        {% endif %}
    </div>
    <div class="footer">
        <p>AXIO Portal &copy; 2026 | Developed by Irfan Ahmed</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    news = fetch_news()
    return render_template_string(HTML_DESIGN, news_list=news)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
