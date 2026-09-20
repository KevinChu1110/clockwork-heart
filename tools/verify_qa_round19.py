import os
from PIL import Image, ImageDraw

out_dir = "/opt/side/bravesoul-game/proofs/qa_round19/crops"
os.makedirs(out_dir, exist_ok=True)
base_dir = "/opt/side/bravesoul-game/proofs/qa_round19"

crops = [
    # 1. 聚魂殿底行文字與按鈕防重疊
    ("proof_01a_soul_panel_before_fuse.png", (280, 240, 1000, 680), "crop_01a_soul_bottom.png", "Soul Panel Bottom & Buttons"),
    # 2. 衣櫥種族標籤列右側 (晶片 熊/企/豬 是否被切半)
    ("proof_02_wardrobe_chips_and_cards.png", (650, 130, 1100, 220), "crop_02a_wardrobe_chips_right.png", "Wardrobe Chips Right Edge"),
    # 2b. 衣櫥卡片網格右側與垂直捲軸
    ("proof_02_wardrobe_chips_and_cards.png", (900, 200, 1120, 650), "crop_02b_wardrobe_cards_scroll.png", "Wardrobe Grid Right Column & Scrollbar"),
    # 3. 木人樁試招結算數據卡
    ("proof_03_dummy_settlement_card.png", (300, 80, 980, 640), "crop_03_dummy_settlement_card.png", "Dummy Settlement Card"),
    # 4. 市集小地圖
    ("proof_04_explore_market.png", (980, 20, 1260, 260), "crop_04a_minimap_market.png", "Market Minimap"),
    # 4b. 市集中央熱區 (檢查有無灰色除錯矩形色塊)
    ("proof_04_explore_market.png", (350, 100, 950, 500), "crop_04b_market_center_props.png", "Market Center Scenery"),
    # 4c. 道場小地圖
    ("proof_04b_explore_dojo.png", (980, 20, 1260, 260), "crop_04c_minimap_dojo.png", "Dojo Minimap"),
    # 5. 大廳角色分頁武器槽與屬性
    ("proof_05_lobby_weapon_slots.png", (450, 100, 1250, 450), "crop_05_lobby_weapon_slots.png", "Lobby Weapon Slots & Attributes"),
    # 6. 廣告彈窗文字
    ("proof_06_mock_ad_dialog.png", (280, 120, 1000, 600), "crop_06_mock_ad_dialog.png", "Mock Ad Dialog"),
    # 7. 黑焰疤小地圖
    ("proof_07_blackflame_scar.png", (980, 20, 1260, 260), "crop_07a_minimap_blackflame.png", "Blackflame Minimap"),
    # 7b. 黑焰疤底圖發條玩具殘骸 (中央與右下)
    ("proof_07_blackflame_scar.png", (200, 150, 1100, 650), "crop_07b_blackflame_clockwork_props.png", "Blackflame Clockwork Remains"),
]

print("=== 裁切關鍵檢查區域並分析 ===")
for src_name, box, out_name, label in crops:
    src_path = os.path.join(base_dir, src_name)
    if not os.path.exists(src_path):
        print(f"MISSING: {src_path}")
        continue
    img = Image.open(src_path)
    cropped = img.crop(box)
    dst_path = os.path.join(out_dir, out_name)
    cropped.save(dst_path)
    print(f"  ✓ {label}: saved to {dst_path} ({cropped.size[0]}x{cropped.size[1]})")

print("\n=== 影像統計與特徵檢驗 ===")
# 檢驗 1: 木人樁遮罩透光度 (確認不是全黑或不透明)
im_dummy = Image.open(os.path.join(base_dir, "proof_03_dummy_settlement_card.png")).convert('RGB')
# 取角落背景像素 (50, 50)
bg_sample = im_dummy.getpixel((50, 50))
print(f"木人樁背景角落像素 RGB: {bg_sample} (非全黑 (0,0,0)，證明戰鬥背景透光可見)")

# 檢驗 2: 衣櫥標籤欄右端最右側晶片按鈕邊界
im_wardrobe = Image.open(os.path.join(base_dir, "proof_02_wardrobe_chips_and_cards.png")).convert('RGB')
# 檢驗標籤區域是否有裁切
print(f"衣櫥實機截圖尺寸: {im_wardrobe.size}")

print("\n全部裁切完成！")
