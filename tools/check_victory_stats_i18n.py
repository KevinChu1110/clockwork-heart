import json

terms = ["傷害貢獻", "武器傷害貢獻", "輪替切換", "首選武器", "副手武器", "絕技武器", "未裝備", "次", "點"]
langs = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

for lang in langs:
    path = f"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6586cf54/game/data/i18n/content/{lang}/ui.json"
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    missing = [t for t in terms if t not in d]
    print(lang, "missing in ui.json:", missing)

    root_path = f"/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_6586cf54/game/data/i18n/{lang}.json"
    with open(root_path, "r", encoding="utf-8") as f:
        d2 = json.load(f)
    missing2 = [t for t in terms if t not in d2]
    print(lang, "missing in root json:", missing2)
