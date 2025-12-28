# MD - 個人知識庫 📚

一個整理自碎片化數據的個人知識庫系統,包含 1016 本高質量書籍及其結構化數據。

## 🎯 項目簡介

MD 是一個智能知識庫系統,從 1303 個碎片化文件中提取、過濾、分類出 1016 本高質量書籍,並提供 Web 閱讀器和結構化數據支持。

## 📊 數據統計

### 書籍內容
- **總書籍**: 1,016 本
- **總大小**: ~313 MB
- **已過濾**: 287 個低質量文件
- **分類數**: 6 個

### 結構化數據
- **JSON 結構**: 1,303 個
- **命題數據**: 完整的書籍結構化分解
- **適用場景**: RAG 引擎、知識圖譜

## 📁 項目結構

```
MD/
├── README.md                 # 本文件
├── START.md                  # 快速啟動指南
├── CATALOG.md                # 完整書籍目錄
├── DELETION_REPORT.md        # 廢料報告
├── PROJECT_SUMMARY.md        # 項目總結
├── package.json              # Node 依賴
├── server.js                 # 後端服務器
├── consolidate_books.py      # 整理腳本
├── metadata.json             # 元數據
│
├── books/                    # 書籍庫 (1016本)
│   ├── 推理懸疑/            # 165 本
│   ├── 盜墓探險/            # 89 本
│   ├── 恐怖驚悚/            # 82 本
│   ├── 網絡小說/            # 145 本
│   ├── 古代言情/            # 25 本
│   └── 其他/                # 510 本
│
├── data/                     # 結構化數據
│   └── structures/          # JSON 命題結構 (1303個)
│
├── public/                   # Web 前端
│   └── index.html           # 閱讀器界面
│
└── 廢料/                    # 低質量文件 (287個)
```

## 📖 分類統計

| 分類 | 數量 | 大小 | 說明 |
|------|------|------|------|
| 其他 | 510 本 | 147 MB | 各類文學作品 |
| 推理懸疑 | 165 本 | 41 MB | 阿加莎、東野圭吾等 |
| 網絡小說 | 145 本 | 41 MB | 穿越、重生、女尊等 |
| 盜墓探險 | 89 本 | 40 MB | 鬼吹燈、盜墓筆記系列 |
| 恐怖驚悚 | 82 本 | 30 MB | 史蒂芬·金等 |
| 古代言情 | 25 本 | 6.8 MB | 古風言情小說 |

## 🚀 快速開始

### 安裝依賴
```bash
cd /mnt/sms/projects/MD
npm install
```

### 啟動閱讀器
```bash
npm start
```

訪問: **http://localhost:3000**

## ✨ 核心功能

### 已實現
- ✅ **智能分類**: 6 個分類,自動識別
- ✅ **質量過濾**: 嚴格標準,只保留優質內容
- ✅ **Web 閱讀器**: 舒適的閱讀體驗
- ✅ **實時搜索**: 快速查找書籍
- ✅ **進度保存**: 自動保存閱讀位置
- ✅ **書籤功能**: 標記重要內容
- ✅ **結構化數據**: JSON 命題結構,支持 RAG

### 計劃中
- [ ] RAG 引擎集成
- [ ] 語義搜索
- [ ] AI 問答
- [ ] 知識圖譜
- [ ] 筆記系統

## 🔍 質量控制

### 過濾標準
- ✅ 最小文件大小: 10 KB
- ✅ 最小內容長度: 5,000 字符
- ✅ 最少章節數: 3 章
- ✅ 亂碼檢測: < 5% 異常字符
- ✅ 內容去重: MD5 哈希

### 廢料處理
- **位置**: `廢料/` 目錄
- **報告**: `DELETION_REPORT.md`
- **用途**: 供後續查找好版本參考

## 📝 使用方式

### 1. 瀏覽書籍
```bash
# 查看目錄
cat CATALOG.md

# 查看分類
ls -lh books/
```

### 2. 閱讀書籍
```bash
# 命令行閱讀
cat "books/推理懸疑/無人生還_阿加莎·克里斯蒂_TXT小说天堂.md"

# Web 閱讀器
npm start
```

### 3. 搜索內容
```bash
# 搜索書名
grep -r "關鍵詞" books/

# 搜索作者
grep -l "阿加莎" books/推理懸疑/*.md
```

### 4. 使用結構化數據
```bash
# 查看 JSON 結構
cat data/structures/[hash]/structure.json

# 統計命題數量
find data/structures -name "*.json" | wc -l
```

## 🔧 技術棧

### 當前實現
- **後端**: Node.js + Express
- **數據庫**: SQLite (進度/書籤)
- **前端**: 原生 HTML/CSS/JS
- **渲染**: Marked.js (Markdown)
- **數據**: JSON (結構化命題)

### 未來擴展
- **向量化**: 用於 RAG 引擎
- **搜索**: Elasticsearch (可選)
- **AI**: LangChain + OpenAI
- **圖譜**: Neo4j (可選)

## 📊 數據來源

### 原始數據
- **來源**: GCS bucket `vps-bomb`
- **格式**: Markdown + JSON
- **處理時間**: 2025-12-16 至 2025-12-17

### 數據處理
1. 從碎片化 hash 目錄提取
2. 質量過濾與去重
3. 智能分類
4. 格式標準化
5. 結構化數據保留

## 🎨 閱讀體驗

### 長篇小說格式
- 保留原始章節結構
- Markdown 格式便於閱讀
- 1.8 行高,2em 首行縮進
- 清晰的標題層級

### 推薦閱讀器
- **命令行**: `less`, `bat`
- **GUI**: Typora, Mark Text, Obsidian
- **Web**: 內置閱讀器 (推薦)

## 🔬 結構化數據說明

### JSON 結構
每本書都有對應的 JSON 結構文件,包含:

```json
{
  "propositions": [
    {
      "id": "1",
      "text": "命題內容",
      "level": 1
    }
  ],
  "concepts": [
    {
      "name": "概念名稱",
      "frequency": 1,
      "context": "上下文"
    }
  ]
}
```

### 用途
- **RAG 引擎**: 向量化後用於語義搜索
- **知識圖譜**: 構建實體關係
- **AI 問答**: 提供結構化上下文
- **內容分析**: 主題提取、摘要生成

## 📈 性能指標

- **啟動時間**: < 2 秒
- **搜索響應**: < 100ms
- **頁面加載**: < 500ms
- **自動保存**: 每 30 秒
- **數據庫**: 輕量級 SQLite

## 🛠️ 開發指南

### 開發模式
```bash
npm run dev  # 使用 nodemon 自動重啟
```

### 端口配置
```bash
PORT=8080 npm start  # 自定義端口
```

### 重新整理數據
```bash
python3 consolidate_books.py
```

## 📦 備份建議

### 重要文件
- `books/` - 書籍內容
- `data/structures/` - 結構化數據
- `reading.db` - 閱讀數據
- `metadata.json` - 元數據

### 備份命令
```bash
tar -czf md-backup-$(date +%Y%m%d).tar.gz \
  books/ data/ reading.db metadata.json
```

## 🎯 路線圖

### Phase 1: 基礎功能 ✅
- [x] 數據整理與過濾
- [x] 智能分類
- [x] Web 閱讀器
- [x] 搜索功能
- [x] 進度保存

### Phase 2: 進階功能
- [ ] 筆記系統
- [ ] 導出/分享
- [ ] 主題切換
- [ ] 字體調整
- [ ] 閱讀統計

### Phase 3: RAG 引擎
- [ ] 向量化內容
- [ ] 語義搜索
- [ ] AI 問答
- [ ] 智能推薦
- [ ] 內容摘要

### Phase 4: 知識圖譜
- [ ] 實體識別
- [ ] 關係抽取
- [ ] 圖譜可視化
- [ ] 路徑查詢

## 🔗 相關文檔

- [START.md](START.md) - 快速啟動指南
- [CATALOG.md](CATALOG.md) - 完整書籍目錄
- [DELETION_REPORT.md](DELETION_REPORT.md) - 廢料報告
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 項目總結

## 📞 故障排除

### 端口被占用
```bash
lsof -i :3000
PORT=8080 npm start
```

### 數據庫鎖定
```bash
rm reading.db
npm start
```

### 依賴問題
```bash
rm -rf node_modules package-lock.json
npm install
```

## 🌟 項目亮點

1. **高質量過濾**: 嚴格標準,只保留優質內容
2. **智能分類**: 自動識別書籍類型
3. **結構化數據**: 支持 RAG 和知識圖譜
4. **即用閱讀器**: 開箱即用的 Web 界面
5. **完整文檔**: 詳細記錄處理過程
6. **可擴展性**: 易於添加新功能

## 📜 許可

個人使用,書籍版權歸原作者所有。

## 🎉 致謝

感謝所有書籍作者和內容創作者。

---

**項目名稱**: MD (Markdown Knowledge Base)  
**創建時間**: 2025-12-28  
**版本**: 1.0.0  
**狀態**: ✅ 完成並可用  
**位置**: `/mnt/sms/MD`
