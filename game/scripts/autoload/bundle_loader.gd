extends Node
## 開機時把放在執行檔旁或 user://packs/ 的 chapter.pck／extra.pck 掛上。
## Autoload：BundleLoader（排在 AudioManager 之前，BGM 預載才找得到章節曲）。
## 不可在這裡寫 class_name BundlePacks：autoload 編譯早於 global class 快取。

const Packs := preload("res://scripts/systems/bundle_packs.gd")

func _ready() -> void:
	_load_sidecars()


func _load_sidecars() -> void:
	var names: Array[String] = ["chapter", "extra"]
	var bases: Array[String] = []
	var exe := OS.get_executable_path()
	if exe != "":
		bases.append(exe.get_base_dir().path_join("packs"))
	bases.append("user://packs")
	for pack_name in names:
		if Packs.has_pack(pack_name):
			continue
		for b in bases:
			var path := "%s/%s.pck" % [b, pack_name]
			if not FileAccess.file_exists(path):
				continue
			if ProjectSettings.load_resource_pack(path):
				print("BundleLoader: loaded ", path)
			else:
				push_warning("BundleLoader: failed %s" % path)
			break
