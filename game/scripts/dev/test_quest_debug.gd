extends SceneTree

var frame := 0

func _process(_delta: float) -> bool:
	frame += 1
	if frame < 2:
		return false
	var loc_node = root.get_node_or_null("Loc")
	var qs = root.get_node_or_null("QuestSystem")
	print("Loc node: ", loc_node)
	print("QuestSystem: ", qs)
	if loc_node and qs:
		print("Current locale: ", loc_node.locale)
		print("Commissions count: ", qs.commissions().size())
		for c in qs.commissions():
			print("  c: ", c.get("id"), " name: ", c.get("name"), " desc: ", c.get("desc"))
		print("List missions bbcode (zh_TW):")
		print(qs.list_missions_bbcode().substr(0, 200))
		
		loc_node.set_locale("en")
		print("\nAfter switch to en:")
		print("Current locale: ", loc_node.locale)
		for c in qs.commissions():
			print("  c: ", c.get("id"), " name: ", c.get("name"), " desc: ", c.get("desc"))
		print("List missions bbcode (en):")
		print(qs.list_missions_bbcode().substr(0, 200))
	quit(0)
	return true
