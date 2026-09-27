import hashlib

def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

print("qa38 zh_TW:", md5("/opt/side/bravesoul-game/proofs/qa_round38/proof_05_battle_broken_zh_TW.png"))
print("parent zh_TW:", md5("/opt/side/bravesoul-game/proofs/battle-broken-i18n/proof_battle_broken_zh_TW.png"))

print("qa38 en:", md5("/opt/side/bravesoul-game/proofs/qa_round38/proof_06_battle_broken_en.png"))
print("parent en:", md5("/opt/side/bravesoul-game/proofs/battle-broken-i18n/proof_battle_broken_en.png"))
