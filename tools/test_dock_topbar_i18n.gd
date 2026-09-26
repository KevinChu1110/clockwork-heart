extends SceneTree

const LOCALES := ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

func _initialize() -> void:
	print("── 開始驗證大廳頂欄三寶與底部 Dock 六語系 ──")
	var loc_node: Node = root.get_node_or_null("Loc")
	if loc_node == null:
		push_error("Loc not found")
		quit(1)
		return

	var LobbyClass: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	if LobbyClass == null:
		push_error("LobbyClass not found")
		quit(1)
		return

	var lobby: Control = LobbyClass.new()
	root.add_child(lobby)
	lobby._ready()

	for code in LOCALES:
		loc_node.call("set_locale", code)
		var nrg: Label = lobby.get("_energy_title_label")
		var gold: Label = lobby.get("_gold_title_label")
		var gem: Label = lobby.get("_gem_title_label")
		var dock_btns: Array = lobby.get("_dock_buttons")

		var dock_texts: Array = []
		for b in dock_btns:
			dock_texts.append((b as Button).text)

		print("[%s] 能量=%s, 金幣=%s, 星屑=%s" % [
			code,
			nrg.text if nrg else "null",
			gold.text if gold else "null",
			gem.text if gem else "null"
		])
		print("  Dock: %s" % [" | ".join(dock_texts)])

	lobby.queue_free()
	print("── 驗證結束 ──")
	quit(0)
