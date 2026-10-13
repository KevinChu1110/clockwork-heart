extends SceneTree
## QA：es 「50% de」是否真的會在執行時炸
const ContentLoc = preload("res://scripts/systems/content_loc.gd")
const KEYS := [
	"二次機會：觀看贊助廣告即可重新上鍊，立即以 50% 生命值重返戰場！",
	"二次機會：已移除廣告，可直接重新上鍊，立即以 50% 生命值重返戰場！",
]
var _done := false
func _initialize() -> void:
	_run.call_deferred()

func _run() -> void:
	root.get_node("Loc").call("set_locale", "es")
	print("locale = ", TranslationServer.get_locale())
	for k in KEYS:
		var es: String = ContentLoc.text("ui", k)
		var lbl := Label.new(); lbl.text = es; root.add_child(lbl)
		print("zh_TW: ", k)
		print("es   : ", es, "  (translated=", es != k, ")")
	# 實際遊戲路徑：battle_defeat_dialog 直接 _hint_lbl.text = _t(...)，沒有 % 格式化
	var dlg_src := FileAccess.get_file_as_string("res://scripts/battle/battle_defeat_dialog.gd")
	for line in dlg_src.split("\n"):
		if line.contains("50% 生命值"): print("usage: ", line.strip_edges())
	# 情境：硬套 % 格式化時才會出事（遊戲裡沒有這樣用）
	var es0: String = ContentLoc.text("ui", KEYS[0])
	print("count('% d') in es = ", es0.count("% d"))
	# 實際建出敗北視窗走一次 es（若可實例化）
	var D = load("res://scripts/battle/battle_defeat_dialog.gd")
	if D and D.can_instantiate():
		var d = D.new()
		root.add_child(d)
		await process_frame
		for c in d.find_children("*", "Label", true, false):
			if (c as Label).text.contains("50%"): print("dialog label (es): ", (c as Label).text)
	print("QA_ES_PROBE_DONE")
	quit(0)
