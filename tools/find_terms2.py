import json, glob, os

for path in glob.glob('/opt/side/bravesoul-game/game/data/i18n/**/*.json', recursive=True):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        if isinstance(d, dict):
            for k, v in d.items():
                if any(t in str(k) or (isinstance(v, str) and t in v) for t in ['星紋', '斗篷', '隨機', '還原']):
                    print(f"{os.path.basename(path)}: {k} -> {v}")
    except Exception:
        pass
