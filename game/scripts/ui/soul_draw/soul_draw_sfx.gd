extends RefCounted
## 抽魂流程音效（#91）。只走 AudioManager 既有 API（play / play_ui）。
## - reveal 只用在抽魂翻卡（brief §5）；依框色分 3 級：白（低、輕）／藍（標準）／紫以上（高、亮＋clash 點綴）。
## - 每個時刻最多 2 聲，符合 #16 的同時兩聲上限；音檔都 ≤0.3 秒，跳過演出不會留殘響。
## - 十連一次只播一聲 reveal（取最高框），不疊十聲。

const Catalog := preload("res://scripts/ui/soul_draw/soul_draw_card_catalog.gd")

## 框色 → 稀有度級（0 白、1 藍、2 紫以上）
const FRAME_LEVEL := {"white": 0, "blue": 1, "purple": 2, "gold": 2, "rainbow": 2}
## 每級的 reveal 音高／音量（dB），以及要不要加 clash 點綴
const REVEAL_BY_LEVEL := [
	{"pitch": 0.88, "db": -5.0, "accent": false},
	{"pitch": 1.0, "db": -1.0, "accent": false},
	{"pitch": 1.16, "db": 1.0, "accent": true},
]

## 測試用：最近播過的 [key, pitch, db]
static var calls: Array = []


static func _am() -> Node:
	var loop := Engine.get_main_loop()
	if loop is SceneTree and (loop as SceneTree).root != null:
		return (loop as SceneTree).root.get_node_or_null("AudioManager")
	return null


static func _play(key: String, pitch: float = 1.0, db: float = 0.0) -> void:
	calls.append([key, pitch, db])
	var am := _am()
	if am and am.has_method("play"):
		am.call("play", key, pitch, db)


## 按下單抽／十連
static func play_pull() -> void:
	calls.append(["ui", 1.0, -2.0])
	var am := _am()
	if am and am.has_method("play_ui"):
		am.call("play_ui")


## 召喚演出開始：發條上鍊聲（十連稍低沉）
static func play_summon_start(is_ten: bool) -> void:
	_play("clock", 0.82 if is_ten else 0.95, -2.0)


static func level_for_drop(drop: Dictionary) -> int:
	var key := Catalog.frame_key_for_drop(Catalog.normalize_drop(drop))
	return int(FRAME_LEVEL.get(key, 1))


## 翻卡／結果卡出現
static func play_reveal_level(level: int) -> void:
	var cfg: Dictionary = REVEAL_BY_LEVEL[clampi(level, 0, REVEAL_BY_LEVEL.size() - 1)]
	_play("reveal", float(cfg["pitch"]), float(cfg["db"]))
	if bool(cfg["accent"]):
		_play("clash", 1.3, -4.0)


static func play_reveal_for_drop(drop: Dictionary) -> void:
	play_reveal_level(level_for_drop(drop))


## 十連結算：只播一次，取最高框
static func play_reveal_for_drops(drops: Array) -> void:
	var best := 0
	for d in drops:
		if d is Dictionary:
			best = maxi(best, level_for_drop(d))
	play_reveal_level(best)
