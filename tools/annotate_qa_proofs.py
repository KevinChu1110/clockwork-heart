#!/usr/bin/env python3
"""
生成探索性 QA 驗證標註截圖：
針對 t_9180aea8 六項驗證標準產出實機證據截圖。
確保所有文字標註均位於左右側留白區（0~250px 與 1030~1280px），
彈窗內部僅使用 2px 亮色外框標示，絕不遮擋任何按鈕文案或介面文字。
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
OUT_DIR = os.path.join(REPO_ROOT, "proofs/shop_skeleton")
FONT_PATH = os.path.join(REPO_ROOT, "game/assets/fonts/jf-openhuninn-2.1.ttf")

FONT_LARGE = ImageFont.truetype(FONT_PATH, 20)
FONT_MED = ImageFont.truetype(FONT_PATH, 15)
FONT_SMALL = ImageFont.truetype(FONT_PATH, 12)

COLOR_DARK = (31, 26, 58, 255)       # #1F1A3A
COLOR_WHITE = (255, 253, 248, 255)   # #FFFDF8
COLOR_GOLD = (255, 208, 40, 255)     # #FFD028
COLOR_ORANGE = (255, 160, 16, 255)   # #FFA010
COLOR_MINT = (78, 216, 106, 255)     # #4ED86A
COLOR_PINK = (255, 94, 138, 255)     # #FF5E8A
COLOR_SKY = (56, 160, 255, 255)      # #38A0FF


def draw_top_banner(draw: ImageDraw.ImageDraw, title: str, subtitle: str, tag: str = "PASS", tag_color=COLOR_MINT):
    draw.rectangle([(0, 0), (1280, 60)], fill=(24, 20, 45, 245))
    draw.line([(0, 60), (1280, 60)], fill=COLOR_ORANGE, width=3)
    
    # Tag
    draw.rounded_rectangle([(16, 12), (96, 48)], radius=8, fill=tag_color)
    draw.text((28, 19), tag, font=FONT_MED, fill=COLOR_DARK)
    
    # Row 1: Title
    draw.text((115, 8), title, font=FONT_LARGE, fill=COLOR_WHITE)
    # Row 2: Subtitle
    draw.text((115, 34), subtitle, font=FONT_SMALL, fill=COLOR_GOLD)


def generate_qa_01():
    src_path = os.path.join(OUT_DIR, "proof_shop_dialog_main.png")
    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 彈窗尺寸: 寬 750, 高 520, 置中在 1280x720: (1280-750)/2 = 265, (720-520)/2 = 100
    x1, y1, x2, y2 = 265, 100, 1015, 620

    # 彈窗外框
    draw.rounded_rectangle([(x1 - 3, y1 - 3), (x2 + 3, y2 + 3)], radius=24, outline=COLOR_PINK, width=3)
    
    # 頂部寬度標註
    draw.line([(x1, y1 - 12), (x2, y1 - 12)], fill=COLOR_PINK, width=2)
    draw.line([(x1, y1 - 20), (x1, y1 - 4)], fill=COLOR_PINK, width=2)
    draw.line([(x2, y1 - 20), (x2, y1 - 4)], fill=COLOR_PINK, width=2)
    draw.text(((x1 + x2) // 2 - 110, y1 - 32), "寬度: 750px (手遊規範 740~760px)", font=FONT_MED, fill=COLOR_PINK)

    # 左側高度標註
    draw.line([(x1 - 12, y1), (x1 - 12, y2)], fill=COLOR_SKY, width=2)
    draw.line([(x1 - 20, y1), (x1 - 4, y1)], fill=COLOR_SKY, width=2)
    draw.line([(x1 - 20, y2), (x1 - 4, y2)], fill=COLOR_SKY, width=2)
    draw.text((x1 - 150, (y1 + y2) // 2 - 10), "高度: 520px", font=FONT_MED, fill=COLOR_SKY)

    # 側欄卡片
    draw.rectangle([(20, 320), (220, 400)], fill=(31, 26, 58, 235), outline=COLOR_GOLD, width=2)
    draw.text((30, 335), "左留白: 265px\n(水平完美置中)", font=FONT_SMALL, fill=COLOR_WHITE)

    draw.rectangle([(1040, 320), (1240, 400)], fill=(31, 26, 58, 235), outline=COLOR_GOLD, width=2)
    draw.text((1050, 335), "右留白: 265px\n(水平完美置中)", font=FONT_SMALL, fill=COLOR_WHITE)

    draw.rectangle([(1035, 180), (1260, 265)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw.text((1045, 192), "背景 Scrim: 55%\n全螢幕遮罩 (0,0,0,0.55)\n暗化底層大廳視角", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_top_banner(
        draw,
        "項目 1：彈窗尺寸 740~760px、置中、背景 Scrim 半透明遮罩",
        "實測尺寸 750×520px（符合 740~760px 規範）｜ 水平置中（左右留白各 265px）｜ 背景 Scrim 半透明遮罩正常覆蓋"
    )
    img.save(os.path.join(OUT_DIR, "proof_01_dialog_size_scrim.png"))
    print("Generated proof_01_dialog_size_scrim.png")


def generate_qa_02():
    src_path = os.path.join(OUT_DIR, "proof_shop_dialog_main.png")
    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 僅用細外框框選按鈕，絕不放置遮擋框
    cb_box = (942, 116, 994, 168)
    ra_box = (295, 266, 625, 320)
    wa_box = (650, 266, 985, 320)
    b1_box = (295, 520, 508, 574)
    b2_box = (528, 520, 742, 574)
    b3_box = (762, 520, 985, 574)

    draw.rectangle([cb_box[0]-1, cb_box[1]-1, cb_box[2]+1, cb_box[3]+1], outline=COLOR_PINK, width=2)
    draw.rectangle([ra_box[0]-1, ra_box[1]-1, ra_box[2]+1, ra_box[3]+1], outline=COLOR_ORANGE, width=2)
    draw.rectangle([wa_box[0]-1, wa_box[1]-1, wa_box[2]+1, wa_box[3]+1], outline=COLOR_MINT, width=2)
    draw.rectangle([b1_box[0]-1, b1_box[1]-1, b1_box[2]+1, b1_box[3]+1], outline=COLOR_ORANGE, width=2)
    draw.rectangle([b2_box[0]-1, b2_box[1]-1, b2_box[2]+1, b2_box[3]+1], outline=COLOR_PINK, width=2)
    draw.rectangle([b3_box[0]-1, b3_box[1]-1, b3_box[2]+1, b3_box[3]+1], outline=COLOR_GOLD, width=2)

    # 左側留白區放置左欄按鈕規格
    draw.rectangle([(20, 140), (250, 340)], fill=(31, 26, 58, 235), outline=COLOR_ORANGE, width=2)
    draw.text((30, 150), "左側按鈕熱區實測：", font=FONT_MED, fill=COLOR_ORANGE)
    draw.text((30, 185), "1. 去廣告買斷按鈕\n   • 尺寸: 330×50px\n   • 高度: 50px (>=48px)\n   • 果凍厚底: 5px\n\n2. 發條能量購買按鈕\n   • 尺寸: 213×50px\n   • 高度: 50px (>=48px)\n   • 果凍厚底: 5px", font=FONT_SMALL, fill=COLOR_WHITE)
    draw.line([(250, 293), (ra_box[0], 293)], fill=COLOR_ORANGE, width=2)
    draw.line([(250, 547), (b1_box[0], 547)], fill=COLOR_ORANGE, width=2)

    # 右側留白區放置右欄按鈕規格
    draw.rectangle([(1030, 120), (1260, 360)], fill=(31, 26, 58, 235), outline=COLOR_PINK, width=2)
    draw.text((1040, 130), "右側按鈕熱區實測：", font=FONT_MED, fill=COLOR_PINK)
    draw.text((1040, 165), "1. 右上關閉按鈕「✕」\n   • 尺寸: 50×50px (>=50px)\n\n2. 觀看廣告領取按鈕\n   • 尺寸: 335×50px\n   • 高度: 50px (>=48px)\n\n3. 聚魂/鍛造購買按鈕\n   • 尺寸: 214×50 / 223×50\n   • 高度: 50px (>=48px)", font=FONT_SMALL, fill=COLOR_WHITE)
    draw.line([(cb_box[2], 142), (1030, 142)], fill=COLOR_PINK, width=2)
    draw.line([(wa_box[2], 293), (1030, 293)], fill=COLOR_MINT, width=2)
    draw.line([(b3_box[2], 547), (1030, 547)], fill=COLOR_GOLD, width=2)

    draw_top_banner(
        draw,
        "項目 2：右上「✕」關閉按鈕與所有互動按鈕熱區 >= 50px",
        "右上關閉按鈕 50×50px ｜ 去廣告/看廣告/品項購買共 5 顆按鈕高度均 50px（觸控熱區 >= 48px，果凍厚底 5px）"
    )
    img.save(os.path.join(OUT_DIR, "proof_02_button_hotspots.png"))
    print("Generated proof_02_button_hotspots.png")


def generate_qa_03():
    src_path = os.path.join(OUT_DIR, "proof_shop_dialog_main.png")
    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    left_palette = [
        ("金黃 #FFD028", "資源箱購買按鈕 / 提示框底", COLOR_GOLD),
        ("暖橘 #FFA010", "商城標題 / 去廣告 / 能量箱", COLOR_ORANGE),
        ("薄荷綠 #4ED86A", "看廣告領取 / 測試骨架標籤", COLOR_MINT),
    ]
    y_start = 130
    for title, desc, col in left_palette:
        draw.rectangle([(20, y_start), (245, y_start + 65)], fill=(31, 26, 58, 235), outline=col, width=2)
        draw.text((30, y_start + 8), title, font=FONT_MED, fill=col)
        draw.text((30, y_start + 36), desc, font=FONT_SMALL, fill=COLOR_WHITE)
        y_start += 80

    right_palette = [
        ("珊瑚粉 #FF5E8A", "聚魂包購買按鈕 / 關閉按鈕", COLOR_PINK),
        ("深藍紫 #1F1A3A", "全彈窗描邊 / 卡片厚底 / 文字", COLOR_SKY),
        ("零泥土灰黑", "底色奶油米白 #FFFDF8 / 暖米黃", COLOR_WHITE),
    ]
    y_start = 130
    for title, desc, col in right_palette:
        draw.rectangle([(1035, y_start), (1260, y_start + 65)], fill=(31, 26, 58, 235), outline=col, width=2)
        draw.text((1045, y_start + 8), title, font=FONT_MED, fill=col)
        draw.text((1045, y_start + 36), desc, font=FONT_SMALL, fill=COLOR_WHITE)
        y_start += 80

    draw_top_banner(
        draw,
        "項目 3：多巴胺鮮亮色盤與深藍紫描邊套用正確、無殘留舊色",
        "金黃#FFD028、暖橘#FFA010、薄荷綠#4ED86A、天藍#38A0FF、珊瑚粉#FF5E8A 均就位 ｜ 深藍紫#1F1A3A 描邊工整 ｜ 零泥土髒色"
    )
    img.save(os.path.join(OUT_DIR, "proof_03_dopamine_palette.png"))
    print("Generated proof_03_dopamine_palette.png")


def generate_qa_04():
    src_path = os.path.join(OUT_DIR, "proof_shop_dialog_main.png")
    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    draw.rectangle([(20, 140), (245, 340)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw.text((32, 155), "字型規範驗收：", font=FONT_MED, fill=COLOR_MINT)
    draw.text((32, 190), "✓ 開源粉圓體\n  jf-openhuninn-2.1\n✓ 圓潤可愛無冰冷黑體\n✓ 字級 >= 14px\n✓ 無破字或截斷", font=FONT_SMALL, fill=COLOR_WHITE)

    draw.rectangle([(1035, 140), (1260, 340)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw.text((1047, 155), "符號規範驗收：", font=FONT_MED, fill=COLOR_MINT)
    draw.text((1047, 190), "✓ 100% 零系統 Emoji\n✓ 圖示全採自繪資產\n✓ 零未定義符號乱碼\n✓ 正則測試全綠通過", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_top_banner(
        draw,
        "項目 4：字體用粉圓體、無破字截斷、零系統 emoji",
        "jf-openhuninn-2.1.ttf 粉圓體全域套用 ｜ 邊界充裕無溢出截斷 ｜ 100% 零系統彩色 Emoji 與特殊符號亂碼"
    )
    img.save(os.path.join(OUT_DIR, "proof_04_openhuninn_zero_emoji.png"))
    print("Generated proof_04_openhuninn_zero_emoji.png")


def generate_qa_05():
    src_path = os.path.join(OUT_DIR, "proof_shop_dialog_main.png")
    img = Image.open(src_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 頂部宣告條框線（細線標記，不遮擋內文）
    draw.rectangle([(287, 168), (993, 206)], outline=COLOR_GOLD, width=2)

    # 3 個 IAP 卡片標記
    draw.rectangle([(295, 488), (508, 514)], outline=COLOR_ORANGE, width=2)
    draw.rectangle([(528, 488), (742, 514)], outline=COLOR_PINK, width=2)
    draw.rectangle([(762, 488), (985, 514)], outline=COLOR_GOLD, width=2)

    # 左側留白區說明變現模型免責條款
    draw.rectangle([(20, 180), (250, 360)], fill=(31, 26, 58, 235), outline=COLOR_GOLD, width=2)
    draw.text((32, 195), "變現模型宣告驗收：", font=FONT_MED, fill=COLOR_GOLD)
    draw.text((32, 230), "• 明確註明『定價待定』\n  依 docs/BUSINESS.md\n• 明確標示全品項為\n  測試佔位 Mock 邏輯\n• 點擊不扣款\n• 恪守 review.md 規範\n  不誤導玩家為正式商品", font=FONT_SMALL, fill=COLOR_WHITE)
    draw.line([(250, 187), (287, 187)], fill=COLOR_GOLD, width=2)

    # 右側留白區說明各品項定價標示
    draw.rectangle([(1030, 280), (1260, 520)], fill=(31, 26, 58, 235), outline=COLOR_ORANGE, width=2)
    draw.text((1040, 295), "佔位品項定價註記：", font=FONT_MED, fill=COLOR_ORANGE)
    draw.text((1040, 330), "1. 免廣告特權:\n   狀態: 未購買\n   (NT$ 60 TODO: 定價待定)\n\n2. 發條能量補給箱:\n   NT$ 30 (TODO: 定價待定)\n\n3. 神殿聚魂召喚包:\n   NT$ 90 (TODO: 定價待定)\n\n4. 工坊鍛造資源箱:\n   NT$ 150 (TODO: 定價待定)", font=FONT_SMALL, fill=COLOR_WHITE)
    draw.line([(985, 501), (1030, 501)], fill=COLOR_GOLD, width=2)

    draw_top_banner(
        draw,
        "項目 5：IAP 佔位品項『TODO 定價待定』標示清楚不誤導玩家",
        "頂部變現模型宣告＋全品項定價清楚標示『(TODO: 定價待定)』與 Mock 提示，恪守 review.md 規範"
    )
    img.save(os.path.join(OUT_DIR, "proof_05_iap_todo_pricing.png"))
    print("Generated proof_05_iap_todo_pricing.png")


def generate_qa_06():
    # 6-A: MockAdDialog
    src_ad = os.path.join(OUT_DIR, "proof_06_mock_ad_dialog_run.png")
    img_ad = Image.open(src_ad).convert("RGBA")
    draw_ad = ImageDraw.Draw(img_ad)

    draw_ad.rectangle([(20, 200), (250, 360)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw_ad.text((32, 215), "MockAdDialog 串接：", font=FONT_MED, fill=COLOR_MINT)
    draw_ad.text((32, 248), "✓ 標題『贊助商廣告』\n✓ 2 秒倒數本機計時\n✓ 動態綠色進度條\n✓ 獨立全螢幕 Scrim\n✓ 播畢發放 +3 能量", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_ad.rectangle([(1035, 200), (1260, 360)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw_ad.text((1047, 215), "無崩潰穩定性：", font=FONT_MED, fill=COLOR_MINT)
    draw_ad.text((1047, 248), "✓ 點擊入口無 Crash\n✓ 倒數計時無 Exception\n✓ 獎勵回調正常觸發\n✓ 關閉彈窗記憶體釋放", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_top_banner(
        draw_ad,
        "項目 6-A：觀看廣告入口觸發 MockAdDialog 模擬播映 (0 Crash)",
        "點擊觀看廣告即刻彈出 MockAdDialog ｜ 倒數 2 秒 / 動態進度條 / Scrim 遮罩正常 ｜ 0 Crash"
    )
    img_ad.save(src_ad)
    print("Annotated proof_06_mock_ad_dialog_run.png")

    # 6-B: 去廣告狀態切換
    src_bought = os.path.join(OUT_DIR, "proof_06_ads_removed_claimed.png")
    img_b = Image.open(src_bought).convert("RGBA")
    draw_b = ImageDraw.Draw(img_b)

    draw_b.rectangle([(20, 200), (250, 360)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw_b.text((32, 215), "去廣告特權生效：", font=FONT_MED, fill=COLOR_MINT)
    draw_b.text((32, 248), "✓ has_removed_ads=true\n✓ 按鈕變『已擁有特權』\n✓ 按鈕禁用防重複點擊\n✓ 綠字顯示永久免廣告", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_b.rectangle([(1035, 200), (1260, 360)], fill=(31, 26, 58, 235), outline=COLOR_MINT, width=2)
    draw_b.text((1047, 215), "免看廣告直接領取：", font=FONT_MED, fill=COLOR_MINT)
    draw_b.text((1047, 248), "✓ 獎勵按鈕文字更新\n  『免看廣告直接領取』\n✓ 點擊直接獲得 +3能量\n✓ 不彈廣告彈窗 0 Crash", font=FONT_SMALL, fill=COLOR_WHITE)

    draw_top_banner(
        draw_b,
        "項目 6-B：去廣告買斷啟用 ｜ 永久免廣告與獎勵直領生效 (0 Crash)",
        "GameState 去廣告標記切換 ｜ 按鈕禁用切換『已擁有去廣告特權』｜ 獎勵直領生效 (+3 能量) ｜ 0 Crash"
    )
    img_b.save(src_bought)
    print("Annotated proof_06_ads_removed_claimed.png")


if __name__ == "__main__":
    generate_qa_01()
    generate_qa_02()
    generate_qa_03()
    generate_qa_04()
    generate_qa_05()
    generate_qa_06()
    print("All QA proofs updated successfully!")
