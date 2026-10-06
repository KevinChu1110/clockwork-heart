extends SceneTree
## 抽魂卡面驗收（美術任務書 §2/§3/§6）：
## 1. 池內每個 DropId 都有卡圖：檔案存在、可載入、128px、透明底、主體完整（不是散點）。
## 2. 模擬十連：每次 10 張、全部 ok、沒有核心碎片、每張卡圖可載入。
## 3. 十連面板實際建出 10 張卡，每張都有貼圖、框色只在五色內、沒有「核心碎片」字樣。
## 4. 稀有度框正好五色（白藍紫金彩）；機芯八階／戰魂品質都壓得進這五色。
## 5. 舊「核心碎片」掉落字典仍能顯示（轉成發條游絲），舊存檔不會出空白卡。

const ConfigScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_config.gd")
const PoolScript := preload("res://scripts/systems/soul_draw_v2/soul_draw_pool.gd")
const Catalog := preload("res://scripts/ui/soul_draw/soul_draw_card_catalog.gd")
const TenPullScript := preload("res://scripts/ui/soul_draw/soul_ten_pull_view.gd")

const RETIRED_ID := "drop_core_shard"
const RETIRED_NAME := "核心碎片"
const FIVE := ["white", "blue", "purple", "gold", "rainbow"]

var _ok := true
var _frame := 0
var _view: Control = null
var _pending_drops: Array[Dictionary] = []
var _texture_cache: Dictionary = {}


func _fail(msg: String) -> void:
	print("  [x] ", msg)
	_ok = false


func _initialize() -> void:
	print("=== test_soul_draw_cards ===")
	var cfg = ConfigScript.new()
	if not cfg.load_from():
		_fail("config load")
		_finish()
		return
	_check_pool_entries(cfg)
	_check_frames()
	_check_legacy()
	_check_ten_pulls(cfg)
	_build_view(cfg)


func _process(_delta: float) -> bool:
	if _view == null:
		return false
	_frame += 1
	if _frame == 1:
		# 等 _ready 建好網格再塞卡
		_view.show_drops(_pending_drops)
	elif _frame == 4:
		_check_view()
		_finish()
		return true
	return false


func _finish() -> void:
	if _view != null and is_instance_valid(_view):
		_view.queue_free()
	if _ok:
		print("TEST_SOUL_DRAW_CARDS_OK")
		quit(0)
	else:
		print("TEST_SOUL_DRAW_CARDS_FAIL")
		quit(1)


# ── 1. 池內卡圖稽核 ─────────────────────────────────────────

func _check_pool_entries(cfg) -> void:
	if cfg.total_weight() != 100:
		_fail("總權重應為 100，實得 %d" % cfg.total_weight())
	if cfg.loot_table.is_empty():
		_fail("LootTable 空的")
	for e in cfg.loot_table:
		var d: Dictionary = e
		var raw_id := str(d.get("DropId", ""))
		var did: String = cfg.resolve_drop_id(raw_id)
		if str(d.get("kind", "")) == "outfit":
			did = cfg.resolve_outfit_id(did)
		if raw_id == RETIRED_ID or did == RETIRED_ID:
			_fail("池裡還有核心碎片")
			continue
		if not Catalog.DROP_ASSETS.has(did):
			_fail("%s 沒有指定卡圖（會掉到保底圖）" % did)
			continue
		var path: String = Catalog.DROP_ASSETS[did]
		_audit_texture(did, path)
		if Catalog.drop_name(did) == did:
			_fail("%s 沒有顯示名稱" % did)
	# 待機卡圖與保底圖也要過同一套稽核
	_audit_texture("idle", Catalog.IDLE_ART)
	_audit_texture("fallback", Catalog.FALLBACK_ART)
	# 核心碎片的 DropId 必須被轉掉
	if cfg.resolve_drop_id(RETIRED_ID) == RETIRED_ID:
		_fail("config 沒把 drop_core_shard 轉成有效零件")


func _audit_texture(label: String, path: String) -> void:
	if _texture_cache.has(path):
		return
	_texture_cache[path] = true
	if not ResourceLoader.exists(path):
		_fail("%s 卡圖不存在：%s" % [label, path])
		return
	var tex := load(path) as Texture2D
	if tex == null or tex.get_width() <= 0 or tex.get_height() <= 0:
		_fail("%s 卡圖載不起來：%s" % [label, path])
		return
	var img := Image.load_from_file(ProjectSettings.globalize_path(path))
	if img == null or img.is_empty():
		_fail("%s 原始 PNG 讀不到：%s" % [label, path])
		return
	if img.get_width() != 128 or img.get_height() != 128:
		_fail("%s 不是 128px 零件圖示（%dx%d）：%s" % [label, img.get_width(), img.get_height(), path])
	img.convert(Image.FORMAT_RGBA8)
	var w := img.get_width()
	var h := img.get_height()
	var solid := PackedByteArray()
	solid.resize(w * h)
	var total := 0
	for y in h:
		for x in w:
			if img.get_pixel(x, y).a > 0.125:
				solid[y * w + x] = 1
				total += 1
	var ratio := float(total) / float(w * h)
	if ratio < 0.2:
		_fail("%s 幾乎是空白（實心 %.1f%%）：%s" % [label, ratio * 100.0, path])
		return
	if ratio > 0.98:
		_fail("%s 沒有透明底（實心 %.1f%%）：%s" % [label, ratio * 100.0, path])
	# 最大連通塊要佔絕大多數 → 排除散點／破圖
	var largest := _largest_component(solid, w, h)
	var share := float(largest) / float(total)
	if share < 0.85:
		_fail("%s 主體破碎、像散點（最大塊 %.0f%%）：%s" % [label, share * 100.0, path])
	else:
		print("  [v] %s → %s（實心 %.0f%%，主體 %.0f%%）" % [label, path.get_file(), ratio * 100.0, share * 100.0])


func _largest_component(solid: PackedByteArray, w: int, h: int) -> int:
	var seen := PackedByteArray()
	seen.resize(w * h)
	var best := 0
	for start in w * h:
		if solid[start] == 0 or seen[start] == 1:
			continue
		var n := 0
		var stack: Array[int] = [start]
		seen[start] = 1
		while not stack.is_empty():
			var i: int = stack.pop_back()
			n += 1
			var x := i % w
			var y := i / w
			if x > 0 and solid[i - 1] == 1 and seen[i - 1] == 0:
				seen[i - 1] = 1
				stack.append(i - 1)
			if x < w - 1 and solid[i + 1] == 1 and seen[i + 1] == 0:
				seen[i + 1] = 1
				stack.append(i + 1)
			if y > 0 and solid[i - w] == 1 and seen[i - w] == 0:
				seen[i - w] = 1
				stack.append(i - w)
			if y < h - 1 and solid[i + w] == 1 and seen[i + w] == 0:
				seen[i + w] = 1
				stack.append(i + w)
		best = maxi(best, n)
	return best


# ── 4. 五色框 ────────────────────────────────────────────

func _check_frames() -> void:
	var keys: Array = Catalog.FRAMES.keys()
	keys.sort()
	var want: Array = FIVE.duplicate()
	want.sort()
	if keys != want:
		_fail("抽卡框應正好五色 %s，實得 %s" % [str(want), str(keys)])
	if Array(Catalog.FRAME_ORDER) != FIVE:
		_fail("FRAME_ORDER 應為 白藍紫金彩")
	for k in Catalog.TIER_TO_FRAME.keys():
		var f: String = Catalog.frame_for_tier(str(k))
		if not FIVE.has(f):
			_fail("內部階 %s 對到未知框 %s" % [k, f])
	# 機芯八階（經濟資料）全部壓進五色，且資料本身不動
	var core_node: Node = root.get_node_or_null("CoreSystem")
	if core_node != null and core_node.get_script() != null:
		var consts: Dictionary = (core_node.get_script() as Script).get_script_constant_map()
		var tiers: Array = consts.get("ALL_TIER_IDS", []) as Array
		if tiers.size() != 8:
			print("  [i] CoreSystem 階數 %d（預期 8，僅提示）" % tiers.size())
		var last_rank := -1
		for t in consts.get("TIER_ORDER", []) as Array:
			var f2: String = Catalog.frame_for_tier(str(t))
			var rank := FIVE.find(f2)
			if rank < 0:
				_fail("機芯階 %s 壓不進五色" % t)
			elif rank < last_rank:
				_fail("機芯階 %s 顯示順序倒退" % t)
			last_rank = maxi(last_rank, rank)
	for q in ["大凶", "凡", "吉", "大吉", "稀世", "神", "秘境"]:
		if not FIVE.has(Catalog.frame_for_tier(q)):
			_fail("戰魂品質 %s 壓不進五色" % q)


# ── 5. 舊存檔相容 ─────────────────────────────────────────

func _check_legacy() -> void:
	var legacy := Catalog.normalize_drop({"DropId": RETIRED_ID, "kind": "part"})
	if str(legacy.get("DropId", "")) != "drop_spring_coil":
		_fail("舊核心碎片沒轉成發條游絲：%s" % str(legacy))
	if Catalog.drop_name(RETIRED_ID) == RETIRED_NAME:
		_fail("舊核心碎片仍顯示「核心碎片」")
	if Catalog.art_texture(RETIRED_ID) == null:
		_fail("舊核心碎片卡圖空白")
	if Catalog.art_texture("drop_does_not_exist") == null:
		_fail("未知 DropId 沒有保底卡圖")


# ── 2. 模擬十連 ──────────────────────────────────────────

func _check_ten_pulls(cfg) -> void:
	var kinds_seen: Dictionary = {}
	for seed_i in 40:
		var pool = PoolScript.new()
		if not pool.setup(cfg, 1000 + seed_i):
			_fail("pool setup")
			return
		var drops := _ten_pull(pool)
		if drops.size() != 10:
			_fail("十連回傳 %d 張" % drops.size())
			continue
		for d in drops:
			var did := str(d.get("DropId", ""))
			kinds_seen[str(d.get("kind", ""))] = true
			if not bool(d.get("ok", false)):
				_fail("抽取失敗 %s" % str(d))
			if did == RETIRED_ID or Catalog.drop_name(did) == RETIRED_NAME:
				_fail("十連抽到核心碎片")
			if not Catalog.DROP_ASSETS.has(did):
				_fail("十連抽到沒有卡圖的 %s" % did)
			elif Catalog.art_texture(did) == null:
				_fail("十連卡圖載入失敗 %s" % did)
	for k in ["part", "outfit"]:
		if not kinds_seen.has(k):
			_fail("400 抽沒出現 %s" % k)
	print("  [v] 40 次十連：每次 10 張、全有卡圖、無核心碎片")


func _ten_pull(pool) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	for i in 10:
		out.append(pool.pull())
	return out


# ── 3. 十連面板 ──────────────────────────────────────────

func _build_view(cfg) -> void:
	var pool = PoolScript.new()
	pool.setup(cfg, 77)
	var drops := _ten_pull(pool)
	# 混入一張舊核心碎片，確認面板也會轉成有效零件
	drops[9] = {"ok": true, "DropId": RETIRED_ID, "kind": "part"}
	_pending_drops = drops
	_view = TenPullScript.new()
	root.add_child(_view)


func _check_view() -> void:
	var cards: Array = _view.get("_cards")
	if cards.size() != 10:
		_fail("十連面板卡數 %d" % cards.size())
		return
	for c in cards:
		var card: Control = c
		var art := card.find_child("CardArt", true, false) as TextureRect
		if art == null or art.texture == null:
			_fail("%s 卡面沒有圖" % card.name)
			continue
		var frame := str(card.get_meta("frame", ""))
		if not FIVE.has(frame):
			_fail("%s 框色 %s 不在五色內" % [card.name, frame])
		var did := str(card.get_meta("drop_id", ""))
		if did == RETIRED_ID:
			_fail("%s 仍是核心碎片" % card.name)
		for lbl in card.find_children("*", "Label", true, false):
			if (lbl as Label).text.find(RETIRED_NAME) >= 0:
				_fail("%s 卡面還寫著核心碎片" % card.name)
	if str((cards[9] as Control).get_meta("drop_id", "")) != "drop_spring_coil":
		_fail("舊核心碎片在面板上沒轉成發條游絲")
	print("  [v] 十連面板 10 張卡全有圖、框色皆屬白藍紫金彩")
