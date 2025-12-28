# GitHub 推送指南

## 創建 GitHub 倉庫

1. 訪問 GitHub: https://github.com/new
2. 倉庫名稱: `MD`
3. 描述: `個人知識庫 - 1016本書籍 + 結構化數據`
4. 設為 Private (推薦)
5. 不要初始化 README

## 推送到 GitHub

```bash
cd /mnt/volume_sgp1_01/projects/MD

# 添加遠程倉庫 (替換 YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/MD.git

# 推送
git branch -M main
git push -u origin main
```

## 使用 Personal Access Token

如果需要認證:

1. 生成 Token: https://github.com/settings/tokens
2. 選擇 `repo` 權限
3. 使用 Token 作為密碼

```bash
git push -u origin main
# Username: YOUR_USERNAME
# Password: YOUR_TOKEN
```

## 後續推送

```bash
git add .
git commit -m "Update: description"
git push
```

## 當前狀態

- ✅ Git 已初始化
- ✅ 所有文件已提交
- ✅ 廢料已在 .gitignore
- ⏳ 等待推送到 GitHub

## 倉庫大小

- Books: ~313 MB
- Structures: ~34 MB
- Total: ~350 MB (不含廢料)
