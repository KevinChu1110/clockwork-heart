extends SceneTree
## 實機錄影專用驅動腳本：展示今日村莊手遊大廳動態、主角待機呼吸、點擊戳碰互動與粒子
var _lobby: Control = null
var _elapsed: float = 0.0
var _next_poke: float = 6.5
var _poke_count: int = 0

func _initialize() -> void:
	root.size = Vector2i(1280, 720)
	var win := root.get_window()
	if win:
		win.size = Vector2i(1280, 720)

	var scn: GDScript = load("res://scripts/ui/mobile_lobby.gd")
	_lobby = scn.new()
	root.add_child(_lobby)
	print("CAPTURE_LOBBY_VIDEO_READY")

func _process(delta: float) -> bool:
	_elapsed += delta

	# 每隔 4-5 秒點擊一次主角，展示動作切換、對話氣泡與彩色星芒
	if _elapsed >= _next_poke and _poke_count < 6:
		_poke_count += 1
		_next_poke = _elapsed + 4.5
		if _lobby and _lobby.has_method("_on_hero_clicked"):
			_lobby._on_hero_clicked()
			print("POKE_HERO: #", _poke_count, " at ", _elapsed)

	# 錄影 20 秒 + 啟動緩衝 6 秒 = 約 26 秒，設定在 35 秒自動結束防呆
	if _elapsed >= 35.0:
		print("CAPTURE_LOBBY_VIDEO_DONE")
		quit(0)
		return true

	return false
