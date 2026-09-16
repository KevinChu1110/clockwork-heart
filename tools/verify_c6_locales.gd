extends SceneTree

func _initialize() -> void:
	print("=== 開始六語系 C6 雙結局對白 DialogLines 實機載入驗證 ===")
	var locales := ["zh_TW", "zh_CN", "en", "es", "ja", "ko"]
	var endings := ["c6.demon_win", "c6.demon_win_refuse_all"]
	var failed := false
	
	# 建立或取得 Loc autoload 模擬節點
	var loc_node = root.get_node_or_null("Loc")
	if loc_node == null:
		loc_node = Node.new()
		loc_node.name = "Loc"
		loc_node.set_meta("locale", "zh_TW")
		root.add_child(loc_node)
	
	for loc in locales:
		print("\n--- 檢查語系: %s ---" % loc)
		# 更新 Loc.locale 屬性
		loc_node.set("locale", loc)
		# 通知 DialogLines 重新載入
		DialogLines.reload()
		
		for ending_key in endings:
			var lines := DialogLines.lines(ending_key)
			if lines.is_empty():
				printerr("❌ 錯誤: %s 在語系 %s 為空！" % [ending_key, loc])
				failed = true
				continue
			print("  結局 [%s] (%d 句):" % [ending_key, lines.size()])
			for i in range(lines.size()):
				var item: Dictionary = lines[i]
				var spk: String = str(item.get("speaker", ""))
				var txt: String = str(item.get("text", ""))
				if "[待補]" in txt or "待補" in txt or "TODO" in txt:
					printerr("    ❌ 發現未翻譯/待補: %s 第 %d 句 [%s] %s" % [ending_key, i+1, spk, txt])
					failed = true
				elif "" in txt:
					printerr("    ❌ 發現亂碼: %s 第 %d 句 [%s] %s" % [ending_key, i+1, spk, txt])
					failed = true
				else:
					print("    ✓ 第 %d 句 [%s] %s" % [i+1, spk, txt])
	
	if failed:
		printerr("\n=== C6 雙結局六語系驗證失敗 ===")
		quit(1)
	else:
		print("\n=== [ALL PASS] C6 雙結局六語系 DialogLines 載入驗證全數合格，無 [待補]、無亂碼！ ===")
		quit(0)
