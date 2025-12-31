# 📚 Novel AI Inference Engine

基於 1016 本中文小說的 AI 推演引擎 - 使用 xAI Grok API 進行角色扮演、劇情推演與互動式故事創作。

## 🎯 項目概述

這是一個創新的 AI 驅動小說推演平台，利用海量中文小說作為知識庫，結合 xAI 的 Grok 模型進行：

- **角色扮演推演** - 扮演小說中的角色進行對話
- **劇情分支模擬** - 探索「如果...會怎樣」的替代劇情
- **跨作品角色碰撞** - 讓不同小說的角色相遇互動
- **風格遷移創作** - 用某作者的風格續寫其他故事

## 📊 小說資料庫統計

| 分類 | 數量 | 描述 |
|------|------|------|
| 🔮 其他 | 510 | 綜合類型小說 |
| 🔍 推理懸疑 | 165 | 偵探推理、懸疑燒腦 |
| 💀 恐怖驚悚 | 82 | 恐怖小說、驚悚故事 |
| ⛏️ 盜墓探險 | 89 | 盜墓探險、冒險類 |
| �� 網絡小說 | 145 | 網絡連載作品 |
| 💕 古代言情 | 25 | 古風言情小說 |
| **總計** | **1016** | |

## 🚀 快速開始

### 1. 配置 API 密鑰（唯一需要修改的地方）

編輯 `config.js` 文件：

```javascript
// config.js
module.exports = {
  XAI_API_KEY: "xai-xxxxxxxxxxxxxxxxxxxxxxxx"  // 👈 填入你的 xAI API Key
};
```

### 2. 安裝依賴並啟動

```bash
npm install
npm start
```

### 3. 開始推演

訪問 `http://localhost:3000`

## 💡 使用場景

### 場景一：角色對話推演
```
輸入: 我想和《鬼吹燈》裡的胡八一對話
AI: [以胡八一的身份回應]
```

### 場景二：劇情分支探索
```
輸入: 如果《盜墓筆記》裡的吳邪沒有進入七星魯王宮？
AI: [推演替代劇情線]
```

### 場景三：跨作品碰撞
```
輸入: 讓福爾摩斯來調查《心理罪》中的案件
AI: [融合兩部作品創造新故事]
```

## 📁 項目結構

```
MD/
├── config.js                 # ⭐ API 配置（唯一需修改）
├── server.js                 # 服務端主程序
├── public/index.html         # 前端界面
├── books/                    # 1016 本小說
│   ├── 恐怖驚悚/            # 82 本
│   ├── 推理懸疑/            # 165 本
│   ├── 盜墓探險/            # 89 本
│   ├── 網絡小說/            # 145 本
│   ├── 古代言情/            # 25 本
│   └── 其他/                # 510 本
├── README.md                 # 本文件
└── 用戶手冊.md              # 詳細使用說明
```

## ⚡ xAI API 預算規劃 ($30/3hr)

| 模型 | 輸入 | 輸出 | 預估對話 |
|------|------|------|----------|
| grok-2 | $2/1M | $10/1M | ~150 輪深度對話 |
| grok-2-mini | $0.10/1M | $0.50/1M | ~3000+ 輪 |

**極限燒法**: 混合使用，mini 探索 + 標準精品。

## 🔧 核心 API 調用

```javascript
const { XAI_API_KEY } = require('./config');

const response = await fetch('https://api.x.ai/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${XAI_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'grok-2',
    messages: [
      { role: 'system', content: `小說推演引擎。基於：\n${novelContent}` },
      { role: 'user', content: userPrompt }
    ],
    temperature: 0.8
  })
});
```

---

**GitHub**: [web3-ai-game/db](https://github.com/web3-ai-game/db)
