> 2026-09-11 自 Hermes 移入 repo；以這份為準。美術風格判準看 ../ART_DIRECTION.md。

# 品牌素材與影片製作準則

> **美術風格本身看 `../ART_DIRECTION.md`**（角色、配色、機械化規則、產圖自檢表）。
> 這份講的是**工具、檔案位置與影片製作準則**，不是風格判準。

## ⭐ 主視覺（所有產圖的基準）

`/opt/side/bravesoul-game/branding/key_visual_main.png`

**這是 Kevin 認可的《發條之心》主視覺**：金屬齒輪質感、暖金與青綠的高光、黃銅色調、
發條動物角色（兔、狐、獅、豬）、神殿石柱、中央發條核心與神秘黑袍。

⛔ **產任何圖之前，一律先用它當 `--ref` 參考**：

```bash
python3 /root/gen_media.py image "<提示詞>" 輸出.png \
  --ref /opt/side/bravesoul-game/branding/key_visual_main.png
```

不帶參考圖產出來的東西跟遊戲長得不像，做出來也不能用 —— 這條沒有例外。
需要別的風格（例如純實機截圖風）就用實機錄影，不要另外產一套美術。

## ⛔ 行銷影片不是把圖做成投影片

Kevin 明確退過一版：「**這根本只是把封面照做成投影片而已**」。
行銷影片要有**鏡頭語言**，不是靜圖輪播。他給的正確範例（做為往後的標準）：

> 黑暗中，廢棄的兔子玩具，背後的發條滿滿地轉動
> → 視角從玩具慢慢往前推，推開門
> → 帶入中間的反應核心
> → 最後點題

拆解成準則：
1. **開場給狀態，不給 logo** —— 先讓觀眾看到「一個東西在那裡」，不要一開始就打標題
2. **鏡頭要動** —— 推軌、拉遠、環繞、跟隨。靜止畫面之間的硬切不算鏡頭語言
3. **中段給資訊** —— 那個東西是什麼、為什麼會動、跟誰有關
4. **最後才點題** —— 標題與 logo 放結尾，不是開頭
5. **音畫節奏** —— 發條聲、齒輪咬合、開門聲這類實體音效，比配樂更有存在感

做影片前先寫**分鏡**（每一鏡：畫面、鏡頭運動、秒數、聲音），寫完貼到頻道讓 Kevin 看過再產。
⛔ 不要直接產一支完整影片給他看 —— 分鏡便宜、影片貴，錯了重做的成本差十倍。

## 素材來源的優先序

1. **實機錄影** `/root/gameplay_capture.sh` —— 真畫面最有說服力，且免費
2. **現有截圖** `screenshots/`（51 張）
3. **主視覺** `branding/key_visual_main.png`
4. **產圖** `gen_media.py`（一定帶 `--ref` 主視覺）
5. Veo 產影片 —— 貴，**一律先問 Kevin**

## 檔案放哪

- 品牌素材（長期要用的）→ `branding/`，進版控
- 一次性草稿與候選 → `/tmp`，不要進 repo
- 產出後用 `python3 /root/discord_file.py "<說明>" <檔案>` 傳到頻道給 Kevin 看

## 靜圖怎麼做出鏡頭運動（不用 AI 影片、不用花錢）

上一版之所以變成投影片，是因為把圖直接串起來。**靜圖也能做出運鏡**，用 ffmpeg 就夠：

**慢推（Push-In）**：`zoompan` 每格微幅放大，`d` 控制時長

    ffmpeg -loop 1 -i shot1.png -vf "zoompan=z='min(zoom+0.0012,1.35)':d=90:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,fps=30" -t 3 -c:v libx264 -pix_fmt yuv420p shot1.mp4

**橫移／跟隨**：`crop` 的 x 隨時間位移

    ffmpeg -loop 1 -i shot.png -vf "scale=2400:-1,crop=1920:1080:'(in_w-1920)*t/4':0,fps=30" -t 4 -c:v libx264 -pix_fmt yuv420p out.mp4

**弧形環繞的近似**：`zoompan` 的 x/y 同時隨 t 位移，再疊極輕微 `rotate`（0.5～1 度以內），
配合淺景深的原圖就有環繞感。

**視差（Parallax）**：背景與前景分兩張圖，各自用不同速度的 crop 位移再 `overlay` 疊起來。
Shot 3 的推門穿越就用這招（門扉前景快、雲海背景慢）。

**光線掃過**：疊一張半透明漸層 png，用 overlay 的 x 隨時間位移。

**接鏡**：鏡與鏡之間用 `xfade`（`transition=fade`，`duration` 0.2 秒以內）。
⛔ 不要用硬切串接一堆靜圖 —— 那就是投影片。

**音效**：實體音優先。沒有素材時**寧可留白也不要塞罐頭配樂**。
混音用 `ffmpeg -i video.mp4 -i sfx.wav -filter_complex amix`。

## 產片流程（一定照這個順序）

1. 寫分鏡 → 貼 Discord 給 Kevin 看 → **等他確認**
2. **一次只做一鏡**，做完用 `discord_file.py` 傳給他看
3. 那一鏡過了才做下一鏡
4. 全部過了才合成完整片並配音

⛔ 不要一次做完整支再給他看 —— 錯了重做的成本差十倍，這是被退過一次的教訓。

## ⭐ 主角角色設定（產任何有兔子的圖都必須照這個）

角色參考圖：`/opt/side/bravesoul-game/branding/char_rabbit.png`（從主視覺裁出的乾淨單體）

**主角是一隻黃銅機械發條兔，不是絨毛玩偶。** 這點被搞錯過一次，產出來變成寫實攝影感的
灰白毛料玩偶，跟主視覺完全不同世界。

| 部位 | 設定 |
|------|------|
| **材質** | 斑駁的**黃銅與米白金屬機殼**，表面有鏽斑、磨損與鉚釘 ⛔ 不是絨毛、不是布料、不是毛料 |
| **胸口** | 發光的**青綠色圓形核心**（發條之心），是全身唯一的強光源 |
| **眼睛** | 大顆**青綠／藍綠玻璃眼**，有明顯高光，帶一點天真 |
| **耳朵** | **一律立耳（挺直向上）**，內耳是**陶土紅／鏽紅**。⛔ 不畫垂耳／lop ear —— 這是金屬機械結構，耳朵不會軟垂 |
| **關節** | 黃銅機械關節，看得出是可動玩具 |
| **配件** | 身上或身側有**黃銅發條鑰匙**；可持齒輪短劍 |
| **比例** | 約 3 頭身，圓潤但不軟爛 |

**畫風**：**手繪插畫**、粗描邊、有筆觸與紙質感，暖金 × 青綠的高對比。
⛔ 不是 3D 渲染、不是攝影寫實、不是柔焦廣告片質感。

## 產圖時怎麼寫提示詞才不會跑掉

`--ref` 只能提供弱引導，**光靠它不夠** —— 提示詞裡沒寫到的材質與畫風，模型會自己發明。
所以每次都要**同時**做兩件事：

1. `--ref /opt/side/bravesoul-game/branding/char_rabbit.png`（有兔子的鏡頭）
   或 `--ref .../key_visual_main.png`（場景與世界觀的鏡頭）
2. **提示詞裡明寫材質與畫風**：`brass and off-white metal clockwork rabbit automaton,
   weathered patina and rivets, glowing teal core in chest, large teal glass eyes,
   rust-red inner ears, hand-painted illustration with thick outlines, warm gold and
   teal palette` —— 並明確排除：`not plush, not fabric, not photorealistic, not 3D render`

⛔ **提示詞裡出現「毛絨／絨毛／plush／fluffy」就是錯的**，那是舊的糖果色 Q 版設定，已作廢。

## 產圖比例（2026-09-04 加）

`gen_media.py image` 新增 `--aspect`。**不給就會跟著 `--ref` 參考圖的比例跑**——拿橫式主視覺當 ref 就會產出橫圖，混在直式影片裡就穿幫。

- 行銷短影音（FB Reels / Shorts）每一鏡：`--aspect 9:16`
- 粉專貼文主圖：`--aspect 4:5`（動態牆佔版面最大）
- 封面／橫幅：`--aspect 16:9`

⛔ 同一支影片裡的所有分鏡必須同比例，產完用 `ffprobe` 對一次寬高再進剪接。

## 品牌字標（2026-09-04 定案）

Kevin 選定 **B 繪本手繪風**（跟遊戲美術同一套筆觸）。emblem＝心形鎖孔插著發條鑰匙。

| 檔案 | 用途 |
|---|---|
| `branding/logo_cn.png` | 中文主字標《發條之心》＋下方 Clockwork Heart |
| `branding/logo_en.png` | 英文字標 CLOCKWORK HEART（國際版） |
| `branding/logo_cn_black.png` / `logo_en_black.png` | 底色已壓成純黑，疊在黑底上用 |
| `branding/title_plate.png` | 點題卡底板（純黑＋右下兔子剪影＋微光） |

⛔ **不要每次重新產字標**。字標是固定資產，要換是品牌決策，要先問 Kevin。

### 合成點題卡的兩個坑（踩過）

1. **YUV 下做 blend 會整張變紫**。`blend` 之前兩路都要 `format=gbrp`，出來再 `format=rgb24`。
2. **`screen` 疊合不會讓深色底消失**，screen 是提亮：深藍底疊黑底還是深藍，會看到方框。
   要先用 `colorlevels=rimin=0.09:gimin=0.12:bimin=0.19` 把字標背景壓到純黑，再 screen。

### 中文字型

pdc-hermes 已裝 `fonts-noto-cjk`，標題可用
`/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc`。
**標語一律用真字型 drawtext 排，不要交給影像模型產**——字數一多就會出錯字。
（四個字的《發條之心》模型產得對，但那是運氣，不是保證。）
