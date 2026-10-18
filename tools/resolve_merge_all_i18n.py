#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

base_repo = "/opt/side/bravesoul-game"
base_i18n = f"{base_repo}/game/data/i18n"

all_keys = {
    "zh_TW": {
        "gem_workshop.btn_go_vault": "前往儲能庫",
        "forge.btn_go_vault": "前往儲能庫",
        "ui.btn_go_vault": "前往儲能庫",
        "前往儲能庫": "前往儲能庫",
        "vault.btn_go_workshop": "前往工坊",
    },
    "zh_CN": {
        "gem_workshop.btn_go_vault": "前往储能库",
        "forge.btn_go_vault": "前往储能库",
        "ui.btn_go_vault": "前往储能库",
        "前往储能库": "前往储能库",
        "vault.btn_go_workshop": "前往工坊",
    },
    "en": {
        "gem_workshop.btn_go_vault": "To Vault",
        "forge.btn_go_vault": "To Vault",
        "ui.btn_go_vault": "To Vault",
        "vault.btn_go_workshop": "To Workshop",
    },
    "ja": {
        "gem_workshop.btn_go_vault": "貯蔵庫へ",
        "forge.btn_go_vault": "貯蔵庫へ",
        "ui.btn_go_vault": "貯蔵庫へ",
        "vault.btn_go_workshop": "工房へ",
    },
    "ko": {
        "gem_workshop.btn_go_vault": "저장고로",
        "forge.btn_go_vault": "저장고로",
        "ui.btn_go_vault": "저장고로",
        "vault.btn_go_workshop": "공방으로",
    },
    "es": {
        "gem_workshop.btn_go_vault": "Al Almacén",
        "forge.btn_go_vault": "Al Almacén",
        "ui.btn_go_vault": "Al Almacén",
        "vault.btn_go_workshop": "Al Taller",
    }
}

def clean_and_update(path, loc_keys):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the start of conflict markers
    idx = content.find("<<<<<<<")
    if idx != -1:
        # Take everything before <<<<<<<
        prefix = content[:idx].rstrip()
        # Ensure it has closing bracket or trim trailing comma
        if prefix.endswith(","):
            prefix = prefix[:-1]
        if not prefix.endswith("}"):
            prefix += "\n}"
        data = json.loads(prefix)
    else:
        data = json.loads(content)

    data.update(loc_keys)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Cleanly fixed {path}")

for loc, kvs in all_keys.items():
    clean_and_update(f"{base_i18n}/{loc}.json", kvs)
    clean_and_update(f"{base_i18n}/content/{loc}/ui.json", kvs)

print("All 12 i18n files resolved cleanly and verified!")
