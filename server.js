const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const Database = require('better-sqlite3');

const app = express();
const PORT = process.env.PORT || 3000;

// 中間件
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// 數據庫初始化
const db = new Database('reading.db');
db.exec(`
  CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_path TEXT NOT NULL,
    position INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  
  CREATE TABLE IF NOT EXISTS reading_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_path TEXT UNIQUE NOT NULL,
    scroll_position INTEGER DEFAULT 0,
    last_read DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

// 讀取元數據
const metadata = JSON.parse(fs.readFileSync('./metadata.json', 'utf-8'));

// API: 獲取分類列表
app.get('/api/categories', (req, res) => {
  const categories = Object.keys(metadata.categories).map(cat => ({
    name: cat,
    count: metadata.categories[cat].length
  }));
  res.json(categories);
});

// API: 獲取分類下的書籍列表
app.get('/api/books/:category', (req, res) => {
  const { category } = req.params;
  const books = metadata.categories[category] || [];
  res.json(books);
});

// API: 搜索書籍
app.get('/api/search', (req, res) => {
  const { q } = req.query;
  if (!q) {
    return res.json([]);
  }
  
  const results = [];
  const query = q.toLowerCase();
  
  for (const [category, books] of Object.entries(metadata.categories)) {
    for (const book of books) {
      if (book.title.toLowerCase().includes(query)) {
        results.push({ ...book, category });
      }
    }
  }
  
  res.json(results);
});

// API: 獲取書籍內容
app.get('/api/book/content', (req, res) => {
  const { category, filename } = req.query;
  
  if (!category || !filename) {
    return res.status(400).json({ error: '缺少參數' });
  }
  
  const bookPath = path.join(__dirname, 'books', category, filename);
  
  if (!fs.existsSync(bookPath)) {
    return res.status(404).json({ error: '書籍不存在' });
  }
  
  try {
    const content = fs.readFileSync(bookPath, 'utf-8');
    const html = marked(content);
    
    res.json({
      content: html,
      raw: content,
      path: `${category}/${filename}`
    });
  } catch (error) {
    res.status(500).json({ error: '讀取失敗' });
  }
});

// API: 保存閱讀進度
app.post('/api/progress', (req, res) => {
  const { book_path, scroll_position } = req.body;
  
  const stmt = db.prepare(`
    INSERT INTO reading_progress (book_path, scroll_position, last_read)
    VALUES (?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(book_path) DO UPDATE SET
      scroll_position = excluded.scroll_position,
      last_read = CURRENT_TIMESTAMP
  `);
  
  stmt.run(book_path, scroll_position);
  res.json({ success: true });
});

// API: 獲取閱讀進度
app.get('/api/progress/:book_path', (req, res) => {
  const { book_path } = req.params;
  
  const stmt = db.prepare('SELECT * FROM reading_progress WHERE book_path = ?');
  const progress = stmt.get(book_path);
  
  res.json(progress || { scroll_position: 0 });
});

// API: 添加書籤
app.post('/api/bookmark', (req, res) => {
  const { book_path, position } = req.body;
  
  const stmt = db.prepare(`
    INSERT INTO bookmarks (book_path, position)
    VALUES (?, ?)
  `);
  
  stmt.run(book_path, position);
  res.json({ success: true });
});

// API: 獲取書籤列表
app.get('/api/bookmarks/:book_path', (req, res) => {
  const { book_path } = req.params;
  
  const stmt = db.prepare('SELECT * FROM bookmarks WHERE book_path = ? ORDER BY position');
  const bookmarks = stmt.all(book_path);
  
  res.json(bookmarks);
});

// API: 刪除書籤
app.delete('/api/bookmark/:id', (req, res) => {
  const { id } = req.params;
  
  const stmt = db.prepare('DELETE FROM bookmarks WHERE id = ?');
  stmt.run(id);
  
  res.json({ success: true });
});

// 啟動服務器
app.listen(PORT, () => {
  console.log(`📚 個人知識庫服務器運行在 http://localhost:${PORT}`);
});
