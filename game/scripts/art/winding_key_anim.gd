extends RefCounted
## 背後發條鑰匙待機動畫（任務書 §3）：每 8 幀轉一格，一圈 8 格。
##
## 目前沒有手繪的鑰匙轉動幀，所以用程式把 winding_key 圖層繞樞軸做「側面看的軸向旋轉」：
## 鑰匙柄朝外插在背上，從側面看就是鑰匙頭沿垂直方向壓扁、翻面再展開。
## 只動鑰匙主體所在的矩形，其他圖層（含鑰匙圖層的零星雜點）保持不動。
##
## 之後有手繪幀時，放到 HAND_FRAMES_DIR/<race>/hero_winding_key_idle_00..07.png（512 畫布，只畫鑰匙），
## build_idle_key_frames_512 會優先用手繪幀。
##
## 不用 class_name，請 preload 使用；不在編譯期引用 autoload。

const PaperdollRenderer = preload("res://scripts/art/paperdoll_renderer.gd")

const FRAMES_PER_STEP := 8
## 「每 8 幀」是 60 FPS 的動畫幀，不是渲染幀（#61）：一格 = 8/60 秒，一秒 7.5 格。
## 以前在 _process 數渲染幀，120／144Hz 螢幕轉速快到 2～2.4 倍、掉幀又變慢。
const ANIM_FPS := 60.0
const STEP_SECONDS := float(FRAMES_PER_STEP) / ANIM_FPS
const STEPS_PER_TURN := 8
const CANVAS := 512
const SLOT_KEY := "winding_key"
## 鑰匙頭最窄時保留的厚度比例（避免整支消失）
const MIN_AXIAL := 0.18
## 壓扁取樣：每個目標像素平均幾列來源
const SUBSAMPLES := 6
const HAND_FRAMES_DIR := "res://assets/sprites/player/paperdoll/%s/winding_key_frames"

## 已量過的鑰匙：主體矩形 (x0, y0, x1, y1) 與樞軸（鑰匙柄插進背板的位置），512 畫布座標
const KEY_GEOMETRY := {
	"rabbit/key_classic_brass": {"rect": Rect2i(140, 256, 56, 80), "pivot": Vector2(190, 296)},
	## 展示立繪 HD 鑰匙層（1344×1680 畫布，不是 512）：只拿來定樞軸，轉法見 WindingKeyTicker.attach_key_layer
	"rabbit/showcase_hd": {"rect": Rect2i(344, 840, 174, 234), "pivot": Vector2(512, 970)},
}

## 每組 8 張 512 貼圖約 8 MB，衣櫥換裝會一直產生新組合，所以只留幾組
const MAX_CACHE := 4
static var _frames_cache: Dictionary = {}


## 第 step 格的軸向縮放：cos(step·45°)，保留最小厚度並帶正負號（負號 = 翻到背面）
static func axial_scale(step: int) -> float:
	var c := cos(float(posmod(step, STEPS_PER_TURN)) * TAU / float(STEPS_PER_TURN))
	var sgn := 1.0 if c >= 0.0 else -1.0
	return sgn * maxf(absf(c), MIN_AXIAL)


## 幀計數 → 第幾格（每 FRAMES_PER_STEP 幀進一格）
static func step_for_frame(frame_count: int) -> int:
	return posmod(frame_count / FRAMES_PER_STEP, STEPS_PER_TURN)


## 時間累加器（純函式）：把這幀的 delta 加進 accum，回傳 [這幀要進幾格, 剩下的秒數]。
## 浮點累加 8 次 1/60 會差一點點，給 1µs 容差，免得 60Hz 下拖到第 9 幀。
static func accumulate(accum: float, delta: float) -> Array:
	var t := accum + maxf(delta, 0.0)
	var n := int(floor((t + 0.000001) / STEP_SECONDS))
	t = maxf(0.0, t - float(n) * STEP_SECONDS)
	return [n, t]


## 鑰匙主體矩形與樞軸；沒量過的鑰匙用不透明像素外框，樞軸取右緣中點（貼背那側）
static func key_geometry(race: String, key_id: String, key_img: Image) -> Dictionary:
	var k := "%s/%s" % [race, key_id]
	if KEY_GEOMETRY.has(k):
		return KEY_GEOMETRY[k]
	var used := key_img.get_used_rect()
	if used.size.x <= 0 or used.size.y <= 0:
		return {}
	return {"rect": used, "pivot": Vector2(used.position.x + used.size.x, used.position.y + used.size.y * 0.5)}


static func resolved_key_id(race: String, sel: Dictionary) -> String:
	var kid := str(sel.get(SLOT_KEY, ""))
	if kid.is_empty():
		kid = PaperdollRenderer._get_default_variant_id(race, SLOT_KEY)
	return kid


## 把鑰匙圖層第 step 格畫出來（回傳新的 512 Image）
static func transform_key_image(key_img: Image, geom: Dictionary, step: int) -> Image:
	var out := key_img.duplicate() as Image
	if geom.is_empty():
		return out
	var rect: Rect2i = geom["rect"]
	var py: float = (geom["pivot"] as Vector2).y
	var s := axial_scale(step)
	# 正面亮、轉到側面略暗，讓轉動讀得出來
	var shade := 0.72 + 0.28 * absf(s)
	var x0 := clampi(rect.position.x, 0, out.get_width())
	var x1 := clampi(rect.position.x + rect.size.x, 0, out.get_width())
	var y0 := clampi(rect.position.y, 0, out.get_height())
	var y1 := clampi(rect.position.y + rect.size.y, 0, out.get_height())
	# 每個目標像素在來源上取 SUBSAMPLES 列平均（預乘 alpha），壓扁時描邊才不會碎成雜點
	for y in range(y0, y1):
		for x in range(x0, x1):
			var acc := Color(0, 0, 0, 0)
			for k in range(SUBSAMPLES):
				var fy := float(y) - 0.5 + (float(k) + 0.5) / float(SUBSAMPLES)
				var iy := int(floor(py + (fy - py) / s))
				if iy < y0 or iy >= y1:
					continue
				var c := key_img.get_pixel(x, iy)
				acc.r += c.r * c.a
				acc.g += c.g * c.a
				acc.b += c.b * c.a
				acc.a += c.a
			var c_out := Color(0, 0, 0, 0)
			if acc.a > 0.0:
				var a := acc.a / float(SUBSAMPLES)
				c_out = Color(acc.r / acc.a * shade, acc.g / acc.a * shade, acc.b / acc.a * shade, minf(1.0, a * 1.15))
			out.set_pixel(x, y, c_out)
	return out


static func _hand_frame(race: String, step: int) -> Image:
	var p := (HAND_FRAMES_DIR % race) + "/hero_winding_key_idle_%02d.png" % step
	if ResourceLoader.exists(p):
		var t := load(p) as Texture2D
		if t != null:
			return t.get_image()
	return null


static func _layer_image(tex: Texture2D) -> Image:
	if tex == null:
		return null
	var img := tex.get_image()
	if img == null or img.is_empty():
		return null
	img = img.duplicate() as Image
	if img.is_compressed():
		img.decompress()
	if img.get_format() != Image.FORMAT_RGBA8:
		img.convert(Image.FORMAT_RGBA8)
	if img.get_width() != CANVAS or img.get_height() != CANVAS:
		img.resize(CANVAS, CANVAS, Image.INTERPOLATE_LANCZOS)
	return img


## 待機 8 格：本體照 z 序合成，鑰匙那層換成第 n 格。素材不齊（不是 512 本體）回空陣列。
static func build_idle_key_frames_512(race: String, sel: Dictionary = {}) -> Array[Texture2D]:
	var rid := race.strip_edges().to_lower()
	var cache_key := "%s:%s" % [rid, JSON.stringify(sel)]
	if _frames_cache.has(cache_key):
		return _frames_cache[cache_key]
	if _frames_cache.size() >= MAX_CACHE:
		_frames_cache.clear()
	var out: Array[Texture2D] = []
	var entries := PaperdollRenderer.get_sorted_slot_entries_512(rid, sel)
	var below := Image.create(CANVAS, CANVAS, false, Image.FORMAT_RGBA8)
	var above := Image.create(CANVAS, CANVAS, false, Image.FORMAT_RGBA8)
	below.fill(Color(0, 0, 0, 0))
	above.fill(Color(0, 0, 0, 0))
	var key_img: Image = null
	var has_chassis_512 := false
	for entry in entries:
		var sid: String = str(entry.get("slot_id", ""))
		var p: String = str(entry.get("texture_path", ""))
		if sid == "chassis" and p.ends_with("_512.png"):
			has_chassis_512 = true
		var img := _layer_image(entry.get("texture", null))
		if img == null:
			continue
		if sid == SLOT_KEY:
			key_img = img
			continue
		if sid in ["chassis", "head_unit", "optic_core"] and not p.ends_with("_512.png"):
			_frames_cache[cache_key] = out
			return out
		var dst := below if key_img == null else above
		dst.blend_rect(img, Rect2i(0, 0, CANVAS, CANVAS), Vector2i.ZERO)
	if not has_chassis_512 or key_img == null:
		_frames_cache[cache_key] = out
		return out
	var geom := key_geometry(rid, resolved_key_id(rid, sel), key_img)
	for step in range(STEPS_PER_TURN):
		var frame := below.duplicate() as Image
		var k := _hand_frame(rid, step)
		if k == null:
			k = transform_key_image(key_img, geom, step)
		else:
			k = _layer_image(ImageTexture.create_from_image(k))
		frame.blend_rect(k, Rect2i(0, 0, CANVAS, CANVAS), Vector2i.ZERO)
		frame.blend_rect(above, Rect2i(0, 0, CANVAS, CANVAS), Vector2i.ZERO)
		out.append(ImageTexture.create_from_image(frame))
	_frames_cache[cache_key] = out
	return out


static var _layer_frames_cache: Dictionary = {}


## 只有鑰匙那層的 8 格（大廳把鑰匙放在獨立節點，疊在本體後面）
static func build_key_layer_frames_512(race: String, key_id: String, key_tex: Texture2D) -> Array[Texture2D]:
	var rid := race.strip_edges().to_lower()
	var ck := "%s/%s/%d" % [rid, key_id, key_tex.get_instance_id() if key_tex != null else 0]
	if _layer_frames_cache.has(ck):
		return _layer_frames_cache[ck]
	if _layer_frames_cache.size() >= MAX_CACHE:
		_layer_frames_cache.clear()
	var out: Array[Texture2D] = []
	var key_img := _layer_image(key_tex)
	if key_img == null:
		return out
	var geom := key_geometry(rid, key_id, key_img)
	for step in range(STEPS_PER_TURN):
		var k := _hand_frame(rid, step)
		if k == null:
			k = transform_key_image(key_img, geom, step)
		else:
			k = _layer_image(ImageTexture.create_from_image(k))
		out.append(ImageTexture.create_from_image(k))
	_layer_frames_cache[ck] = out
	return out


static func clear_cache() -> void:
	_layer_frames_cache.clear()
	_frames_cache.clear()
