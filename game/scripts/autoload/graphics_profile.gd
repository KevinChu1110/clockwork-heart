extends Node
## Low / Mid / High 繪圖 profile（Product Lock §5.1 第 5 項）
## 存 user://graphics_profile.json。choice=auto 時桌面／Web 落 High，不砍開發機。

const PATH := "user://graphics_profile.json"
const TIERS: PackedStringArray = ["low", "mid", "high"]
const CHOICES: PackedStringArray = ["auto", "high", "mid", "low"]
const BASE_W := 1280
const BASE_H := 720

## auto | low | mid | high
var choice: String = "auto"
## 上次 apply 實際落到的檔
var applied: String = "high"
var applied_scale: float = 1.0
var applied_content_size: Vector2i = Vector2i(BASE_W, BASE_H)

signal changed(tier: String)


func _ready() -> void:
	load_settings()
	call_deferred("apply")


func load_settings() -> void:
	if not FileAccess.file_exists(PATH):
		choice = "auto"
		save_settings()
		return
	var f := FileAccess.open(PATH, FileAccess.READ)
	if f == null:
		return
	var data = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		return
	choice = str(data.get("choice", "auto"))
	if choice != "auto" and choice not in TIERS:
		choice = "auto"


func save_settings() -> void:
	var f := FileAccess.open(PATH, FileAccess.WRITE)
	if f == null:
		push_warning("GraphicsProfile: cannot write %s" % PATH)
		return
	f.store_string(JSON.stringify({"choice": choice}, "\t"))


func detect_device_tier() -> String:
	## 桌面／Web 維持高檔，避免把開發機畫面砍成低階。
	var os := OS.get_name()
	if os in ["Windows", "Linux", "macOS", "FreeBSD", "Web"]:
		return "high"
	var cores := OS.get_processor_count()
	var scr := DisplayServer.screen_get_size()
	var short_side := mini(scr.x, scr.y)
	if cores <= 4 or (short_side > 0 and short_side < 720):
		return "low"
	return "mid"


func effective_tier() -> String:
	if choice in TIERS:
		return choice
	return detect_device_tier()


func spec(tier: String = "") -> Dictionary:
	var t := tier if tier != "" else effective_tier()
	match t:
		"low":
			return {
				"id": "low",
				"shadows": false,
				"particles": false,
				"vfx": false,
				"particle_count_scale": 0.0,
				"render_scale": 0.5,
				"content_w": 640,
				"content_h": 360,
			}
		"mid":
			return {
				"id": "mid",
				"shadows": true,
				"particles": true,
				"vfx": true,
				"particle_count_scale": 0.5,
				"render_scale": 0.75,
				"content_w": 960,
				"content_h": 540,
			}
		_:
			return {
				"id": "high",
				"shadows": true,
				"particles": true,
				"vfx": true,
				"particle_count_scale": 1.0,
				"render_scale": 1.0,
				"content_w": BASE_W,
				"content_h": BASE_H,
			}


func cost_score(tier: String = "") -> int:
	var s := spec(tier)
	var n := 0
	if bool(s.get("shadows", false)):
		n += 2
	if bool(s.get("particles", false)):
		n += 2
	if bool(s.get("vfx", false)):
		n += 2
	n += int(round(float(s.get("render_scale", 1.0)) * 4.0))
	return n


func shadows_enabled() -> bool:
	return bool(spec().get("shadows", true))


func particles_enabled() -> bool:
	return bool(spec().get("particles", true))


func vfx_enabled() -> bool:
	return bool(spec().get("vfx", true))


func particle_count(base: int) -> int:
	var scale := float(spec().get("particle_count_scale", 1.0))
	if scale <= 0.0:
		return 0
	return maxi(1, int(round(float(base) * scale)))


func apply() -> void:
	applied = effective_tier()
	var s := spec(applied)
	applied_scale = float(s.get("render_scale", 1.0))
	applied_content_size = Vector2i(int(s.get("content_w", BASE_W)), int(s.get("content_h", BASE_H)))
	var win := get_window()
	if win != null:
		if applied == "high":
			## (0,0) = 用 project.godot 的 1280×720，不改開發機現況
			win.content_scale_size = Vector2i(0, 0)
		else:
			win.content_scale_size = applied_content_size
	changed.emit(applied)
	print("GraphicsProfile apply choice=%s applied=%s scale=%s size=%s shadows=%s particles=%s vfx=%s method=%s" % [
		choice, applied, applied_scale, applied_content_size, s.get("shadows"), s.get("particles"), s.get("vfx"),
		RenderingServer.get_current_rendering_method(),
	])


func set_choice(c: String) -> void:
	if c != "auto" and c not in TIERS:
		return
	choice = c
	save_settings()
	apply()


func cycle_choice() -> void:
	var idx := 0
	for i in CHOICES.size():
		if CHOICES[i] == choice:
			idx = i
			break
	idx = (idx + 1) % CHOICES.size()
	set_choice(CHOICES[idx])


func _t(key: String, vars: Dictionary = {}) -> String:
	var t := Engine.get_main_loop()
	if t is SceneTree and (t as SceneTree).root != null:
		var loc: Node = (t as SceneTree).root.get_node_or_null("Loc")
		if loc != null and loc.has_method("t"):
			return str(loc.call("t", key, vars))
	return key


func choice_label() -> String:
	match choice:
		"low":
			return _t("display.quality_low")
		"mid":
			return _t("display.quality_mid")
		"high":
			return _t("display.quality_high")
		_:
			return _t("display.quality_auto")


func applied_label() -> String:
	match applied:
		"low":
			return _t("display.quality_low")
		"mid":
			return _t("display.quality_mid")
		_:
			return _t("display.quality_high")


func summary_line() -> String:
	if choice == "auto":
		return _t("display.quality_summary_auto", {"tier": applied_label()})
	return _t("display.quality_summary", {"tier": choice_label()})
