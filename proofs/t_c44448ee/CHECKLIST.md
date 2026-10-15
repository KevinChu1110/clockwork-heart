# PowerStatDialog 發條儲能庫放置收益卡片與前往儲能快捷按鈕驗收存證 (t_c44448ee)

## 驗收重點
- [x] PowerStatDialog 捲軸中成功構建 ClockworkVaultCard 儲能庫放置收益卡片（溫暖米黃底、深藍紫描邊、橙色標題、產能效率膠囊）。
- [x] 當前產能效率膠囊 VaultRateCapsule 與 VaultRateLabel 顯示正確產能數值（150金·3鐵/h）。
- [x] 累積放置能量值 VaultEnergyLabel 支援動態刷新顯示（初始蓄能 0% -> 4小時 50% -> 8小時蓄滿上限）。
- [x] 前往儲能立體果凍按鈕 BtnGoVault 規格合規（寬 120px、高 48px 符合熱區 >= 48px、底邊 5px、圓角 18px、零系統 Emoji）。
- [x] 點擊 BtnGoVault 正確發射 vault_requested 訊號並關閉 PowerStatDialog，連動大廳直通開啟 ClockworkVaultDialog。
- [x] 完整支援六語系 i18n 即時切換無缺失（zh_TW, zh_CN, en, ja, ko, es），零系統 Emoji。

## 實機截圖清單
| 截圖檔案 | SHA256 (前 16 碼) | 說明 |
|---|---|---|

