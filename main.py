from flask import Flask, request, redirect, url_for
import datetime
import os

app = Flask(__name__)

# My personal book list (stored in memory)
books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "date": "March 2025", "rating": 5, "pages": 208},
    {"title": "Atomic Habits", "author": "James Clear", "date": "February 2025", "rating": 5, "pages": 320},
    {"title": "The Midnight Library", "author": "Matt Haig", "date": "January 2025", "rating": 4, "pages": 304},
]

@app.route("/")
def home():
    now = datetime.datetime.now().strftime("%B %d, %Y")
    
    total_books = len(books)
    avg_rating = sum(book['rating'] for book in books) / total_books if total_books > 0 else 0
    total_pages = sum(book['pages'] for book in books)
    unique_authors = len(set(book['author'] for book in books))
    
    book_items = ""
    for book in reversed(books[-5:]):
        stars = ""
        for i in range(5):
            if i < book['rating']:
                stars += '<i class="fas fa-star"></i>'
            else:
                stars += '<i class="far fa-star"></i>'
        
        book_items += f"""
        <div class="book-card">
            <div class="book-cover">
                <i class="fas fa-book-open"></i>
            </div>
            <div class="book-info">
                <h3>{book['title']}</h3>
                <p class="author"><i class="fas fa-user"></i> {book['author']}</p>
                <div class="rating">{stars}</div>
            </div>
            <div class="book-meta">
                <span><i class="fas fa-calendar"></i> {book['date']}</span>
                <span><i class="fas fa-file-alt"></i> {book['pages']} pages</span>
            </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>BookTracker | My Reading Journey</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .header h1 {{
                font-size: 3em;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                margin-bottom: 10px;
            }}
            
            .header h1 i {{
                margin-right: 15px;
            }}
            
            .header p {{
                color: white;
                font-size: 1.2em;
                opacity: 0.9;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }}
            
            .stat-card {{
                background: white;
                border-radius: 20px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
            }}
            
            .stat-card i {{
                font-size: 2.5em;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                margin-bottom: 15px;
            }}
            
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                color: #333;
                margin-bottom: 5px;
            }}
            
            .stat-label {{
                color: #666;
                font-size: 0.9em;
            }}
            
            .section {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .section h2 {{
                color: #333;
                margin-bottom: 25px;
                font-size: 1.8em;
                border-left: 4px solid #667eea;
                padding-left: 15px;
            }}
            
            .section h2 i {{
                color: #667eea;
                margin-right: 10px;
            }}
            
            .book-card {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 20px;
                transition: all 0.3s ease;
                border: 1px solid #e9ecef;
            }}
            
            .book-card:hover {{
                transform: translateX(5px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
                background: white;
                border-color: #667eea;
            }}
            
            .book-cover {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .book-cover i {{
                font-size: 2em;
                color: white;
            }}
            
            .book-info {{
                flex: 1;
            }}
            
            .book-info h3 {{
                color: #333;
                margin-bottom: 5px;
                font-size: 1.2em;
            }}
            
            .author {{
                color: #666;
                font-size: 0.9em;
                margin-bottom: 8px;
            }}
            
            .author i {{
                margin-right: 5px;
                font-size: 0.85em;
            }}
            
            .rating {{
                color: #ffc107;
            }}
            
            .rating i {{
                margin-right: 2px;
            }}
            
            .book-meta {{
                text-align: right;
                color: #888;
                font-size: 0.85em;
            }}
            
            .book-meta span {{
                display: block;
                margin: 5px 0;
            }}
            
            .book-meta i {{
                margin-right: 5px;
                width: 20px;
            }}
            
            .button-group {{
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 25px;
            }}
            
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                transition: all 0.3s ease;
                border: none;
                cursor: pointer;
                font-size: 1em;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            
            .btn i {{
                font-size: 1.1em;
            }}
            
            @media (max-width: 768px) {{
                .book-card {{
                    flex-direction: column;
                    text-align: center;
                }}
                
                .book-meta {{
                    text-align: center;
                }}
                
                .header h1 {{
                    font-size: 2em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-book-reader"></i> My Reading Journey</h1>
                <p><i class="fas fa-calendar-alt"></i> {now}</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <i class="fas fa-books"></i>
                    <div class="stat-number">{total_books}</div>
                    <div class="stat-label">Books Read</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-star"></i>
                    <div class="stat-number">{avg_rating:.1f}</div>
                    <div class="stat-label">Average Rating</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-users"></i>
                    <div class="stat-number">{unique_authors}</div>
                    <div class="stat-label">Authors</div>
                </div>
                <div class="stat-card">
                    <i class="fas fa-file-alt"></i>
                    <div class="stat-number">{total_pages}</div>
                    <div class="stat-label">Pages Read</div>
                </div>
            </div>
            
            <div class="section">
                <h2><i class="fas fa-clock"></i> Recently Added</h2>
                {book_items}
            </div>
            
            <div class="button-group">
                <a href="/add" class="btn"><i class="fas fa-plus-circle"></i> Add New Book</a>
                <a href="/all" class="btn"><i class="fas fa-list"></i> View All Books</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/all")
def all_books():
    total_books = len(books)
    total_pages = sum(book['pages'] for book in books)
    
    book_items = ""
    for book in reversed(books):
        stars = ""
        for i in range(5):
            if i < book['rating']:
                stars += '<i class="fas fa-star"></i>'
            else:
                stars += '<i class="far fa-star"></i>'
        
        book_items += f"""
        <div class="book-card">
            <div class="book-cover">
                <i class="fas fa-book"></i>
            </div>
            <div class="book-info">
                <h3>{book['title']}</h3>
                <p class="author"><i class="fas fa-user"></i> {book['author']}</p>
                <div class="rating">{stars}</div>
            </div>
            <div class="book-meta">
                <span><i class="fas fa-calendar"></i> {book['date']}</span>
                <span><i class="fas fa-file-alt"></i> {book['pages']} pages</span>
            </div>
        </div>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>All Books | BookTracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }}
            
            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }}
            
            .header h1 i {{
                margin-right: 15px;
            }}
            
            .header p {{
                color: white;
                font-size: 1.1em;
                margin-top: 10px;
            }}
            
            .section {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }}
            
            .book-card {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 20px;
                transition: all 0.3s ease;
                border: 1px solid #e9ecef;
            }}
            
            .book-card:hover {{
                transform: translateX(5px);
                background: white;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
                border-color: #667eea;
            }}
            
            .book-cover {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .book-cover i {{
                font-size: 2em;
                color: white;
            }}
            
            .book-info {{
                flex: 1;
            }}
            
            .book-info h3 {{
                color: #333;
                margin-bottom: 5px;
            }}
            
            .author {{
                color: #666;
                font-size: 0.9em;
                margin-bottom: 8px;
            }}
            
            .author i {{
                margin-right: 5px;
            }}
            
            .rating {{
                color: #ffc107;
            }}
            
            .rating i {{
                margin-right: 2px;
            }}
            
            .book-meta {{
                text-align: right;
                color: #888;
                font-size: 0.85em;
            }}
            
            .book-meta span {{
                display: block;
                margin: 5px 0;
            }}
            
            .book-meta i {{
                margin-right: 5px;
                width: 20px;
            }}
            
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                margin-top: 25px;
                transition: all 0.3s ease;
            }}
            
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            
            @media (max-width: 768px) {{
                .book-card {{
                    flex-direction: column;
                    text-align: center;
                }}
                
                .book-meta {{
                    text-align: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-book"></i> My Complete Library</h1>
                <p><i class="fas fa-chart-line"></i> {total_books} books • {total_pages} pages read</p>
            </div>
            
            <div class="section">
                {book_items}
                <a href="/" class="btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route("/add", methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = int(request.form['rating'])
        pages = int(request.form['pages'])
        date = datetime.datetime.now().strftime("%B %Y")
        
        books.append({
            "title": title,
            "author": author,
            "date": date,
            "rating": rating,
            "pages": pages
        })
        
        return redirect(url_for('home'))
    
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Book | BookTracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            
            .container {
                max-width: 550px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .header h1 {
                font-size: 2.5em;
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            
            .header h1 i {
                margin-right: 15px;
            }
            
            .card {
                background: white;
                border-radius: 20px;
                padding: 35px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
            }
            
            label i {
                color: #667eea;
                margin-right: 8px;
            }
            
            input, select {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                font-size: 1em;
                transition: all 0.3s ease;
            }
            
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            }
            
            .button-group {
                display: flex;
                gap: 15px;
                margin-top: 30px;
            }
            
            .btn {
                flex: 1;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                padding: 12px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                border: none;
                cursor: pointer;
                font-size: 1em;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            .btn-secondary:hover {
                box-shadow: 0 5px 15px rgba(108, 117, 125, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-plus-circle"></i> Add a Book</h1>
                <p><i class="fas fa-smile"></i> What did you read recently?</p>
            </div>
            
            <div class="card">
                <form method="POST">
                    <div class="form-group">
                        <label><i class="fas fa-book"></i> Book Title</label>
                        <input type="text" name="title" required placeholder="Enter book title">
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> Author</label>
                        <input type="text" name="author" required placeholder="Enter author name">
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-file-alt"></i> Pages</label>
                        <input type="number" name="pages" required placeholder="Number of pages">
                    </div>
                    
                    <div class="form-group">
                        <label><i class="fas fa-star"></i> Your Rating</label>
                        <select name="rating" required>
                            <option value="5">⭐⭐⭐⭐⭐ - Masterpiece (5)</option>
                            <option value="4">⭐⭐⭐⭐ - Great (4)</option>
                            <option value="3">⭐⭐⭐ - Good (3)</option>
                            <option value="2">⭐⭐ - Average (2)</option>
                            <option value="1">⭐ - Disappointing (1)</option>
                        </select>
                    </div>
                    
                    <div class="button-group">
                        <button type="submit" class="btn"><i class="fas fa-save"></i> Save Book</button>
                        <a href="/" class="btn btn-secondary"><i class="fas fa-times"></i> Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)