extends Control
## Art Pivot v2 紙娃娃視圖：以組裝器相位 composite 顯示，胸口錨點給 WindStaminaGlow。
## 模組邊界：只負責顯示與錨點；不驅動流程／體力邏輯。
## 舊電影 3D／s8_smoke placeholder 皮由此退役（改走 pack_a/v2）。

const AssemblerScript := preload("res://scripts/systems/paper_doll_v2/paper_doll_assembler.gd")

var assembler
var _art: TextureRect
var chest_anchor: Control
var _slot_debug: Label


func setup(asm = null) -> void:
	assembler = asm if asm != null else AssemblerScript.new()
	if assembler.config == null or assembler.config.raw.is_empty():
		assembler.setup()
	_ensure_nodes()
	refresh()


func _ensure_nodes() -> void:
	if _art == null:
		_art = TextureRect.new()
		_art.name = "PaperDollArt"
		_art.set_anchors_preset(Control.PRESET_FULL_RECT)
		_art.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		_art.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		_art.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(_art)
	if chest_anchor == null:
		chest_anchor = Control.new()
		chest_anchor.name = "ChestHeartAnchor"
		chest_anchor.size = Vector2(96, 96)
		chest_anchor.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(chest_anchor)
	if _slot_debug == null:
		_slot_debug = Label.new()
		_slot_debug.name = "SlotDebug"
		_slot_debug.position = Vector2(8, 8)
		_slot_debug.add_theme_font_size_override("font_size", 12)
		_slot_debug.add_theme_color_override("font_color", Color(0.75, 0.85, 0.7, 0.7))
		_slot_debug.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(_slot_debug)


func set_phase(phase: String) -> void:
	if assembler == null:
		return
	assembler.set_phase(phase)
	refresh()


func refresh() -> void:
	if assembler == null or _art == null:
		return
	var path := assembler.composite_path_for_phase()
	if ResourceLoader.exists(path):
		_art.texture = load(path) as Texture2D
	else:
		push_warning("PaperDollView: missing composite %s" % path)
	_layout_chest_anchor()
	var s: Dictionary = assembler.summary()
	_slot_debug.text = "v2 · %s · %s · off=%s · key=%s" % [
		str(s.get("phase", "")),
		str(s.get("weaponClass", "")),
		str(s.get("weapon_off", "")),
		str(s.get("back_key", "")),
	]


func _layout_chest_anchor() -> void:
	## 胸口心相對視圖中心偏下（給 ChestGlowHud 掛載）
	if chest_anchor == null:
		return
	var sz := size
	if sz.x < 8.0 or sz.y < 8.0:
		sz = Vector2(640, 720)
	match assembler.current_phase if assembler else "explore":
		"battle":
			chest_anchor.position = Vector2(sz.x * 0.42, sz.y * 0.48)
		"dismantle":
			chest_anchor.position = Vector2(sz.x * 0.40, sz.y * 0.50)
		_:
			chest_anchor.position = Vector2(sz.x * 0.46, sz.y * 0.52)
