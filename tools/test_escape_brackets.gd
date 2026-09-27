extends SceneTree

func _escape_custom_brackets(s: String) -> String:
	# 保留合法的 bbcode 標籤 [b], [/b], [color=...], [/color], [lb], [rb]
	# 將其他 [ 換成 [lb], ] 換成 [rb]
	var regex := RegEx.new()
	# 匹配不是合法 bbcode 的 [ 開頭
	# 或簡單地：[The King's Cut] -> [lb]The King's Cut[rb]
	var res := s.replace("[The King's Cut]", "[lb]The King's Cut[rb]")
	res = res.replace("[Corte del Rey]", "[lb]Corte del Rey[rb]")
	return res

func _init() -> void:
	var rtl := RichTextLabel.new()
	rtl.bbcode_enabled = true
	var raw := "[The King's Cut] Rampant Clockwork Lion deals 37 damage"
	var processed := _escape_custom_brackets(raw)
	var final_line := "[b]%s[/b]" % processed
	rtl.append_text(final_line)
	print("Input: ", raw)
	print("Processed: ", processed)
	print("Parsed: [", rtl.get_parsed_text(), "]")
	quit()
