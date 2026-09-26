extends AcceptDialog

## 章節包尚未下載提示彈窗（六語系支援）
## 支援在彈窗開啟時動態切換語系 (Loc.locale_changed)

const ContentLoc := preload("res://scripts/systems/content_loc.gd")
const BundlePacksScn := preload("res://scripts/systems/bundle_packs.gd")

var _map_id: String = ""

static func _t(s: String) -> String:
	return ContentLoc.text("ui", s)

func _init(p_map_id: String = "") -> void:
	_map_id = p_map_id
	unresizable = true

func setup(p_map_id: String) -> void:
	_map_id = p_map_id
	_update_texts()

func _ready() -> void:
	unresizable = true
	confirmed.connect(queue_free)
	close_requested.connect(queue_free)
	_connect_loc_signal()
	_update_texts()

func _exit_tree() -> void:
	_disconnect_loc_signal()

func _connect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed"):
			if not loc.locale_changed.is_connected(_on_locale_changed):
				loc.locale_changed.connect(_on_locale_changed)

func _disconnect_loc_signal() -> void:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		var loc: Node = (loop as SceneTree).root.get_node_or_null("Loc")
		if loc and loc.has_signal("locale_changed") and loc.locale_changed.is_connected(_on_locale_changed):
			loc.locale_changed.disconnect(_on_locale_changed)

func _on_locale_changed(_new_locale: String = "") -> void:
	_update_texts()

func _update_texts() -> void:
	title = _t("尚未下載")
	if _map_id != "":
		dialog_text = BundlePacksScn.missing_pack_line(_map_id)
	else:
		dialog_text = _t("後續章節尚未下載（需要 %s 包）") % "chapter"
	ok_button_text = _t("確定")
