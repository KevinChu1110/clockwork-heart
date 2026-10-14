# PowerStatDialog 木人樁試招紀錄卡片與前往試招快捷按鈕驗收存證 (t_36384dbb)

## 驗收重點
- [x] PowerStatDialog 捲軸中具備 DummyTrialCard 木人樁試招卡片（溫暖米黃底 #FFF8E7、深藍紫描邊 #1F1A3A、圓角 14px、底邊 4px）。
- [x] 未試招引導狀態：best_dummy_dps <= 0 時顯示 NoRecordGuideLabel 引導文字，DPS 徽章顯示尚未試招。
- [x] 歷史最佳記錄狀態：best_dummy_dps > 0 時徽章顯示最佳 DPS 數值，詳情列顯示最高單擊 MaxHitLabel 與出招記錄 HitCountLabel。
- [x] 前往試招果凍按鈕 BtnGoDummyPractice 規格尺寸合規（寬 120px、高 48px、底邊 5px、圓角 18px、零系統 Emoji）。
- [x] 點擊 BtnGoDummyPractice 正確發射 go_dummy_practice 訊號並關閉彈窗，連動大廳觸發 request_battle("training_dummy") 進入木人樁試招。
- [x] 完整支援六語系即時切換（zh_TW, zh_CN, en, ja, ko, es），無缺漏字或 Emoji。

## 存證截圖列表
| 檔案名稱 | SHA256 (前 16 碼) | 說明 |
|---|---|---|
| `proof_01_dummy_trial_card_no_record.png` | `0286d40734a6a6fb` | DummyTrialCard 無紀錄狀態展示（尚未試招引導、按鈕合規、零 Emoji） |
| `proof_02_dummy_trial_card_has_record.png` | `dcb662405fab89c9` | DummyTrialCard 有紀錄狀態展示（最佳 DPS 徽章、最高單擊、出招記錄、零 Emoji） |
| `proof_03_dummy_trial_card_zh_TW.png` | `d309b82c2baceb60` | 六語系展示：繁體中文 (zh_TW) 木人樁試招 / 前往試招 |
| `proof_04_dummy_trial_card_en.png` | `c88ccb4ee68ee89d` | 六語系展示：英文 (en) Dummy Trial / Practice |
| `proof_05_dummy_trial_card_ja.png` | `39d1abadf04e3da6` | 六語系展示：日文 (ja) 木人試練 / 試練へ |
| `proof_06_dummy_trial_card_ko.png` | `32417fb00e8d9d8a` | 六語系展示：韓文 (ko) 목인 시험 / 시험장 이동 |
| `proof_07_dummy_trial_card_es.png` | `f7619ef6f018fafd` | 六語系展示：西文 (es) Prueba de Muñeco / Ir a Prueba |
| `proof_08_dummy_trial_card_zh_CN.png` | `24c14b72c0a7c445` | 六語系展示：簡體中文 (zh_CN) 木人桩试招 / 前往试招 |

