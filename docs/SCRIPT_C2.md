# SCRIPT · C2 白霧村「霧與真」（3m 完整域）

> **轉譯說明**：依 PRODUCT_LOCK_0.20 §2.2 轉譯，2026-09-07。  
> 3m 第二可玩域；精做 **白霧看破**；必做 **N8 延遲的信**（中段情感錨，不可刪）。  
> **敘事底色：** 世界大鐘停擺之後；主角是剛被上弦喚醒的發條兔，不是預言選民。舊鑰的信＝「還有人在等」，不是天命。  
> **用語對齊**：C0 的閣樓／舊鑰／鑰繩；C1 的「白霧那側」；CANON 的停擺、黑鏽、工坊守衛泰坦·白霧仙狐。  
> **用途**：對白、舞台指示、flag、戰鬥插入點。  
> **格式**：`角色：台詞`；`【系統】`；`（舞台）`；`→ flag`

---

## 目標

| 完成 | 內容 |
|------|------|
| 機制 | 白霧：幻影／僅破綻可傷本體 |
| 情感 | N8 信 |
| 解鎖 | 霧影外觀契機；往塔路（經 C3 蒙太奇） |
| flag | `boss.white_fog_cleared` |

---

## 節點（簡）

```
[白霧村入口]——[客棧／營火 ← N8]——[霧廊訓練]
        |
   [幻廊地城]——[白霧戰場]
```

---

## C2-S1 進村

**霧隱**：霧裡真假同色。發條最鬆的那掛？……眼睛，借我用用。  
**霧隱**：先住一晚。發條將盡還趕路的——尤其是來「看一眼」的——會先斷在自己心裡。

→ 開放客棧  

---

## C2-S2 · **N8 延遲的信**（主線必觸）

（第一次進客棧房間／點營火，強制或高優先。）

（若持鑰繩 `item.wheat_stalk` 或碎鑰繩 `item.wheat_stalk_broken`：）  
**【系統】** 鑰繩／行囊縫裡……有一張薄紙。字跡被捏過。

（若無鑰繩：星讀或霧隱交給你。）  
**霧隱／星讀**：有人託人一站一站轉來。慢了。

### 信（全屏或日誌大字，可截圖）

> 我還在。  
> 不是因為預言，  
> 是因為你還沒回來。  
> ——舊鑰

**主角內心**：……還在。那我就還能走。

→ `flag.c2_wheat_letter = true`  
→ 日誌：「舊鑰的字。比預言輕，比劍重。」  
→ **此段不可完全跳過正文**（可加速，需確認）

---

## C2-S3 霧廊教學

**霧隱**：打影子，影子笑你。看**破綻**——刃抬起的那一幀，才是真的。

（小戰鬥：2 幻影 + 1 真；打錯彈飛輕傷。）

---

## C2-S4 白霧戰

### 開場
**白霧**：嘻嘻～真的假的，你分得清嗎？

### 機制（3m 精做）
- 場上 1 本體 + 多幻影  
- 僅「真實破綻幀」（閃白邊／動作不同）可傷本體  
- 打錯幻影：反噬或霧偷笑 SE（clip 向）  
- 可保留部位或階段台詞  

### 勝利
**白霧**：看破了呀……剛上弦的也會看破？真沒意思。  
**白霧**：霧散了，路就在你眼前——回去跟堡壘說，或繼續走。隨便你。  
（可短記憶節 6m 再加長）

→ `boss.white_fog_cleared = true`  
→ 解鎖霧影外觀契機  

---

## C2-S5 出村

**霧隱**：塔在中央。中間還有山的鐘……你若趕路，聽一聲也夠。  
**霧隱**：堡壘問起來，就說：霧裡的東西，你分得清了。  
→ 接 **C3 蒙太奇**（非完整域）

---

## C3 蒙太奇（趕路捷徑）／正本見 [SCRIPT_C3.md](SCRIPT_C3.md)

**【旁白】**  
山門。茶煙。一頭熊貓不發一掌，只問：你，為何而戰？  
你答了自己的名字與——還有人在等。不是預言選民。  
鐘響。道，暫記一筆。路，繼續向塔。

→ 完整道場：`SCRIPT_C3.md`  
→ `flag.c3_montage_done` / `boss.abo_cleared`  

---

## Flag 總表（C2）

| flag | 含義 |
|------|------|
| `c2_wheat_letter` | N8 延遲的信已讀（舊鑰；不可跳過正文） |
| `boss.white_fog_cleared` | 白霧勝／霧散 |
| `c3_montage_done` | C3 趕路蒙太奇（本檔捷徑；正本見 SCRIPT_C3） |
| `boss.abo_cleared` | 阿波（蒙太奇捷徑旗；正本見 SCRIPT_C3） |

---

## 六語系專有名詞對照表（Localization Lexicon）

| 專有名詞分類 | 繁體中文 | 簡體中文 | 英文（EN） | 西班牙文（ES） | 日文（JA） | 韓文（KO） |
|:---|:---|:---|:---|:---|:---|:---|
| **章節名** | 霧與真 | 雾与真 | Fog and Truth | Niebla y Verdad | 霧と真 | 안개와 진실 |
| **可玩域** | 白霧村 | 白雾村 | White Fog Village | Aldea de la Niebla Blanca | 白霧の村 | 백무 마을 |
| **核心地標** | 世界大鐘 | 世界大钟 | Grand Clockwork | Gran Reloj Mundial | 世界の大時計 | 세계 대시계 |
| **世界狀態** | 停擺 | 停摆 | Stasis | Inactividad | 停止 | 정지 |
| **旗艦 BOSS** | 白霧 | 白雾 | White Fog | Niebla Blanca | 白霧 | 백무 |
| **BOSS 全稱** | 守衛泰坦·白霧 | 守卫泰坦·白雾 | Titan Overseer White Fog | Titán Guardián Niebla Blanca | 守護タイタン・白霧 | 수호 타이탄·백무 |
| **種族稱謂** | 白霧仙狐 | 白雾仙狐 | Fox Titan White Fog | Zorro Titán Niebla Blanca | 白霧の仙狐 | 백무 선호 |
| **核心 NPC** | 霧隱 | 雾隐 | Mistveil | Velo de Niebla | ミストベール | 미스트베일 |
| **核心 NPC** | 星讀 | 星读 | Star-Reader | Lector Estelar | 星読み | 성독 |
| **情感夥伴** | 舊鑰 | 旧钥 | Oldkey | Llavevieja | オールドキー | 올드키 |
| **牽掛信物** | 鑰繩 | 钥绳 | Key Cord | Cordón de Llave | 鍵ひも | 열쇠끈 |
| **紀念信物** | 碎鑰繩 | 碎钥绳 | Broken Key Cord | Cordón de Llave Roto | 折れた鍵ひも | 부러진 열쇠끈 |
| **情感錨** | 延遲的信 | 延迟的信 | Delayed Letter | Carta Retrasada | 遅れた手紙 | 늦어진 편지 |
| **教學節點** | 霧廊 | 雾廊 | Fog Corridor | Corredor de Niebla | 霧の回廊 | 안개 회랑 |
| **地城節點** | 幻廊 | 幻廊 | Illusion Gallery | Galería de Ilusiones | 幻の回廊 | 환상 회랑 |
| **休息節點** | 客棧 | 客栈 | Inn | Posada | 宿場 | 여관 |
| **休息節點** | 營火 | 营火 | Campfire | Fogata | 焚き火 | 모닥불 |
| **戰鬥節點** | 白霧戰場 | 白雾战场 | White Fog Battlefield | Campo de Niebla Blanca | 白霧の戦場 | 백무 전장 |
| **機制** | 看破 | 看破 | See-Through | Traspasar | 見破り | 간파 |
| **機制** | 破綻 | 破绽 | True Tell | Gesto Real | 隙 | 빈틈 |
| **機制** | 幻影 | 幻影 | Phantom | Fantasma | 幻影 | 환영 |
| **機制** | 本體 | 本体 | True Body | Cuerpo Verdadero | 本体 | 본체 |
| **外觀** | 霧影 | 雾影 | Fogveil Form | Forma de Niebla | 霧影 | 무영 |
| **下域提示** | 山的鐘 | 山的钟 | Mountain Bell | Campana de la Montaña | 山の鐘 | 산의 종 |
