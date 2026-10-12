extends SceneTree
## 《發條之心》三大戰鬥回饋與指點快捷全面回歸驗收說明 (t_655239f0)
## 依據場景生命週期架構，實機截圖分別由下列兩工具執行：
## 1. tools/capture_regression_t_655239f0_combat_lobby.gd (戰鬥超載爆裂、結算機芯入包、大廳紅點)
## 2. tools/capture_regression_t_655239f0_dummy_btn.gd (武術館前往木人樁試招按鈕)
func _initialize() -> void:
	print("請執行 tools/capture_regression_t_655239f0_combat_lobby.gd 與 tools/capture_regression_t_655239f0_dummy_btn.gd")
	quit(0)
