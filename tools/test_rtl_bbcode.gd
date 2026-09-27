extends SceneTree

func _init() -> void:
	var rtl1 := RichTextLabel.new()
	rtl1.bbcode_enabled = true
	rtl1.append_text("[b][The King's Cut] Rampant Clockwork Lion deals 37 damage [/b]")
	print("Test 1 raw: [", rtl1.get_parsed_text(), "]")

	var rtl2 := RichTextLabel.new()
	rtl2.bbcode_enabled = true
	rtl2.append_text("[b]【The King's Cut】 Rampant Clockwork Lion deals 37 damage [/b]")
	print("Test 2 fullwidth: [", rtl2.get_parsed_text(), "]")

	var rtl3 := RichTextLabel.new()
	rtl3.bbcode_enabled = true
	rtl3.append_text("[b][lb]The King's Cut[rb] Rampant Clockwork Lion deals 37 damage [/b]")
	print("Test 3 lb rb: [", rtl3.get_parsed_text(), "]")

	var rtl4 := RichTextLabel.new()
	rtl4.bbcode_enabled = true
	rtl4.append_text("[b][King's Cut] Rampant Clockwork Lion deals 37 damage [/b]")
	print("Test 4 no space: [", rtl4.get_parsed_text(), "]")
	quit()
