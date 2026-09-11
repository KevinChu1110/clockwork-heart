extends RefCounted
## Alice Art Pivot v2 單幀對照表（SlotId／AnimId → res 路徑）。
## 模組邊界：只負責路徑解析；組裝規則在 Assembler。
## 舊 strip（oh_anim_strip*.png／explore_dismantle_anims）已退役。

const FRAMES_DIR := "res://assets/sprites/pack_a/v2/paper_doll/frames/"

## AnimId（W6-K3 ＋ Alice 別名）→ 單幀檔名
const ANIM_FILES := {
	"idle": "oh_idle.png",
	"ready": "oh_ready.png",
	"hit": "oh_hit.png",
	"one_hand_atk_1": "oh_atk_1.png",
	"one_hand_atk_2": "oh_atk_2.png",
	"one_hand_atk_3": "oh_atk_3.png",
	"oh_attack_1": "oh_atk_1.png",
	"oh_attack_2": "oh_atk_2.png",
	"oh_attack_3": "oh_atk_3.png",
	"atk_1": "oh_atk_1.png",
	"atk_2": "oh_atk_2.png",
	"atk_3": "oh_atk_3.png",
	"explore_walk": "explore_walk.png",
	"dismantle_pull": "dismantle_pull.png",
}

## SlotId → 裝備單幀（身份層暫含在動作幀內）
const SLOT_FILES := {
	"outfit": "outfit_cream_enamel.png",
	"helmet": "helmet_default.png",
	"weapon_main": "weapon_main_sword_1h.png",
}

## 相位預設 AnimId（無顯式 play 時）
const PHASE_ANIM := {
	"explore": "explore_walk",
	"battle": "ready",
	"dismantle": "dismantle_pull",
}


static func anim_path(anim_id: String) -> String:
	var file := str(ANIM_FILES.get(anim_id, ""))
	if file.is_empty():
		return ""
	return FRAMES_DIR + file


static func slot_path(slot_id: String) -> String:
	var file := str(SLOT_FILES.get(slot_id, ""))
	if file.is_empty():
		return ""
	return FRAMES_DIR + file


static func phase_default_anim(phase: String) -> String:
	return str(PHASE_ANIM.get(phase, "idle"))
