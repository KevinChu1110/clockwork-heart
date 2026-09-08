extends RefCounted
class_name BundlePacks
## 分包邊界：core / chapter / extra。單一真相在 res://data/bundle_manifest.json。
## 之後新地圖預設進 chapter，除非前綴是 village／road／town（大廳＋C0）。

const MANIFEST_PATH := "res://data/bundle_manifest.json"

static var _cache: Dictionary = {}


static func manifest() -> Dictionary:
	if not _cache.is_empty():
		return _cache
	if not FileAccess.file_exists(MANIFEST_PATH):
		push_warning("BundlePacks: missing %s" % MANIFEST_PATH)
		return {}
	var f := FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if f == null:
		return {}
	var data: Variant = JSON.parse_string(f.get_as_text())
	if typeof(data) != TYPE_DICTIONARY:
		push_warning("BundlePacks: manifest 不是 Dictionary")
		return {}
	_cache = data as Dictionary
	return _cache


static func default_pack() -> String:
	return str(manifest().get("default_pack", "chapter"))


static func pack_for_map(map_id: String) -> String:
	var mid := map_id.strip_edges()
	if mid == "":
		return "core"
	var packs: Dictionary = manifest().get("packs", {})
	var core: Dictionary = packs.get("core", {})
	if _matches(mid, core):
		return "core"
	var chap: Dictionary = packs.get("chapter", {})
	if _matches(mid, chap):
		return "chapter"
	return default_pack()


static func _matches(map_id: String, pack: Dictionary) -> bool:
	for p in pack.get("map_prefixes", []):
		var pre := str(p)
		if map_id == pre or map_id.begins_with(pre + "_"):
			return true
	for e in pack.get("map_extra", []):
		if map_id == str(e):
			return true
	return false


static func pack_for_bgm(bgm_id: String) -> String:
	var packs: Dictionary = manifest().get("packs", {})
	for name in ["core", "chapter"]:
		var bgm: Variant = (packs.get(name, {}) as Dictionary).get("bgm", [])
		if bgm is Array and (bgm as Array).has(bgm_id):
			return str(name)
	return "extra"


static func has_pack(pack_name: String) -> bool:
	var packs: Dictionary = manifest().get("packs", {})
	var spec: Dictionary = packs.get(pack_name, {})
	var sentinels: Variant = spec.get("sentinels", [])
	if not (sentinels is Array) or (sentinels as Array).is_empty():
		return true
	for s in sentinels:
		if ResourceLoader.exists(str(s)):
			return true
	return false


static func can_enter_map(map_id: String) -> bool:
	return has_pack(pack_for_map(map_id))


static func missing_pack_line(map_id: String) -> String:
	var pack := pack_for_map(map_id)
	return "後續章節尚未下載（需要 %s 包）" % pack
