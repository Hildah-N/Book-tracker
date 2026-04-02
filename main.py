from flask import Flask, request, redirect, url_for, render_template_string
import datetime
import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, text, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# ===== ENVIRONMENT CONFIGURATION =====
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///books.db')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
APP_ENV = os.environ.get('APP_ENV', 'development')

print(f"✅ Running in {APP_ENV} mode")
print(f"📧 Admin contact: {ADMIN_EMAIL}")

# ===== DATABASE INTEGRATION =====
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    pages = Column(Integer, nullable=False)
    date_read = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

Base.metadata.create_all(engine)

# ===== SHARED CSS =====
SHARED_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    :root {
        --ink: #1a1a2e;
        --ink-soft: #4a4a6a;
        --ink-muted: #8888aa;
        --cream: #faf8f4;
        --warm: #f5f0e8;
        --accent: #c0392b;
        --accent-soft: #e74c3c;
        --gold: #d4a843;
        --green: #27ae60;
        --surface: #ffffff;
        --border: #e8e4dc;
        --shadow: 0 2px 16px rgba(26,26,46,0.08);
        --shadow-hover: 0 8px 32px rgba(26,26,46,0.14);
        --radius: 12px;
        --radius-lg: 20px;
    }

    body {
        font-family: 'DM Sans', sans-serif;
        background: var(--cream);
        color: var(--ink);
        min-height: 100vh;
    }

    /* ── NAV ── */
    .nav {
        background: var(--ink);
        padding: 0 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 60px;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .nav-brand {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: var(--cream);
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .nav-brand i { color: var(--gold); font-size: 1rem; }
    .nav-links { display: flex; gap: 8px; }
    .nav-link {
        color: #aaa;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: 8px;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .nav-link:hover { color: var(--cream); background: rgba(255,255,255,0.1); }
    .nav-link.primary {
        background: var(--accent);
        color: white;
    }
    .nav-link.primary:hover { background: var(--accent-soft); }

    /* ── PAGE WRAPPER ── */
    .page { max-width: 980px; margin: 0 auto; padding: 36px 24px; }

    /* ── PAGE TITLE ── */
    .page-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 6px;
    }
    .page-subtitle { color: var(--ink-muted); font-size: 0.9rem; margin-bottom: 32px; }

    /* ── STAT CARDS ── */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 36px;
    }
    .stat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: var(--shadow);
        transition: all 0.25s ease;
        cursor: default;
    }
    .stat-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-4px);
        border-color: #d0ccc4;
    }
    .stat-icon {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .stat-icon.red { background: #fde8e8; color: var(--accent); }
    .stat-icon.gold { background: #fdf3dc; color: var(--gold); }
    .stat-icon.blue { background: #dbeafe; color: #2563eb; }
    .stat-icon.green { background: #dcfce7; color: var(--green); }
    .stat-icon i { font-size: 1.1rem; }
    .stat-body {}
    .stat-number { font-size: 1.5rem; font-weight: 700; line-height: 1; color: var(--ink); }
    .stat-label { font-size: 0.75rem; color: var(--ink-muted); margin-top: 2px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em; }

    /* ── SECTION ── */
    .section {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow);
        margin-bottom: 24px;
    }
    .section-header {
        padding: 18px 24px;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--ink);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title i { color: var(--accent); font-size: 0.9rem; }
    .section-body { padding: 8px 0; }

    /* ── BOOK ROW ── */
    .book-row {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 14px 24px;
        border-bottom: 1px solid var(--border);
        transition: background 0.15s;
    }
    .book-row:last-child { border-bottom: none; }
    .book-row:hover { background: var(--warm); }

    .book-spine {
        width: 40px;
        height: 52px;
        background: linear-gradient(135deg, var(--ink) 0%, #2d2d4e 100%);
        border-radius: 4px 8px 8px 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
    }
    .book-spine i { color: var(--gold); font-size: 1rem; }

    .book-main { flex: 1; min-width: 0; }
    .book-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--ink);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .book-author {
        font-size: 0.8rem;
        color: var(--ink-muted);
        margin-top: 2px;
    }

    .book-rating { color: var(--gold); font-size: 0.8rem; letter-spacing: 1px; }
    .book-rating .empty { color: #ddd; }

    .book-meta {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 3px;
        color: var(--ink-muted);
        font-size: 0.78rem;
        white-space: nowrap;
    }
    .book-meta i { margin-right: 4px; }

    /* ── ACTION BUTTONS ── */
    .row-actions { display: flex; gap: 6px; align-items: center; }
    .btn-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--surface);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: var(--ink-soft);
        font-size: 0.8rem;
        text-decoration: none;
        transition: all 0.2s;
    }
    .btn-icon:hover { background: var(--ink); color: white; border-color: var(--ink); }
    .btn-icon.danger:hover { background: var(--accent); border-color: var(--accent); color: white; }

    /* ── FORM ELEMENTS ── */
    .form-card {
        max-width: 520px;
        margin: 0 auto;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 36px;
        box-shadow: var(--shadow);
    }
    .form-group { margin-bottom: 20px; }
    .form-label {
        display: block;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--ink-soft);
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .form-input, .form-select {
        width: 100%;
        padding: 10px 14px;
        border: 1.5px solid var(--border);
        border-radius: var(--radius);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: var(--ink);
        background: var(--cream);
        transition: border-color 0.2s;
        appearance: none;
    }
    .form-input:focus, .form-select:focus {
        outline: none;
        border-color: var(--accent);
        background: white;
    }

    /* ── BUTTONS ── */
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border-radius: var(--radius);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
        border: none;
        transition: all 0.2s;
    }
    .btn-primary { background: var(--ink); color: white; }
    .btn-primary:hover { background: #2d2d4e; }
    .btn-accent { background: var(--accent); color: white; }
    .btn-accent:hover { background: var(--accent-soft); }
    .btn-ghost { background: transparent; color: var(--ink-soft); border: 1.5px solid var(--border); }
    .btn-ghost:hover { background: var(--warm); }
    .btn-full { width: 100%; justify-content: center; padding: 12px; }

    /* ── EMPTY STATE ── */
    .empty-state {
        text-align: center;
        padding: 60px 24px;
        color: var(--ink-muted);
    }
    .empty-state i { font-size: 3rem; margin-bottom: 16px; display: block; }
    .empty-state p { font-size: 0.9rem; }

    /* ── BADGE ── */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        background: var(--warm);
        color: var(--ink-soft);
        border: 1px solid var(--border);
    }

    /* ── HEALTH PAGE ── */
    .health-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .health-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px;
    }
    .health-status { display: flex; align-items: center; gap: 10px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .dot.green { background: var(--green); box-shadow: 0 0 0 3px #dcfce7; }
    .dot.red { background: var(--accent); box-shadow: 0 0 0 3px #fde8e8; }
    .health-label { font-size: 0.8rem; color: var(--ink-muted); margin-top: 4px; }
    .health-value { font-weight: 600; font-size: 0.95rem; }

    @media (max-width: 700px) {
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .book-meta { display: none; }
        .nav-links .nav-link span { display: none; }
    }
</style>
"""

def render_stars(rating, max_rating=5):
    filled = "★" * rating
    empty = "☆" * (max_rating - rating)
    return f'<span class="book-rating">{filled}<span class="empty">{empty}</span></span>'

def nav_html(active=""):
    return f"""
    <nav class="nav">
        <a href="/" class="nav-brand"><i class="fas fa-bookmark"></i> BookTracker</a>
        <div class="nav-links">
            <a href="/" class="nav-link {'primary' if active=='home' else ''}"><i class="fas fa-home"></i> <span>Home</span></a>
            <a href="/all" class="nav-link {'primary' if active=='library' else ''}"><i class="fas fa-books"></i> <span>Library</span></a>
            <a href="/add" class="nav-link {'primary' if active=='add' else ''}"><i class="fas fa-plus"></i> <span>Add Book</span></a>
            <a href="/health" class="nav-link {'primary' if active=='health' else ''}"><i class="fas fa-heartbeat"></i> <span>Health</span></a>
        </div>
    </nav>
    """

@app.route("/")
def home():
    session = Session()
    books = session.query(Book).order_by(desc(Book.created_at)).all()
    session.close()

    total_books = len(books)
    avg_rating = sum(b.rating for b in books) / total_books if total_books > 0 else 0
    unique_authors = len(set(b.author for b in books))
    total_pages = sum(b.pages for b in books)

    book_rows = ""
    for book in books[:8]:
        book_rows += f"""
        <div class="book-row">
            <div class="book-spine"><i class="fas fa-book"></i></div>
            <div class="book-main">
                <div class="book-title">{book.title}</div>
                <div class="book-author"><i class="fas fa-user" style="font-size:0.7rem"></i> {book.author}</div>
            </div>
            {render_stars(book.rating)}
            <div class="book-meta">
                <span><i class="fas fa-file-alt"></i>{book.pages} pp</span>
                <span><i class="fas fa-calendar"></i>{book.date_read}</span>
            </div>
        </div>
        """

    if not book_rows:
        book_rows = """
        <div class="empty-state">
            <i class="fas fa-book-open"></i>
            <p>No books yet. Add your first book to get started!</p>
        </div>
        """

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>BookTracker – My Reading Journey</title>
        {SHARED_CSS}
    </head>
    <body>
        {nav_html('home')}
        <div class="page">
            <h1 class="page-title">My Reading Journey</h1>
            <p class="page-subtitle"><i class="fas fa-calendar-alt"></i> {datetime.datetime.now().strftime('%B %d, %Y')}</p>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon red"><i class="fas fa-book-open"></i></div>
                    <div class="stat-body">
                        <div class="stat-number">{total_books}</div>
                        <div class="stat-label">Books Read</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon gold"><i class="fas fa-star"></i></div>
                    <div class="stat-body">
                        <div class="stat-number">{avg_rating:.1f}</div>
                        <div class="stat-label">Avg Rating</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon blue"><i class="fas fa-users"></i></div>
                    <div class="stat-body">
                        <div class="stat-number">{unique_authors}</div>
                        <div class="stat-label">Authors</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon green"><i class="fas fa-file-alt"></i></div>
                    <div class="stat-body">
                        <div class="stat-number">{total_pages:,}</div>
                        <div class="stat-label">Total Pages</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-header">
                    <span class="section-title"><i class="fas fa-clock"></i> Recently Added</span>
                    <a href="/all" class="btn btn-ghost" style="padding:6px 14px;font-size:0.82rem">View All <i class="fas fa-arrow-right"></i></a>
                </div>
                <div class="section-body">
                    {book_rows}
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route("/all")
def all_books():
    session = Session()
    books = session.query(Book).order_by(desc(Book.created_at)).all()
    session.close()

    book_rows = ""
    for book in books:
        book_rows += f"""
        <div class="book-row">
            <div class="book-spine"><i class="fas fa-book"></i></div>
            <div class="book-main">
                <div class="book-title">{book.title}</div>
                <div class="book-author"><i class="fas fa-user" style="font-size:0.7rem"></i> {book.author}</div>
            </div>
            {render_stars(book.rating)}
            <div class="book-meta">
                <span><i class="fas fa-file-alt"></i>{book.pages} pp</span>
                <span><i class="fas fa-calendar"></i>{book.date_read}</span>
            </div>
            <div class="row-actions">
                <a href="/edit/{book.id}" class="btn-icon" title="Edit"><i class="fas fa-pencil"></i></a>
                <form method="POST" action="/delete/{book.id}" style="display:inline" onsubmit="return confirm('Delete \\'{book.title}\\'?')">
                    <button type="submit" class="btn-icon danger" title="Delete"><i class="fas fa-trash"></i></button>
                </form>
            </div>
        </div>
        """

    if not book_rows:
        book_rows = """
        <div class="empty-state">
            <i class="fas fa-book-open"></i>
            <p>Your library is empty. <a href="/add">Add your first book!</a></p>
        </div>
        """

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Library – BookTracker</title>
        {SHARED_CSS}
    </head>
    <body>
        {nav_html('library')}
        <div class="page">
            <h1 class="page-title">My Library</h1>
            <p class="page-subtitle">{len(books)} book{'s' if len(books) != 1 else ''} in your collection</p>

            <div class="section">
                <div class="section-header">
                    <span class="section-title"><i class="fas fa-list"></i> All Books</span>
                    <a href="/add" class="btn btn-accent" style="padding:6px 14px;font-size:0.82rem"><i class="fas fa-plus"></i> Add Book</a>
                </div>
                <div class="section-body">
                    {book_rows}
                </div>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route("/add", methods=['GET', 'POST'])
def add_book():
    error = ""
    if request.method == 'POST':
        try:
            session = Session()
            new_book = Book(
                title=request.form['title'].strip(),
                author=request.form['author'].strip(),
                rating=int(request.form['rating']),
                pages=int(request.form['pages']),
                date_read=datetime.datetime.now().strftime("%B %Y")
            )
            session.add(new_book)
            session.commit()
            session.close()
            return redirect(url_for('home'))
        except Exception as e:
            error = f"Error saving book: {str(e)}"

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Add Book – BookTracker</title>
        {SHARED_CSS}
    </head>
    <body>
        {nav_html('add')}
        <div class="page">
            <h1 class="page-title">Add a Book</h1>
            <p class="page-subtitle">Log a book you've read to your collection</p>

            {'<p style="color:var(--accent);margin-bottom:16px">' + error + '</p>' if error else ''}

            <div class="form-card">
                <form method="POST">
                    <div class="form-group">
                        <label class="form-label">Book Title</label>
                        <input class="form-input" type="text" name="title" placeholder="e.g. The Pragmatic Programmer" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Author</label>
                        <input class="form-input" type="text" name="author" placeholder="e.g. Andrew Hunt" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Number of Pages</label>
                        <input class="form-input" type="number" name="pages" min="1" placeholder="e.g. 352" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Rating</label>
                        <select class="form-select" name="rating">
                            <option value="5">★★★★★ — Masterpiece</option>
                            <option value="4">★★★★☆ — Great</option>
                            <option value="3" selected>★★★☆☆ — Good</option>
                            <option value="2">★★☆☆☆ — Average</option>
                            <option value="1">★☆☆☆☆ — Disappointing</option>
                        </select>
                    </div>
                    <div style="display:flex;gap:12px;margin-top:8px">
                        <button type="submit" class="btn btn-primary btn-full">
                            <i class="fas fa-check"></i> Save Book
                        </button>
                        <a href="/" class="btn btn-ghost btn-full">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit_book(book_id):
    session = Session()
    book = session.query(Book).filter_by(id=book_id).first()

    if not book:
        session.close()
        return redirect(url_for('all_books'))

    error = ""
    if request.method == 'POST':
        try:
            book.title = request.form['title'].strip()
            book.author = request.form['author'].strip()
            book.rating = int(request.form['rating'])
            book.pages = int(request.form['pages'])
            book.updated_at = datetime.datetime.now()
            session.commit()
            session.close()
            return redirect(url_for('all_books'))
        except Exception as e:
            error = f"Error updating book: {str(e)}"

    def sel(val):
        return 'selected' if book.rating == val else ''

    title_val = book.title
    author_val = book.author
    pages_val = book.pages
    session.close()

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Edit Book – BookTracker</title>
        {SHARED_CSS}
    </head>
    <body>
        {nav_html()}
        <div class="page">
            <h1 class="page-title">Edit Book</h1>
            <p class="page-subtitle">Update the details for this entry</p>

            {'<p style="color:var(--accent);margin-bottom:16px">' + error + '</p>' if error else ''}

            <div class="form-card">
                <form method="POST">
                    <div class="form-group">
                        <label class="form-label">Book Title</label>
                        <input class="form-input" type="text" name="title" value="{title_val}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Author</label>
                        <input class="form-input" type="text" name="author" value="{author_val}" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Number of Pages</label>
                        <input class="form-input" type="number" name="pages" value="{pages_val}" min="1" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Rating</label>
                        <select class="form-select" name="rating">
                            <option value="5" {sel(5)}>★★★★★ — Masterpiece</option>
                            <option value="4" {sel(4)}>★★★★☆ — Great</option>
                            <option value="3" {sel(3)}>★★★☆☆ — Good</option>
                            <option value="2" {sel(2)}>★★☆☆☆ — Average</option>
                            <option value="1" {sel(1)}>★☆☆☆☆ — Disappointing</option>
                        </select>
                    </div>
                    <div style="display:flex;gap:12px;margin-top:8px">
                        <button type="submit" class="btn btn-primary btn-full">
                            <i class="fas fa-check"></i> Update Book
                        </button>
                        <a href="/all" class="btn btn-ghost btn-full">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </body>
    </html>
    """)


@app.route("/delete/<int:book_id>", methods=['POST'])
def delete_book(book_id):
    session = Session()
    book = session.query(Book).filter_by(id=book_id).first()
    if book:
        session.delete(book)
        session.commit()
    session.close()
    return redirect(url_for('all_books'))


@app.route("/health")
def health():
    db_ok = False
    db_msg = "disconnected"
    try:
        session = Session()
        session.execute(text("SELECT 1"))
        session.close()
        db_ok = True
        db_msg = "connected"
    except Exception as e:
        db_msg = str(e)

    status_code = 200 if db_ok else 500
    dot_class = "green" if db_ok else "red"

    session2 = Session()
    book_count = session2.query(Book).count()
    session2.close()

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Health – BookTracker</title>
        {SHARED_CSS}
    </head>
    <body>
        {nav_html('health')}
        <div class="page">
            <h1 class="page-title">System Health</h1>
            <p class="page-subtitle">Live status of your BookTracker instance</p>

            <div class="health-grid">
                <div class="health-card">
                    <div class="health-status">
                        <div class="dot {dot_class}"></div>
                        <div>
                            <div class="health-value">{'Healthy' if db_ok else 'Unhealthy'}</div>
                            <div class="health-label">Overall Status</div>
                        </div>
                    </div>
                </div>
                <div class="health-card">
                    <div class="health-status">
                        <div class="dot {dot_class}"></div>
                        <div>
                            <div class="health-value">Database {db_msg}</div>
                            <div class="health-label">SQLAlchemy / SQLite</div>
                        </div>
                    </div>
                </div>
                <div class="health-card">
                    <div class="health-value">{APP_ENV}</div>
                    <div class="health-label">Environment</div>
                </div>
                <div class="health-card">
                    <div class="health-value">{book_count} books</div>
                    <div class="health-label">Records in Database</div>
                </div>
                <div class="health-card" style="grid-column: 1/-1">
                    <div class="health-value" style="font-size:0.85rem;font-family:monospace">{datetime.datetime.now().isoformat()}</div>
                    <div class="health-label">Server Timestamp</div>
                </div>
            </div>

            <div style="margin-top:24px">
                <a href="/" class="btn btn-ghost"><i class="fas fa-arrow-left"></i> Back Home</a>
            </div>
        </div>
    </body>
    </html>
    """), status_code


@app.route("/env")
def env_info():
    return {
        "APP_ENV": APP_ENV,
        "ADMIN_EMAIL": ADMIN_EMAIL,
        "database_configured": bool(DATABASE_URL),
        "note": "Sensitive values are never exposed"
    }


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=(APP_ENV == 'development'))