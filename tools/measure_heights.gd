extends SceneTree

const ContentLoc = preload("res://scripts/systems/content_loc.gd")

func _process(_delta: float) -> bool:
	var qs = root.get_node_or_null("QuestSystem")
	var loc = root.get_node_or_null("Loc")
	if qs and loc:
		for lc in ["en", "ja", "zh_TW"]:
			loc.call("set_locale", lc)
			var b := RichTextLabel.new()
			b.bbcode_enabled = true
			b.fit_content = true
			b.custom_minimum_size = Vector2(680, 0)
			root.add_child(b)
			var full_text: String = str(qs.call("list_missions_bbcode"))
			var lines := full_text.split("\n")
			# header in _go_quest_panel is: _t("長遠任務（完成後可領獎）\n\n")
			var header: String = ContentLoc.text("ui", "長遠任務（完成後可領獎）\n\n")
			var t1: String = header + lines[0] + "\n" + lines[1] + "\n" + lines[2]
			b.text = t1
			print("[%s] 1 task height: %f" % [lc, b.get_content_height()])
			var t2: String = t1 + "\n" + lines[3] + "\n" + lines[4] + "\n" + lines[5]
			b.text = t2
			print("[%s] 2 tasks height: %f" % [lc, b.get_content_height()])
			var t3: String = t2 + "\n" + lines[6] + "\n" + lines[7] + "\n" + lines[8]
			b.text = t3
			print("[%s] 3 tasks height: %f" % [lc, b.get_content_height()])
			b.queue_free()
		quit(0)
		return true
	return false
