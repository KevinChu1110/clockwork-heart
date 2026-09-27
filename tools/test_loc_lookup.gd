extends SceneTree

func _initialize():
	var loc_cls = load("res://scripts/autoload/loc.gd")
	var loc = loc_cls.new()
	loc.name = "Loc"
	root.add_child(loc)
	loc.call("set_locale", "en")
	var ContentLoc = load("res://scripts/systems/content_loc.gd")
	print("loc.locale = ", loc.get("locale"))
	print("ContentLoc.locale() = ", ContentLoc.locale())
	print("file exists = ", FileAccess.file_exists("res://data/i18n/content/en/ui.json"))
	var tbl = ContentLoc._table("ui", "en")
	print("tbl size = ", tbl.size())
	print("tbl['上品'] = ", tbl.get("上品", "NOT_FOUND"))
	print("ContentLoc.text('ui', '上品') = '", ContentLoc.text("ui", "上品"), "'")
	quit(0)
