#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

locales = {
    "zh_TW": {
        "power_stat.windup_card": "冒險委託上發條",
        "power_stat.btn_go_windup": "前往委託",
        "power_stat.windup_progress": "今日委託進度: %d/%d",
        "power_stat.windup_status_done": "今日已完成",
        "power_stat.windup_status_ready": "待完成委託",
        "power_stat.windup_claimed": "今日已領取",
        "power_stat.windup_claimable": "可領取獎勵",
        "power_stat.windup_unclaimed": "今日未領取",
        "power_stat.windup_desc": "每天一件發條小事 · 完成日常委託領取星屑與金幣",
        "冒險委託上發條": "冒險委託上發條",
        "前往委託": "前往委託",
        "今日已完成": "今日已完成",
        "待完成委託": "待完成委託",
        "今日已領取": "今日已領取",
        "可領取獎勵": "可領取獎勵",
        "今日未領取": "今日未領取"
    },
    "zh_CN": {
        "power_stat.windup_card": "冒险委托上发条",
        "power_stat.btn_go_windup": "前往委托",
        "power_stat.windup_progress": "今日委托进度: %d/%d",
        "power_stat.windup_status_done": "今日已完成",
        "power_stat.windup_status_ready": "待完成委托",
        "power_stat.windup_claimed": "今日已领取",
        "power_stat.windup_claimable": "可领取奖励",
        "power_stat.windup_unclaimed": "今日未领取",
        "power_stat.windup_desc": "每天一件发条小事 · 完成日常委托领取星屑与金币",
        "冒險委託上發條": "冒险委托上发条",
        "前往委託": "前往委托",
        "今日已完成": "今日已完成",
        "待完成委託": "待完成委托",
        "今日已領取": "今日已领取",
        "可領取獎勵": "可领取奖励",
        "今日未領取": "今日未领取"
    },
    "en": {
        "power_stat.windup_card": "Adventure Commission Windup",
        "power_stat.btn_go_windup": "To Commission",
        "power_stat.windup_progress": "Commissions: %d/%d",
        "power_stat.windup_status_done": "Completed Today",
        "power_stat.windup_status_ready": "Pending Commission",
        "power_stat.windup_claimed": "Claimed Today",
        "power_stat.windup_claimable": "Reward Ready",
        "power_stat.windup_unclaimed": "Not Claimed",
        "power_stat.windup_desc": "A daily windup chore · Complete commissions for stardust and gold",
        "冒險委託上發條": "Adventure Commission Windup",
        "前往委託": "To Commission",
        "今日已完成": "Completed Today",
        "待完成委託": "Pending Commission",
        "今日已領取": "Claimed Today",
        "可領取獎勵": "Reward Ready",
        "今日未領取": "Not Claimed"
    },
    "ja": {
        "power_stat.windup_card": "冒険依頼ゼンマイ",
        "power_stat.btn_go_windup": "依頼へ",
        "power_stat.windup_progress": "依頼進捗: %d/%d",
        "power_stat.windup_status_done": "本日完了",
        "power_stat.windup_status_ready": "依頼待機中",
        "power_stat.windup_claimed": "本日受取済",
        "power_stat.windup_claimable": "報酬受取可能",
        "power_stat.windup_unclaimed": "未受取",
        "power_stat.windup_desc": "毎日のゼンマイ小話 · 日常依頼を達成して星屑とゴールドを獲得",
        "冒險委託上發條": "冒険依頼ゼンマイ",
        "前往委託": "依頼へ",
        "今日已完成": "本日完了",
        "待完成委託": "依頼待機中",
        "今日已領取": "本日受取済",
        "可領取獎勵": "報酬受取可能",
        "今日未領取": "未受取"
    },
    "ko": {
        "power_stat.windup_card": "모험 의뢰 태엽 감기",
        "power_stat.btn_go_windup": "의뢰 이동",
        "power_stat.windup_progress": "의뢰 진행도: %d/%d",
        "power_stat.windup_status_done": "오늘 완료",
        "power_stat.windup_status_ready": "의뢰 진행 중",
        "power_stat.windup_claimed": "오늘 수령 완료",
        "power_stat.windup_claimable": "보상 수령 가능",
        "power_stat.windup_unclaimed": "미수령",
        "power_stat.windup_desc": "매일 작은 태엽 이야기 · 일일 의뢰 완료하고 스타더스트와 골드 획득",
        "冒險委託上發條": "모험 의뢰 태엽 감기",
        "前往委託": "의뢰 이동",
        "今日已完成": "오늘 완료",
        "待完成委託": "의뢰 진행 중",
        "今日已領取": "오늘 수령 완료",
        "可領取獎勵": "보상 수령 가능",
        "今日未領取": "미수령"
    },
    "es": {
        "power_stat.windup_card": "Cuerda de Encargos",
        "power_stat.btn_go_windup": "Ir a Encargos",
        "power_stat.windup_progress": "Progreso: %d/%d",
        "power_stat.windup_status_done": "Completado Hoy",
        "power_stat.windup_status_ready": "Encargo Pendiente",
        "power_stat.windup_claimed": "Reclamado Hoy",
        "power_stat.windup_claimable": "Recompensa Lista",
        "power_stat.windup_unclaimed": "Sin Reclamar",
        "power_stat.windup_desc": "Una tarea diaria de cuerda · Completa encargos para obtener polvo estelar y oro",
        "冒險委託上發條": "Cuerda de Encargos",
        "前往委託": "Ir a Encargos",
        "今日已完成": "Completado Hoy",
        "待完成委託": "Encargo Pendiente",
        "今日已領取": "Reclamado Hoy",
        "可領取獎勵": "Recompensa Lista",
        "今日未領取": "Sin Reclamar"
    }
}

base_path = "/opt/side/bravesoul-game/game/data/i18n"

for loc, kvs in locales.items():
    # 1. <loc>.json
    f1 = f"{base_path}/{loc}.json"
    with open(f1, "r", encoding="utf-8") as f:
        d1 = json.load(f)
    d1.update(kvs)
    with open(f1, "w", encoding="utf-8") as f:
        json.dump(d1, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 2. content/<loc>/ui.json
    f2 = f"{base_path}/content/{loc}/ui.json"
    with open(f2, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    d2.update(kvs)
    with open(f2, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
        f.write("\n")

print("i18n updated successfully for power_stat windup card!")
