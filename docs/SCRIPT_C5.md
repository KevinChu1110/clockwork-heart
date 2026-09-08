# SCRIPT · C5 石拳海岸「岸上最後一擊」

> **轉譯說明**：依 PRODUCT_LOCK_0.20 §2.2 轉譯，2026-09-07。  
> 完整可玩域。精做 **石拳對撞**。  
> **敘事底色：** 世界大鐘停擺之後；主角是剛被上弦喚醒的發條兔，發條最鬆，不是預言選民。岸上不認頭銜，認你敢不敢迎上去。  
> **用語對齊**：C0 的舊鑰／鑰繩；C1 的堡壘；C2 的白霧那側；C3-S4 的東岸有石（石拳）；C4 西林出山往海岸／塔；CANON 禁令三／四與 5.3 工坊守衛泰坦·石拳巨豕。地圖結構見 [CHAPTER_C4_C5.md](CHAPTER_C4_C5.md)，本檔口吻用地名石拳海岸（接 C3 東岸、C4 海岸），不另起一套，不沿用舊 IP「維京」。  
> **用途**：對白、舞台指示、flag、戰鬥插入點。  
> **格式**：`角色：台詞`；`【系統】`；`（舞台）`；`→ flag`

機制與地圖見 [CHAPTER_C4_C5.md](CHAPTER_C4_C5.md)。本檔只管口吻——不要發明第三套主題。

---

## 目標

| 完成 | 內容 |
|------|------|
| 機制 | 石拳：對撞剝岩甲；落岩按 J |
| 情感 | 力氣若沒有方向，只是浪打空岸 |
| 解鎖 | 炎心外觀；往塔 |
| flag | `c5_entered`、`boss.stonefist_cleared` |

---

## C5-S1 碼頭 · 潮吼

（舞台：石拳海岸碼頭。潮吼是守岸的發條偶，胸腔是空的號角盒，浪一拍就響。客從西林來。）

**旁白**：林盡是鹽。發條最鬆的那個，被浪先打濕。  
**潮吼**：剛上弦的？岸上不比腕力——比你敢不敢迎上去。  
**潮吼**：石拳不是為了砸碎你。它忘了力氣該往哪放。

**【系統】** 海岸可走。石拳崖在東。

→ `c5_entered`

---

## C5-S2 符文石

**符文石**：力為護，不為炫。  
**內心**：頭銜砸不開岸。迎上去。

---

## C5-S3 石拳崖

（舞台：石拳崖。石拳是工坊守衛泰坦·巨豕，岩甲層層，對撞才剝得開。防衛協議溢流，力氣沒了方向。）

**石拳**：……把發條最鬆的送來了？還站著？那就接下這一拳——  
**石拳**：力氣該砸向誰？頭銜砸不開岸。

（戰鬥：對撞＋落岩）

### 勝利
**石拳**：哈哈哈！站到最後的是你！發條最鬆的，卻迎上去。  
**石拳**：力氣是用來護岸的。回報時別寫成預言選民。  
**潮吼**：好！去塔吧。堡壘若問，就說：你把力氣對準了。

→ `boss.stonefist_cleared`

---

## 不做偏

- 不把石拳改成認預言／發頭銜。  
- 不把對撞改成問答破防。  
- 兔子 chibi 保留；台詞不叫兔子觀光。  

---

## Flag 總表（C5）

| flag | 含義 |
|------|------|
| `c5_entered` | 進石拳海岸碼頭 |
| `boss.stonefist_cleared` | 石拳勝／把力氣對準了 |

---

## 六語系專有名詞對照表（Localization Lexicon）

| 專有名詞分類 | 繁體中文 | 簡體中文 | 英文（EN） | 西班牙文（ES） | 日文（JA） | 韓文（KO） |
|:---|:---|:---|:---|:---|:---|:---|
| **章節名** | 岸上最後一擊 | 岸上最后一击 | Last Blow on the Shore | El Último Golpe en la Orilla | 岸の最後の一撃 | 해안의 마지막 일격 |
| **可玩域** | 石拳海岸 | 石拳海岸 | Stonefist Coast | Costa del Puño de Piedra | 石拳の海岸 | 석권 해안 |
| **上域提示** | 東岸 | 东岸 | East Shore | Costa Este | 東の岸 | 동안 |
| **上域提示** | 西林 | 西林 | West Woods | Bosque del Oeste | 西の林 | 서림 |
| **核心地標** | 世界大鐘 | 世界大钟 | Grand Clockwork | Gran Reloj Mundial | 世界の大時計 | 세계 대시계 |
| **世界狀態** | 停擺 | 停摆 | Stasis | Inactividad | 停止 | 정지 |
| **旗艦 BOSS** | 石拳 | 石拳 | Stonefist | Puño de Piedra | 石拳 | 석권 |
| **BOSS 全稱** | 守衛泰坦·石拳 | 守卫泰坦·石拳 | Titan Overseer Stonefist | Titán Guardián Puño de Piedra | 守護タイタン・石拳 | 수호 타이탄·석권 |
| **種族稱謂** | 石拳巨豕 | 石拳巨豕 | Boar Titan Stonefist | Jabalí Titán Puño de Piedra | 石拳の巨猪 | 석권 거돈 |
| **核心 NPC** | 潮吼 | 潮吼 | Tidehowl | Rugido de Marea | 潮吼 | 조후 |
| **情感夥伴** | 舊鑰 | 旧钥 | Oldkey | Llavevieja | オールドキー | 올드키 |
| **牽掛信物** | 鑰繩 | 钥绳 | Key Cord | Cordón de Llave | 鍵ひも | 열쇠끈 |
| **碼頭節點** | 碼頭 | 码头 | Dock | Muelle | 波止場 | 부두 |
| **碑節點** | 符文石 | 符文石 | Inscribed Stone | Piedra Inscrita | 銘石 | 새긴 돌 |
| **戰鬥節點** | 石拳崖 | 石拳崖 | Stonefist Cliff | Acantilado del Puño de Piedra | 石拳の崖 | 석권 절벽 |
| **機制** | 對撞 | 对撞 | Clash | Choque | ぶつかり | 정면충돌 |
| **機制** | 岩甲 | 岩甲 | Rock Armor | Armadura de Roca | 岩の装甲 | 바위 갑옷 |
| **機制** | 落岩 | 落岩 | Falling Rock | Roca que Cae | 落石 | 낙석 |
| **情感錨** | 浪打空岸 | 浪打空岸 | Waves on Empty Shore | Olas en Orilla Vacía | 空の岸を打つ波 | 빈 해안을 치는 파도 |
| **認可** | 力氣對準了 | 力气对准了 | Force Aimed True | Fuerza Bien Encaminada | 力の向きが定まった | 힘이 방향을 잡았다 |
| **外觀** | 炎心 | 炎心 | Ember | Ascua | 炎心 | 염심 |
| **下域提示** | 塔 | 塔 | Tower | Torre | 塔 | 탑 |
| **上域提示** | 堡壘 | 堡垒 | Keep | Fortaleza | 砦 | 요새 |
