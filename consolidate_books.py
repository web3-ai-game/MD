#!/usr/bin/env python3
"""
個人知識庫整理腳本
- 整合碎片化的小說/文本數據
- 過濾低質量內容(超短、亂碼、精簡版)
- 分類組織高質量內容
- 生成刪除報告
"""

import os
import re
import json
import shutil
from pathlib import Path
from collections import defaultdict
import hashlib

# 配置
SOURCE_DIR = "/mnt/volume_sgp1_01/gcs_dump/vps-bomb/markdown"
OUTPUT_DIR = "/mnt/volume_sgp1_01/projects/personal-knowledge-base"
WASTE_DIR = os.path.join(OUTPUT_DIR, "廢料")
BOOKS_DIR = os.path.join(OUTPUT_DIR, "books")

# 質量標準
MIN_FILE_SIZE = 10 * 1024  # 10KB 最小文件大小
MIN_CONTENT_LENGTH = 5000  # 最少5000字符
MIN_CHAPTERS = 3  # 最少章節數

# 垃圾關鍵詞
GARBAGE_KEYWORDS = [
    "test", "debug", "測試", "调试",
    "hbmb", "yq", "test_"
]

class BookAnalyzer:
    def __init__(self):
        self.stats = {
            "total": 0,
            "processed": 0,
            "kept": 0,
            "removed": 0,
            "duplicates": 0
        }
        self.removed_books = []
        self.categories = defaultdict(list)
        self.seen_hashes = {}
        
    def is_garbage_filename(self, filename):
        """檢查是否為垃圾文件名"""
        filename_lower = filename.lower()
        return any(kw in filename_lower for kw in GARBAGE_KEYWORDS)
    
    def detect_encoding_issues(self, content):
        """檢測亂碼"""
        # 檢查是否有大量亂碼字符
        garbage_chars = sum(1 for c in content if ord(c) > 0xFFFF or c == '�')
        ratio = garbage_chars / len(content) if content else 1
        return ratio > 0.05  # 超過5%認為是亂碼
    
    def count_chapters(self, content):
        """統計章節數"""
        chapter_patterns = [
            r'##\s+第.{1,5}章',
            r'第.{1,5}章',
            r'Chapter\s+\d+',
            r'##\s+\d+'
        ]
        count = 0
        for pattern in chapter_patterns:
            matches = re.findall(pattern, content)
            count = max(count, len(matches))
        return count
    
    def extract_title(self, filename, content):
        """提取書名"""
        # 從文件名提取
        title = filename.replace('.md', '')
        
        # 清理常見後綴
        title = re.sub(r'_TXT小说天堂$', '', title)
        title = re.sub(r'_.*?\.txt$', '', title)
        title = re.sub(r'\.txt$', '', title)
        
        # 嘗試從內容提取更好的標題
        lines = content.split('\n')[:10]
        for line in lines:
            if line.startswith('# ') and len(line) > 2:
                extracted = line[2:].strip()
                if len(extracted) > len(title) * 0.5:
                    title = extracted
                break
        
        return title.strip()
    
    def categorize_book(self, title, content):
        """分類書籍"""
        title_lower = title.lower()
        content_sample = content[:1000].lower()
        
        # 作者關鍵詞
        authors = {
            "阿加莎": "推理懸疑",
            "史蒂芬·金": "恐怖驚悚",
            "南派三叔": "盜墓探險",
            "天下霸唱": "盜墓探險",
            "鬼马星": "恐怖驚悚",
        }
        
        for author, category in authors.items():
            if author in title:
                return category
        
        # 關鍵詞分類
        if any(kw in title_lower for kw in ['女尊', '穿书', '重生', '穿越']):
            return "網絡小說"
        elif any(kw in title_lower for kw in ['谋杀', '探案', '侦探', '推理']):
            return "推理懸疑"
        elif any(kw in title_lower for kw in ['盗墓', '鬼吹灯', '古墓']):
            return "盜墓探險"
        elif any(kw in title_lower for kw in ['恐怖', '惊悚', '鬼', '死']):
            return "恐怖驚悚"
        elif any(kw in title_lower for kw in ['军师', '皇', '宫', '朝']):
            return "古代言情"
        else:
            return "其他"
    
    def get_content_hash(self, content):
        """計算內容哈希用於去重"""
        # 只取前10000字符計算哈希
        sample = content[:10000]
        return hashlib.md5(sample.encode('utf-8', errors='ignore')).hexdigest()
    
    def analyze_book(self, filepath):
        """分析單本書籍"""
        self.stats["total"] += 1
        filename = os.path.basename(filepath)
        
        # 讀取文件
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 無法讀取: {filename} - {e}")
            self.removed_books.append({
                "filename": filename,
                "reason": f"讀取錯誤: {e}",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查1: 垃圾文件名
        if self.is_garbage_filename(filename):
            print(f"🗑️  測試文件: {filename}")
            self.removed_books.append({
                "filename": filename,
                "reason": "測試/調試文件",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查2: 文件大小
        file_size = os.path.getsize(filepath)
        if file_size < MIN_FILE_SIZE:
            print(f"🗑️  文件過小: {filename} ({file_size} bytes)")
            self.removed_books.append({
                "filename": filename,
                "reason": f"文件過小 ({file_size} bytes)",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查3: 內容長度
        content_length = len(content)
        if content_length < MIN_CONTENT_LENGTH:
            print(f"🗑️  內容過短: {filename} ({content_length} 字符)")
            self.removed_books.append({
                "filename": filename,
                "reason": f"內容過短 ({content_length} 字符)",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查4: 亂碼
        if self.detect_encoding_issues(content):
            print(f"🗑️  檢測到亂碼: {filename}")
            self.removed_books.append({
                "filename": filename,
                "reason": "內容亂碼",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查5: 章節數
        chapter_count = self.count_chapters(content)
        if chapter_count < MIN_CHAPTERS and content_length < 50000:
            print(f"🗑️  章節過少: {filename} ({chapter_count} 章)")
            self.removed_books.append({
                "filename": filename,
                "reason": f"章節過少 ({chapter_count} 章)",
                "path": filepath
            })
            self.stats["removed"] += 1
            return None
        
        # 檢查6: 去重
        content_hash = self.get_content_hash(content)
        if content_hash in self.seen_hashes:
            print(f"🗑️  重複內容: {filename}")
            self.removed_books.append({
                "filename": filename,
                "reason": f"與 {self.seen_hashes[content_hash]} 重複",
                "path": filepath
            })
            self.stats["duplicates"] += 1
            self.stats["removed"] += 1
            return None
        
        self.seen_hashes[content_hash] = filename
        
        # 提取信息
        title = self.extract_title(filename, content)
        category = self.categorize_book(title, content)
        
        print(f"✅ 保留: {title} [{category}] ({content_length} 字符, {chapter_count} 章)")
        
        self.stats["kept"] += 1
        self.stats["processed"] += 1
        
        return {
            "filename": filename,
            "title": title,
            "category": category,
            "content": content,
            "length": content_length,
            "chapters": chapter_count,
            "source_path": filepath
        }
    
    def process_all_books(self):
        """處理所有書籍"""
        print(f"\n📚 開始掃描: {SOURCE_DIR}\n")
        
        # 創建輸出目錄
        os.makedirs(BOOKS_DIR, exist_ok=True)
        os.makedirs(WASTE_DIR, exist_ok=True)
        
        # 掃描所有markdown文件
        md_files = list(Path(SOURCE_DIR).rglob("*.md"))
        print(f"找到 {len(md_files)} 個文件\n")
        
        for filepath in md_files:
            book_info = self.analyze_book(str(filepath))
            
            if book_info:
                # 保存到分類目錄
                category = book_info["category"]
                self.categories[category].append(book_info)
        
        print(f"\n{'='*60}")
        print(f"處理完成!")
        print(f"{'='*60}")
        print(f"總文件數: {self.stats['total']}")
        print(f"保留: {self.stats['kept']}")
        print(f"移除: {self.stats['removed']}")
        print(f"  - 重複: {self.stats['duplicates']}")
        print(f"{'='*60}\n")
    
    def save_books(self):
        """保存整理後的書籍"""
        print("\n💾 保存書籍到分類目錄...\n")
        
        for category, books in self.categories.items():
            category_dir = os.path.join(BOOKS_DIR, category)
            os.makedirs(category_dir, exist_ok=True)
            
            print(f"📁 {category}: {len(books)} 本")
            
            for book in books:
                # 清理文件名
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', book['title'])
                output_path = os.path.join(category_dir, f"{safe_title}.md")
                
                # 寫入文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(book['content'])
    
    def move_waste(self):
        """移動廢料文件"""
        print(f"\n🗑️  移動 {len(self.removed_books)} 個廢料文件...\n")
        
        for item in self.removed_books:
            source = item['path']
            if os.path.exists(source):
                # 保持原始目錄結構
                rel_path = os.path.relpath(source, SOURCE_DIR)
                dest = os.path.join(WASTE_DIR, rel_path)
                
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(source, dest)
    
    def generate_reports(self):
        """生成報告"""
        print("\n📊 生成報告...\n")
        
        # 1. 刪除報告
        deletion_report = os.path.join(OUTPUT_DIR, "DELETION_REPORT.md")
        with open(deletion_report, 'w', encoding='utf-8') as f:
            f.write("# 廢料文件報告\n\n")
            f.write(f"生成時間: {os.popen('date').read().strip()}\n\n")
            f.write(f"## 統計\n\n")
            f.write(f"- 總文件數: {self.stats['total']}\n")
            f.write(f"- 保留: {self.stats['kept']}\n")
            f.write(f"- 移除: {self.stats['removed']}\n")
            f.write(f"- 重複: {self.stats['duplicates']}\n\n")
            
            f.write("## 被移除的書籍列表\n\n")
            f.write("| 書名 | 原因 |\n")
            f.write("|------|------|\n")
            
            for item in self.removed_books:
                f.write(f"| {item['filename']} | {item['reason']} |\n")
        
        # 2. 分類目錄
        catalog = os.path.join(OUTPUT_DIR, "CATALOG.md")
        with open(catalog, 'w', encoding='utf-8') as f:
            f.write("# 個人知識庫目錄\n\n")
            f.write(f"總計: {self.stats['kept']} 本書籍\n\n")
            
            for category in sorted(self.categories.keys()):
                books = self.categories[category]
                f.write(f"## {category} ({len(books)})\n\n")
                
                for book in sorted(books, key=lambda x: x['title']):
                    f.write(f"- **{book['title']}** ")
                    f.write(f"({book['length']:,} 字, {book['chapters']} 章)\n")
                
                f.write("\n")
        
        # 3. JSON元數據
        metadata = os.path.join(OUTPUT_DIR, "metadata.json")
        with open(metadata, 'w', encoding='utf-8') as f:
            data = {
                "stats": self.stats,
                "categories": {
                    cat: [{
                        "title": b['title'],
                        "filename": b['filename'],
                        "length": b['length'],
                        "chapters": b['chapters']
                    } for b in books]
                    for cat, books in self.categories.items()
                }
            }
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 報告已生成:")
        print(f"   - {deletion_report}")
        print(f"   - {catalog}")
        print(f"   - {metadata}")

def main():
    print("="*60)
    print("個人知識庫整理工具")
    print("="*60)
    
    analyzer = BookAnalyzer()
    
    # 處理所有書籍
    analyzer.process_all_books()
    
    # 保存整理後的書籍
    analyzer.save_books()
    
    # 移動廢料
    analyzer.move_waste()
    
    # 生成報告
    analyzer.generate_reports()
    
    print("\n✨ 整理完成!\n")

if __name__ == "__main__":
    main()
