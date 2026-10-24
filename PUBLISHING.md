# 無邊界學習專題文章

這個 repository 只負責靜態公開網站；文章在 Google Cloud 的 1221 後台管理。

- 首頁無邊界學習區顯示最新三篇；`articles/index.html` 顯示全部已發布文章，可搜尋集數、主題及文字並依分類篩選。
- 每篇文章固定網址為 `articles/{集數}/`，包含完整圖文、圖片標題與圖說、Podcast 播放器。
- 後台發布程式將頁面、圖片與 `articles/publication-state.json` 原子提交到網站的來源分支，再等待 Pages 公開版本確認。編輯中稿件不會自動公開。
- 本 PR 索引預設為空，不包含第 12 集或其他測試稿。文章會等雲端後台核准部署並操作發布才出現。
- 本機測試用後台的 `pnpm dev:publishing`，以 `PUBLISH_LOCAL_SITE_DIR` 指向網站副本。測試會寫入該副本，因此測試生成的 `articles/{集數}/`、`articles/assets/` 與索引內容不要提交。
- 沿用現有 GitHub Pages 部署設定，不在這次開發期間變更 Settings 或部署。合併後需確認來源分支及目錄包含 `articles/`。
- 首頁簡體版也提供文章專區入口；文章保留編輯後台的原始繁體內容，不會自動翻譯。

CSS/JS 用相對路徑，支援 `/introduce-self/` 子路徑。列表不依賴登入後台；每篇 HTML 可獨立閱讀。公開索引只包含已發布文章的摘要資料與工作版本標記，不含後台憑證。
