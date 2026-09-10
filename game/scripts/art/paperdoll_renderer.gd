class_name PaperdollRenderer
extends RefCounted
## 《發條之心》紙娃娃圖層合成程式骨架
## 依據 docs/design/paperdoll_slots.json / PAPERDOLL_SLOTS_SPEC.md 規格：
## 讀取 7 大機械部件槽位定義與 z_index 渲染層級，
## 依「動物種族 + 各槽位選擇」組出 {slot: texture_path} 對照表與安全貼圖載入。

const SPEC_JSON_PATH := "res://data/tables/paperdoll_slots.json"
const ROOT_SPRITES := "res://assets/sprites/player"
const PAPERDOLL_ROOT := "res://assets/sprites/player/paperdoll"

## 規格書定義之 7 大槽位 ID 常數
const SLOT_CHASSIS := "chassis"          ## 軀體外殼與塗裝 (Z: 10, required)
const SLOT_HEAD_UNIT := "head_unit"      ## 頭部機關與耳朵造型 (Z: 20, required)
const SLOT_WINDING_KEY := "winding_key"  ## 背部發條鑰匙 (Z: 5, required)
const SLOT_COSTUME := "costume"          ## 玩具外裝與服飾 (Z: 25, optional)
const SLOT_OPTIC_CORE := "optic_core"    ## 面部光學與表情核心 (Z: 30, required)
const SLOT_WEAPON := "weapon"            ## 手持武器外觀 (Z: 40, required)
const SLOT_BACK_CURIO := "back_curio"    ## 隨身奇玩與尾部機關 (Z: 8, optional)

## 規格快取
static var _spec_cache: Dictionary = {}
static var _slots_sorted_cache: Array[Dictionary] = []


## ── 規格讀取與解析 ──

## 讀取 res://data/tables/paperdoll_slots.json，若已快取則直接回傳
static func get_spec(force_reload: bool = false) -> Dictionary:
	if not _spec_cache.is_empty() and not force_reload:
		return _spec_cache

	if FileAccess.file_exists(SPEC_JSON_PATH):
		var file := FileAccess.open(SPEC_JSON_PATH, FileAccess.READ)
		if file != null:
			var text := file.get_as_text()
			var parsed: Variant = JSON.parse_string(text)
			if parsed is Dictionary and parsed.has("slots_architecture"):
				_spec_cache = parsed as Dictionary
				_init_cache()
				return _spec_cache

	push_warning("[PaperdollRenderer] 無法讀取紙娃娃規格檔 %s，使用內部安全備份規格" % SPEC_JSON_PATH)
	_spec_cache = _get_fallback_spec()
	_init_cache()
	return _spec_cache


static func _init_cache() -> void:
	_slots_sorted_cache.clear()
	var slots: Array = get_slots_raw()
	var typed_slots: Array[Dictionary] = []
	for s in slots:
		if s is Dictionary:
			typed_slots.append(s as Dictionary)

	# 依 layer_z_index 由小到大排序 (ASCENDING)
	typed_slots.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		var za: int = int(a.get("layer_z_index", 0))
		var zb: int = int(b.get("layer_z_index", 0))
		return za < zb
	)
	_slots_sorted_cache = typed_slots


static func get_slots_raw() -> Array:
	var spec := get_spec()
	var arch: Dictionary = spec.get("slots_architecture", {})
	return arch.get("slots", [])


## 取得依 z_index 由小到大排序的所有槽位定義
static func get_slots_sorted_by_z() -> Array[Dictionary]:
	if _slots_sorted_cache.is_empty():
		get_spec()
	return _slots_sorted_cache


## 取得依 z_index 由小到大排序的所有槽位 ID
static func get_slot_ids_sorted_by_z() -> Array[String]:
	var sorted_slots := get_slots_sorted_by_z()
	var ids: Array[String] = []
	for slot in sorted_slots:
		ids.append(str(slot.get("slot_id", "")))
	return ids


## 取得特定槽位規格定義
static func get_slot_def(slot_id: String) -> Dictionary:
	for slot in get_slots_sorted_by_z():
		if str(slot.get("slot_id", "")) == slot_id:
			return slot
	return {}


## 取得特定槽位之 z_index
static func get_slot_z_index(slot_id: String) -> int:
	var def := get_slot_def(slot_id)
	return int(def.get("layer_z_index", 0))


## 取得特定槽位是否為必選
static func is_slot_required(slot_id: String) -> bool:
	var def := get_slot_def(slot_id)
	return bool(def.get("required", false))


## ── 圖層路徑組裝與解析 ──

## 依種族、槽位、選項計算對應貼圖路徑
## 先支援兔 (rabbit) 與猴 (macaque)：
## - 兔：優先專屬紙娃娃切片，若尚未切圖則退回現有 player/ 資源，確保 7 槽皆能對應真實檔案
## - 猴：產出規範預定路徑，目前尚未切圖，載入時安全回傳 null
static func resolve_slot_texture_path(race: String, slot_id: String, item_id: String = "") -> String:
	var rid := race.to_lower().strip_edges()
	var sid := slot_id.to_lower().strip_edges()
	var iid := item_id.strip_edges()

	# 0. 若明確指定無裝備 / 卸除，回傳空字串以安全隱藏該層
	if iid in ["none", "empty", "bare"]:
		return ""

	# 1. 若已有專屬紙娃娃切片圖檔存在，優先採用
	var effective_id := iid if iid != "" else _get_default_variant_id(rid, sid)
	if effective_id != "":
		var custom_slice := "%s/%s/%s/%s.png" % [PAPERDOLL_ROOT, rid, sid, effective_id]
		if ResourceLoader.exists(custom_slice) or FileAccess.file_exists(custom_slice):
			return custom_slice
		# 檢查去前綴後之切片命名相容性
		var clean_id := effective_id
		for pfx in ["wpn_", "costume_", "key_", "curio_", "paint_", "ear_", "core_"]:
			if clean_id.begins_with(pfx):
				clean_id = clean_id.trim_prefix(pfx)
				break
		var custom_slice_clean := "%s/%s/%s/%s.png" % [PAPERDOLL_ROOT, rid, sid, clean_id]
		if ResourceLoader.exists(custom_slice_clean) or FileAccess.file_exists(custom_slice_clean):
			return custom_slice_clean
		# 若指定的 item_id 在該族不存在（例如切換種族時殘留他族武器），退回該族預設部件
		var def_id := _get_default_variant_id(rid, sid)
		if def_id != "" and def_id != effective_id:
			var def_slice := "%s/%s/%s/%s.png" % [PAPERDOLL_ROOT, rid, sid, def_id]
			if ResourceLoader.exists(def_slice) or FileAccess.file_exists(def_slice):
				return def_slice

	# 2. 通用裝備紙娃娃目錄 (weapon, armor, accessory, key, curio)
	if sid in [SLOT_WEAPON, SLOT_COSTUME, SLOT_BACK_CURIO, SLOT_WINDING_KEY]:
		var uni_path := _resolve_universal_equipment_path(sid, iid)
		if uni_path != "" and ResourceLoader.exists(uni_path):
			return uni_path

	# 3. 兔族系 (rabbit) 現有資產對應
	if rid == "rabbit":
		return _resolve_rabbit_existing_asset(sid, iid)

	# 4. 其他族系（如 macaque 靈爪猴）暫定路徑佔位
	# 依照 docs/design/paperdoll_slots.json 的命名規範產生標準預定路徑
	var item_slug := iid if iid != "" else _get_default_variant_id(rid, sid)
	return "%s/%s/%s/%s.png" % [PAPERDOLL_ROOT, rid, sid, item_slug]


## 解決通用裝備切片路徑
static func _resolve_universal_equipment_path(slot_id: String, item_id: String) -> String:
	if item_id == "":
		return ""
	var clean_id := item_id
	if clean_id.begins_with("wpn_"):
		clean_id = clean_id.trim_prefix("wpn_")
	elif clean_id.begins_with("costume_"):
		clean_id = clean_id.trim_prefix("costume_")
	elif clean_id.begins_with("key_"):
		clean_id = clean_id.trim_prefix("key_")
	elif clean_id.begins_with("curio_"):
		clean_id = clean_id.trim_prefix("curio_")

	match slot_id:
		SLOT_WEAPON:
			var p1 := "%s/weapon/%s.png" % [PAPERDOLL_ROOT, clean_id]
			if ResourceLoader.exists(p1): return p1
			var p2 := "%s/weapons/%s.png" % [ROOT_SPRITES, clean_id]
			if ResourceLoader.exists(p2): return p2
		SLOT_COSTUME:
			var p1 := "%s/armor/%s.png" % [PAPERDOLL_ROOT, clean_id]
			if ResourceLoader.exists(p1): return p1
			var p2 := "%s/armor/%s.png" % [ROOT_SPRITES, clean_id]
			if ResourceLoader.exists(p2): return p2
		SLOT_BACK_CURIO:
			var p1 := "%s/accessory/%s.png" % [PAPERDOLL_ROOT, clean_id]
			if ResourceLoader.exists(p1): return p1
			var p2 := "%s/accessories/%s.png" % [ROOT_SPRITES, clean_id]
			if ResourceLoader.exists(p2): return p2
		SLOT_WINDING_KEY:
			var p1 := "%s/key/%s.png" % [PAPERDOLL_ROOT, clean_id]
			if ResourceLoader.exists(p1): return p1
	return ""


## 兔族系現有真實檔案對照表（確保 7 槽皆能映射至真實既有檔案，非空字串）
static func _resolve_rabbit_existing_asset(slot_id: String, item_id: String) -> String:
	match slot_id:
		SLOT_CHASSIS:
			# 素體外殼：高畫質待機素體
			return "%s/rabbit_idle_x3.png" % ROOT_SPRITES
		SLOT_HEAD_UNIT:
			# 頭部機關與耳朵造型：既有待機姿態頭部基礎
			return "%s/poses/idle.png" % ROOT_SPRITES
		SLOT_WINDING_KEY:
			# 背部發條鑰匙：既有背部發條符號配件
			return "%s/accessories/ring.png" % ROOT_SPRITES
		SLOT_COSTUME:
			# 玩具外裝與服飾：胡桃鉗/騎士重裝甲
			if item_id != "" and ResourceLoader.exists("%s/paperdoll/armor/%s.png" % [ROOT_SPRITES, item_id]):
				return "%s/paperdoll/armor/%s.png" % [ROOT_SPRITES, item_id]
			return "%s/armor/plate.png" % ROOT_SPRITES
		SLOT_OPTIC_CORE:
			# 面部光學與表情核心：戰鬥光學特寫
			return "%s/rabbit_battle.png" % ROOT_SPRITES
		SLOT_WEAPON:
			# 手持武器：晨曦發條單手長劍 / 經典單手劍
			if item_id != "" and ResourceLoader.exists("%s/paperdoll/weapon/%s.png" % [ROOT_SPRITES, item_id]):
				return "%s/paperdoll/weapon/%s.png" % [ROOT_SPRITES, item_id]
			return "%s/weapons/sword.png" % ROOT_SPRITES
		SLOT_BACK_CURIO:
			# 隨身奇玩與尾部機關：星紋吊墜/發條配件
			if item_id != "" and ResourceLoader.exists("%s/paperdoll/accessory/%s.png" % [ROOT_SPRITES, item_id]):
				return "%s/paperdoll/accessory/%s.png" % [ROOT_SPRITES, item_id]
			return "%s/accessories/pendant.png" % ROOT_SPRITES
		_:
			return "%s/rabbit_idle.png" % ROOT_SPRITES


static func _get_default_variant_id(race: String, slot_id: String) -> String:
	match slot_id:
		SLOT_CHASSIS:
			if race == "fox":
				return "paint_fox_orange"
			elif race == "lion":
				return "paint_brass_gold"
			elif race == "boar":
				return "paint_ivory_stock"
			elif race == "macaque":
				return "paint_ivory_stock"
			return "paint_ivory_stock"
		SLOT_HEAD_UNIT:
			if race == "macaque":
				return "ear_macaque_coaxial"
			elif race == "fox":
				return "ear_fox_radar"
			elif race == "lion":
				return "ear_lion_gilded_mane"
			elif race == "boar":
				return "ear_boar_rivet_cowl"
			return "ear_rabbit_straight"
		SLOT_WINDING_KEY:
			return "key_classic_brass"
		SLOT_COSTUME:
			if race == "macaque":
				return "costume_dawn_monk_tunic"
			elif race == "fox":
				return "costume_astral_cape"
			elif race == "lion":
				return "costume_nutcracker_guard"
			elif race == "boar":
				return "costume_viking_harness"
			return "costume_nutcracker_guard"
		SLOT_OPTIC_CORE:
			if race == "lion":
				return "core_amber_sun"
			return "core_cyan_emerald"
		SLOT_WEAPON:
			if race == "macaque":
				return "wpn_spring_claws"
			elif race == "fox":
				return "wpn_astral_staff"
			elif race == "lion":
				return "wpn_knight_lance"
			elif race == "boar":
				return "wpn_anvil_greathammer"
			return "wpn_dawn_blade"
		SLOT_BACK_CURIO:
			if race == "macaque":
				return "curio_spring_tail"
			elif race == "fox":
				return "curio_fox_astral_tail"
			elif race == "lion":
				return "curio_lion_fan_tail"
			elif race == "boar":
				return "curio_spring_tail"
			return "curio_clockwork_pigeon"
		_:
			return "default"


## 組出依 z_index 由小到大排列的 {slot_id: texture_path} 對照表
static func build_paperdoll_map(race: String, slot_selection: Dictionary = {}) -> Dictionary:
	var result: Dictionary = {}
	var sorted_slots := get_slots_sorted_by_z()

	for slot_def in sorted_slots:
		var sid: String = str(slot_def.get("slot_id", ""))
		var chosen_item: String = str(slot_selection.get(sid, ""))
		var path := resolve_slot_texture_path(race, sid, chosen_item)
		result[sid] = path

	return result


## 安全取得貼圖資源（缺圖時回傳 null，絕不拋出例外）
static func get_slot_texture(path: String) -> Texture2D:
	if path == "" or (not ResourceLoader.exists(path) and not FileAccess.file_exists(path)):
		return null
	if ResourceLoader.exists(path):
		var res = load(path)
		if res is Texture2D:
			return res as Texture2D
	# 若尚未產生 .import 快取，使用 Image.load_from_file 安全即時載入
	if FileAccess.file_exists(path):
		var img := Image.load_from_file(path)
		if img != null and not img.is_empty():
			return ImageTexture.create_from_image(img)
	return null


## 組出 {slot_id: Texture2D or null} 對照表
static func build_paperdoll_textures(race: String, slot_selection: Dictionary = {}) -> Dictionary:
	var path_map := build_paperdoll_map(race, slot_selection)
	var textures: Dictionary = {}
	for sid in path_map.keys():
		textures[sid] = get_slot_texture(str(path_map[sid]))
	return textures


## 取得完整有序槽位結構資料，便於渲染層或除錯驗證
static func get_sorted_slot_entries(race: String, slot_selection: Dictionary = {}) -> Array[Dictionary]:
	var entries: Array[Dictionary] = []
	var sorted_slots := get_slots_sorted_by_z()

	for slot_def in sorted_slots:
		var sid: String = str(slot_def.get("slot_id", ""))
		var chosen_item: String = str(slot_selection.get(sid, ""))
		var path := resolve_slot_texture_path(race, sid, chosen_item)
		var texture: Texture2D = get_slot_texture(path)

		entries.append({
			"slot_id": sid,
			"name_zh": str(slot_def.get("name_zh", "")),
			"name_en": str(slot_def.get("name_en", "")),
			"layer_z_index": int(slot_def.get("layer_z_index", 0)),
			"required": bool(slot_def.get("required", false)),
			"chosen_item": chosen_item,
			"texture_path": path,
			"texture": texture,
			"is_loaded": texture != null
		})

	return entries


## ── 記憶體即時合成 128x128 RGBA8 貼圖（依 z_index 順序疊合 7 大槽位）──
static func build_composite_image(race: String, slot_selection: Dictionary = {}) -> Image:
	var entries := get_sorted_slot_entries(race, slot_selection)
	var base_img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	base_img.fill(Color(0, 0, 0, 0))
	for entry in entries:
		var tex: Texture2D = entry.get("texture", null)
		if tex == null:
			continue
		var layer_img: Image = tex.get_image()
		if layer_img == null or layer_img.is_empty():
			continue
		if layer_img.get_format() != Image.FORMAT_RGBA8:
			layer_img.convert(Image.FORMAT_RGBA8)
		var src_rect := Rect2i(0, 0, layer_img.get_width(), layer_img.get_height())
		base_img.blend_rect(layer_img, src_rect, Vector2i.ZERO)
	return base_img


static func build_composite_texture(race: String, slot_selection: Dictionary = {}) -> Texture2D:
	var img := build_composite_image(race, slot_selection)
	if img != null and not img.is_empty():
		return ImageTexture.create_from_image(img)
	return null


static func get_race_composite_texture(race: String, slot_selection: Dictionary = {}) -> Texture2D:
	var rid := race.to_lower().strip_edges()
	if slot_selection.is_empty():
		var proof_path := "%s/%s/proof_paperdoll_%s_composite.png" % [PAPERDOLL_ROOT, rid, rid]
		if ResourceLoader.exists(proof_path):
			var res = load(proof_path)
			if res is Texture2D:
				return res as Texture2D
	return build_composite_texture(rid, slot_selection)


## ── 執行期走路姿態動態合成 (PaperdollRenderer Walk Kinematics) ──

const RABBIT_WALK_GAIT: Array[Dictionary] = [
	{
		"name": "Frame 0",
		"torso_dy": 0,
		"leg_l_rot": 12.5, "leg_l_dx": -2, "leg_l_dy": 0,
		"leg_r_rot": -12.5, "leg_r_dx": 2, "leg_r_dy": 0,
	},
	{
		"name": "Frame 1",
		"torso_dy": -1,
		"leg_l_rot": 13.0, "leg_l_dx": 0, "leg_l_dy": 1,
		"leg_r_rot": 22.0, "leg_r_dx": -5, "leg_r_dy": -4,
	},
	{
		"name": "Frame 2",
		"torso_dy": 0,
		"leg_l_rot": -12.5, "leg_l_dx": 2, "leg_l_dy": 0,
		"leg_r_rot": 12.5, "leg_r_dx": -2, "leg_r_dy": 0,
	},
	{
		"name": "Frame 3",
		"torso_dy": -1,
		"leg_l_rot": 22.0, "leg_l_dx": -5, "leg_l_dy": -4,
		"leg_r_rot": 13.0, "leg_r_dx": 0, "leg_r_dy": 1,
	},
]

static func _rotate_and_translate_layer(src: Image, angle_deg: float, pivot: Vector2, translate: Vector2i) -> Image:
	var dst := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	dst.fill(Color(0, 0, 0, 0))
	if src == null or src.is_empty():
		return dst
	if is_zero_approx(angle_deg):
		var src_rect := Rect2i(0, 0, 128, 128)
		dst.blend_rect(src, src_rect, translate)
		return dst

	var rad := deg_to_rad(angle_deg)
	var cos_a := cos(rad)
	var sin_a := sin(rad)

	for y in range(85, 126):
		for x in range(30, 95):
			var tx: float = float(x - translate.x) - pivot.x
			var ty: float = float(y - translate.y) - pivot.y
			var sx: float = pivot.x + tx * cos_a + ty * sin_a
			var sy: float = pivot.y - tx * sin_a + ty * cos_a

			var x0: int = int(floor(sx))
			var y0: int = int(floor(sy))
			var x1: int = x0 + 1
			var y1: int = y0 + 1

			if x0 < 0 or x1 >= 128 or y0 < 0 or y1 >= 128:
				continue

			var fx: float = sx - float(x0)
			var fy: float = sy - float(y0)

			var c00: Color = src.get_pixel(x0, y0)
			var c10: Color = src.get_pixel(x1, y0)
			var c01: Color = src.get_pixel(x0, y1)
			var c11: Color = src.get_pixel(x1, y1)

			var c0: Color = c00.lerp(c10, fx)
			var c1: Color = c01.lerp(c11, fx)
			var c: Color = c0.lerp(c1, fy)

			if c.a > 0.02:
				dst.set_pixel(x, y, c)

	return dst

static func _blend_slot(canvas: Image, entry_map: Dictionary, slot_id: String, offset: Vector2i) -> void:
	var entry: Dictionary = entry_map.get(slot_id, {})
	var tex: Texture2D = entry.get("texture", null)
	if tex == null:
		return
	var img: Image = tex.get_image()
	if img == null or img.is_empty():
		return
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	var rect := Rect2i(0, 0, img.get_width(), img.get_height())
	canvas.blend_rect(img, rect, offset)

## 依據種族、幀數 (0..3) 與換裝選擇，執行期分部位即時合成走路姿態
static func build_walk_composite_image(race: String, frame: int, slot_selection: Dictionary = {}) -> Image:
	var rid := race.to_lower().strip_edges()
	var f_idx := posmod(frame, 4)
	if rid != "rabbit":
		var base_img: Image = null
		var baked_path := "%s/%s_walk_%d_x3.png" % [ROOT_SPRITES, rid, f_idx]
		var baked_tex := get_slot_texture(baked_path)
		if baked_tex:
			base_img = baked_tex.get_image()
			if base_img and base_img.get_format() != Image.FORMAT_RGBA8:
				base_img.convert(Image.FORMAT_RGBA8)
		if base_img == null:
			base_img = build_composite_image(rid, slot_selection)
		else:
			for sid in ["costume", "weapon"]:
				if slot_selection.has(sid) and str(slot_selection[sid]) != "":
					var path := resolve_slot_texture_path(rid, sid, str(slot_selection[sid]))
					var tex := get_slot_texture(path)
					if tex:
						var img := tex.get_image()
						if img and not img.is_empty():
							if img.get_format() != Image.FORMAT_RGBA8:
								img.convert(Image.FORMAT_RGBA8)
							base_img.blend_rect(img, Rect2i(0, 0, img.get_width(), img.get_height()), Vector2i.ZERO)
		return base_img

	# 兔族分部位關節運動學合成
	var entries := get_sorted_slot_entries("rabbit", slot_selection)
	var entry_map := {}
	for e in entries:
		entry_map[str(e.get("slot_id", ""))] = e

	var chassis_entry: Dictionary = entry_map.get(SLOT_CHASSIS, {})
	var chassis_tex: Texture2D = chassis_entry.get("texture", null)
	var chassis_img: Image = null
	if chassis_tex:
		chassis_img = chassis_tex.get_image()
		if chassis_img and chassis_img.get_format() != Image.FORMAT_RGBA8:
			chassis_img.convert(Image.FORMAT_RGBA8)

	if chassis_img == null or chassis_img.is_empty():
		return build_composite_image("rabbit", slot_selection)

	# 1. 分解 chassis 軀幹、骨盆、雙腿與影子
	var shadow_img := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	var torso_chassis := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	var pelvis := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	var leg_l := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	var leg_r := Image.create(128, 128, false, Image.FORMAT_RGBA8)

	for y in range(128):
		for x in range(128):
			var c: Color = chassis_img.get_pixel(x, y)
			if c.a <= 0.0:
				continue
			if y >= 118 and (c.a <= 200.0 / 255.0 or (c.r < 50.0 / 255.0 and c.g < 50.0 / 255.0 and c.b < 70.0 / 255.0)):
				shadow_img.set_pixel(x, y, c)
				continue
			if y < 98:
				torso_chassis.set_pixel(x, y, c)
			else:
				if x <= 61:
					leg_l.set_pixel(x, y, c)
				else:
					leg_r.set_pixel(x, y, c)
			# 骨盆完整覆蓋切割線上下各 3px (y=95..101)，隨軀幹位移消除接縫橫向空洞 (Rule 4b-13)
			if y >= 95 and y <= 101:
				pelvis.set_pixel(x, y, c)

	var gait: Dictionary = RABBIT_WALK_GAIT[f_idx]
	var tdy: int = int(gait.get("torso_dy", 0))
	var pivot_l := Vector2(52, 98)
	var pivot_r := Vector2(71, 98)

	# 2. 雙腿各自關節位移與旋轉 (Rule 4b-7 / 4b-7-1)
	var lr_rot: float = float(gait.get("leg_r_rot", 0.0))
	var lr_trans := Vector2i(int(gait.get("leg_r_dx", 0)), int(gait.get("leg_r_dy", 0)))
	var leg_r_tx := _rotate_and_translate_layer(leg_r, lr_rot, pivot_r, lr_trans)

	var ll_rot: float = float(gait.get("leg_l_rot", 0.0))
	var ll_trans := Vector2i(int(gait.get("leg_l_dx", 0)), int(gait.get("leg_l_dy", 0)))
	var leg_l_tx := _rotate_and_translate_layer(leg_l, ll_rot, pivot_l, ll_trans)

	# 3. 依 z_index 階梯與部位上下關係疊合
	var canvas := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	canvas.fill(Color(0, 0, 0, 0))
	var full_rect := Rect2i(0, 0, 128, 128)

	# 腳底軟影帶（固定在基底）
	canvas.blend_rect(shadow_img, full_rect, Vector2i.ZERO)

	# z=5: winding_key（隨軀幹微幅浮沉）
	_blend_slot(canvas, entry_map, SLOT_WINDING_KEY, Vector2i(0, tdy))

	# z=8: back_curio
	_blend_slot(canvas, entry_map, SLOT_BACK_CURIO, Vector2i(0, tdy))

	# 後腿
	canvas.blend_rect(leg_r_tx, full_rect, Vector2i.ZERO)

	# 骨盆底層
	canvas.blend_rect(pelvis, full_rect, Vector2i(0, tdy))

	# 前腿
	canvas.blend_rect(leg_l_tx, full_rect, Vector2i.ZERO)

	# 軀幹主機體
	canvas.blend_rect(torso_chassis, full_rect, Vector2i(0, tdy))

	# z=20: head_unit
	_blend_slot(canvas, entry_map, SLOT_HEAD_UNIT, Vector2i(0, tdy))

	# z=25: costume 玩具外裝獨立層即時疊合（下擺隨雙腿分段位移與旋轉，防止布料遮蔽腿部步態 Rule 4b-12）
	var costume_entry: Dictionary = entry_map.get(SLOT_COSTUME, {})
	var costume_tex: Texture2D = costume_entry.get("texture", null)
	if costume_tex:
		var cos_img: Image = costume_tex.get_image()
		if cos_img and not cos_img.is_empty():
			if cos_img.get_format() != Image.FORMAT_RGBA8:
				cos_img = cos_img.duplicate()
				cos_img.convert(Image.FORMAT_RGBA8)
			var cos_torso := Image.create(128, 128, false, Image.FORMAT_RGBA8)
			var cos_skirt_l := Image.create(128, 128, false, Image.FORMAT_RGBA8)
			var cos_skirt_r := Image.create(128, 128, false, Image.FORMAT_RGBA8)
			for y in range(128):
				for x in range(128):
					var c: Color = cos_img.get_pixel(x, y)
					if c.a <= 0.0:
						continue
					if y < 98:
						cos_torso.set_pixel(x, y, c)
					else:
						if x <= 61:
							cos_skirt_l.set_pixel(x, y, c)
						else:
							cos_skirt_r.set_pixel(x, y, c)
			var c_lr_rot: float = lr_rot * 0.7
			var c_lr_trans := Vector2i(int(round(float(lr_trans.x) * 0.7)), int(round(float(lr_trans.y) * 0.7)))
			var cos_skirt_r_tx := _rotate_and_translate_layer(cos_skirt_r, c_lr_rot, pivot_r, c_lr_trans)
			var c_ll_rot: float = ll_rot * 0.7
			var c_ll_trans := Vector2i(int(round(float(ll_trans.x) * 0.7)), int(round(float(ll_trans.y) * 0.7)))
			var cos_skirt_l_tx := _rotate_and_translate_layer(cos_skirt_l, c_ll_rot, pivot_l, c_ll_trans)

			canvas.blend_rect(cos_skirt_r_tx, full_rect, Vector2i(0, tdy))
			canvas.blend_rect(cos_skirt_l_tx, full_rect, Vector2i(0, tdy))
			canvas.blend_rect(cos_torso, full_rect, Vector2i(0, tdy))

	# z=30: optic_core
	_blend_slot(canvas, entry_map, SLOT_OPTIC_CORE, Vector2i(0, tdy))

	# z=40: weapon 手持武器獨立層即時疊合
	_blend_slot(canvas, entry_map, SLOT_WEAPON, Vector2i(0, tdy))

	return canvas

static func build_walk_composite_texture(race: String, frame: int, slot_selection: Dictionary = {}) -> Texture2D:
	var img := build_walk_composite_image(race, frame, slot_selection)
	if img != null and not img.is_empty():
		return ImageTexture.create_from_image(img)
	return null

static func get_race_walk_composite_texture(race: String, frame: int, slot_selection: Dictionary = {}) -> Texture2D:
	var rid := race.to_lower().strip_edges()
	var f := posmod(frame, 4)
	if slot_selection.is_empty():
		var baked_path := "%s/%s_walk_%d_x3.png" % [ROOT_SPRITES, rid, f]
		if ResourceLoader.exists(baked_path):
			var res = load(baked_path)
			if res is Texture2D:
				return res as Texture2D
	return build_walk_composite_texture(rid, f, slot_selection)


## ── 安全預設規格 ──
static func _get_fallback_spec() -> Dictionary:
	return {
		"slots_architecture": {
			"total_slots": 7,
			"slots": [
				{"slot_id": "chassis", "name_zh": "軀體外殼與塗裝", "layer_z_index": 10, "required": true},
				{"slot_id": "head_unit", "name_zh": "頭部機關與耳朵造型", "layer_z_index": 20, "required": true},
				{"slot_id": "winding_key", "name_zh": "背部發條鑰匙", "layer_z_index": 5, "required": true},
				{"slot_id": "costume", "name_zh": "玩具外裝與服飾", "layer_z_index": 25, "required": false},
				{"slot_id": "optic_core", "name_zh": "面部光學與表情核心", "layer_z_index": 30, "required": true},
				{"slot_id": "weapon", "name_zh": "手持武器外觀", "layer_z_index": 40, "required": true},
				{"slot_id": "back_curio", "name_zh": "隨身奇玩與尾部機關", "layer_z_index": 8, "required": false}
			]
		},
		"races_specification": {
			"total_races": 5,
			"races": [
				{"race_id": "rabbit", "name_zh": "白金兔", "name_en": "Clockwork Rabbit", "class_archetype": "劍士 (Knight)"},
				{"race_id": "lion", "name_zh": "烈鬃獅", "name_en": "Gilded Lion", "class_archetype": "騎士 (Knight)"},
				{"race_id": "fox", "name_zh": "靈尾狐", "name_en": "Astral Fox", "class_archetype": "法師 (Mage)"},
				{"race_id": "boar", "name_zh": "鋼牙豕", "name_en": "Forge Boar", "class_archetype": "戰士 (Viking)"},
				{"race_id": "macaque", "aliases": ["monkey"], "name_zh": "靈爪猴", "name_en": "Spring Macaque", "class_archetype": "武術家 (Monk)"}
			]
		}
	}


## ── 種族規格讀取與解析 (races_specification) ──

## 取得所有種族規格定義清單
static func get_races() -> Array[Dictionary]:
	var spec := get_spec()
	var races_spec: Dictionary = spec.get("races_specification", {})
	var raw_races: Array = races_spec.get("races", [])
	var typed_races: Array[Dictionary] = []
	for r in raw_races:
		if r is Dictionary:
			typed_races.append(r as Dictionary)
	return typed_races


## 取得所有支援的種族 ID 清單
static func get_race_ids() -> Array[String]:
	var races := get_races()
	var ids: Array[String] = []
	for r in races:
		ids.append(str(r.get("race_id", "")))
	return ids


## 取得特定種族規格
static func get_race_def(race_id: String) -> Dictionary:
	var rid := race_id.to_lower().strip_edges()
	for r in get_races():
		if str(r.get("race_id", "")).to_lower() == rid:
			return r
		var aliases: Array = r.get("aliases", [])
		for a in aliases:
			if str(a).to_lower() == rid:
				return r
	return {}


## 檢查特定種族是否已有可載入的貼圖素材
static func has_race_assets(race_id: String, slot_selections: Dictionary = {}) -> bool:
	var entries := get_sorted_slot_entries(race_id, slot_selections)
	for entry in entries:
		if bool(entry.get("is_loaded", false)):
			return true
	return false

