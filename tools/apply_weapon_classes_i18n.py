#!/usr/bin/env python3
import json
import os

BASE_DIR = "/opt/side/bravesoul-game"
CONTENT_I18N_DIR = os.path.join(BASE_DIR, "game/data/i18n/content")

LOCALES = ["zh_TW", "zh_CN", "en", "ja", "ko", "es"]

# 12 Classes Data in 6 Languages
WEAPON_CLASSES_I18N = {
    "sword": {
        "zh_TW": {
            "name": "劍",
            "title": "騎士·劍",
            "tagline": "平衡的刃",
            "play": "近身中距離，普攻和怒氣技輪著來。同職也可玩槍。",
            "pros": ["攻防平均，最好上手", "出招節奏穩，怒氣接得順", "裝備選擇最多，新手友善"],
            "cons": ["爆發打不過火槍和法", "硬度比不上鎚和斧", "打不到遠的"]
        },
        "zh_CN": {
            "name": "剑",
            "title": "骑士·剑",
            "tagline": "平衡之刃",
            "play": "近身中距离，普攻与怒气技交替施展。同职业亦可使用长枪。",
            "pros": ["攻防均衡，极易上手", "出招节奏稳定，怒气衔接顺畅", "装备选择最广，新手友好"],
            "cons": ["爆发不及火枪与法杖", "坚固度不及重锤与战斧", "无法触及远距离敌人"]
        },
        "en": {
            "name": "Sword",
            "title": "Knight · Sword",
            "tagline": "A Balanced Edge",
            "play": "Close to mid range, alternating normal strikes and rage skills. The spear is also playable in this class.",
            "pros": ["Balanced offense and defense, easiest to master", "Steady rhythm, seamless rage skill transitions", "Widest gear options, beginner-friendly"],
            "cons": ["Burst falls behind guns and spells", "Less sturdy than hammer and axe", "Cannot hit distant foes"]
        },
        "ja": {
            "name": "剣",
            "title": "騎士・剣",
            "tagline": "均衡の刃",
            "play": "近距離から中距離で、通常攻撃と怒り技を交互に繰り出す。同職で槍も扱える。",
            "pros": ["攻守のバランスが良く扱いやすい", "技のリズムが安定し怒り技が繋がりやすい", "装備の選択肢が最も多く初心者に優しい"],
            "cons": ["瞬間火力は銃や魔法に及ばない", "耐久力は槌や斧に劣る", "遠くの敵には届かない"]
        },
        "ko": {
            "name": "검",
            "title": "기사·검",
            "tagline": "균형의 날",
            "play": "근거리와 중거리에서 기본 공격과 분노 기술을 번갈아 사용합니다. 같은 직업으로 창도 선택할 수 있습니다.",
            "pros": ["공방 균형이 뛰어나 가장 다루기 쉬움", "공격 리듬이 안정적이며 분노 연계가 매끄러움", "장비 선택의 폭이 가장 넓어 초보자 친화적"],
            "cons": ["순간 화력은 화승총과 마법에 미치지 못함", "내구력은 망치와 도끼보다 부족함", "원거리의 적을 타격할 수 없음"]
        },
        "es": {
            "name": "Espada",
            "title": "Caballero · Espada",
            "tagline": "El Filo Equilibrado",
            "play": "Distancia corta a media, alternando ataques básicos y habilidades de furia. Esta clase también puede usar lanza.",
            "pros": ["Ataque y defensa equilibrados, el más fácil de dominar", "Ritmo estable, encadena furia fluidamente", "Mayor variedad de equipo, ideal para principiantes"],
            "cons": ["Ráfaga inferior a las armas de fuego y magia", "Menor solidez que el martillo y hacha", "No alcanza objetivos lejanos"]
        }
    },
    "spear": {
        "zh_TW": {
            "name": "長槍",
            "title": "騎士·槍",
            "tagline": "比劍更長的一步",
            "play": "卡住距離，等他進來就迎上去。同職也可玩劍。",
            "pros": ["中距離最吃香", "對衝和迎擊有額外好處", "場面控得住"],
            "cons": ["地形一窄就難施展", "轉身慢", "暴擊偏低"]
        },
        "zh_CN": {
            "name": "长枪",
            "title": "骑士·枪",
            "tagline": "胜于利剑的一步之遥",
            "play": "把控距离，待敌逼近即刻迎击。同职业亦可使用利剑。",
            "pros": ["中距离优势显著", "冲撞与迎击具备额外收益", "掌控战场局势能力极佳"],
            "cons": ["狭窄地形难以施展", "转身迟缓", "暴击率偏低"]
        },
        "en": {
            "name": "Spear",
            "title": "Knight · Spear",
            "tagline": "A Step Beyond the Sword",
            "play": "Hold spacing and counter when they push in. The sword is also playable in this class.",
            "pros": ["Dominant at mid-range", "Bonus advantages on clash and counter", "Keeps the field under control"],
            "cons": ["Struggles in narrow terrain", "Slow turning", "Lower crit rate"]
        },
        "ja": {
            "name": "長槍",
            "title": "騎士・槍",
            "tagline": "剣より一歩先へ",
            "play": "間合いを保ち、踏み込んできた敵を迎え撃つ。同職で剣も扱える。",
            "pros": ["中距離戦で最も有利", "突進や迎撃で追加の恩恵がある", "戦場の状況を制御しやすい"],
            "cons": ["狭い地形では力を発揮しづらい", "旋回が遅い", "会心率がやや低い"]
        },
        "ko": {
            "name": "창",
            "title": "기사·창",
            "tagline": "검보다 한 걸음 더 먼 곳",
            "play": "거리를 유지하다가 파고드는 적을 요격합니다. 같은 직업으로 검도 선택할 수 있습니다.",
            "pros": ["중거리 교전에서 가장 우세함", "돌격과 반격 시 추가 이점이 있음", "전장 제어력이 뛰어남"],
            "cons": ["지형이 좁으면 기술을 펼치기 어려움", "방향 전환이 느림", "치명타율이 다소 낮음"]
        },
        "es": {
            "name": "Lanza",
            "title": "Caballero · Lanza",
            "tagline": "Un Paso Más Allá de la Espada",
            "play": "Mantén la distancia y contraataca cuando el enemigo avance. Esta clase también puede usar espada.",
            "pros": ["Gran ventaja a media distancia", "Beneficios adicionales en choques y contraataques", "Excelente control del campo de batalla"],
            "cons": ["Difícil de maniobrar en espacios estrechos", "Giro lento", "Tasa de crítico algo baja"]
        }
    },
    "axe": {
        "zh_TW": {
            "name": "斧",
            "title": "維京·斧",
            "tagline": "一擊要有重量",
            "play": "抓重擊的空檔下手。同職也可玩鎚。",
            "pros": ["單下最痛", "對重甲和石拳很有效", "一斧下去對手會怕"],
            "cons": ["出手慢", "揮空了很吃虧", "不靈活"]
        },
        "zh_CN": {
            "name": "斧",
            "title": "维京·斧",
            "tagline": "一击必有千钧重",
            "play": "伺机把握重击间隙猛攻。同职业亦可使用重锤。",
            "pros": ["单次伤害冠绝群雄", "克制重甲与坚硬石躯效果拔群", "势大力沉令对手胆寒"],
            "cons": ["出招动作较慢", "挥空极易露出破绽", "身法欠缺灵动"]
        },
        "en": {
            "name": "Axe",
            "title": "Viking · Axe",
            "tagline": "Every Blow Must Have Weight",
            "play": "Exploit openings with heavy strikes. The hammer is also playable in this class.",
            "pros": ["Highest single-hit damage", "Highly effective against heavy armor and stone fists", "A single cleave strikes fear into foes"],
            "cons": ["Slow swings", "Heavy penalty on misses", "Lacks agility"]
        },
        "ja": {
            "name": "斧",
            "title": "ヴァイキング・斧",
            "tagline": "一撃に重みを",
            "play": "重撃の隙を突いて叩き込む。同職で槌も扱える。",
            "pros": ["単発の威力が最も高い", "重装甲や石拳に絶大な効果", "一振りで相手を威圧する"],
            "cons": ["攻撃の発生が遅い", "空振りした時の隙が大きい", "小回りが利かない"]
        },
        "ko": {
            "name": "도끼",
            "title": "바이킹·도끼",
            "tagline": "묵직한 한 방",
            "play": "강타의 빈틈을 노려 일격을 가합니다. 같은 직업으로 망치도 선택할 수 있습니다.",
            "pros": ["단일 타격 피해량이 가장 강력함", "중장갑과 암석 주먹에 매우 효과적", "한 번의 일격으로 적을 위압함"],
            "cons": ["공격 속도가 느림", "빗맞혔을 때의 위험이 큼", "기동성이 떨어짐"]
        },
        "es": {
            "name": "Hacha",
            "title": "Vikingo · Hacha",
            "tagline": "Cada Golpe Debe Pesar",
            "play": "Aprovecha las aberturas con golpes pesados. Esta clase también puede usar martillo.",
            "pros": ["El mayor daño de un solo impacto", "Muy eficaz contra armaduras pesadas y puños de piedra", "Un solo hachazo intimida al rival"],
            "cons": ["Ataque lento", "Gran desventaja si falla el golpe", "Falta de agilidad"]
        }
    },
    "hammer": {
        "zh_TW": {
            "name": "鎚",
            "title": "維京·鎚",
            "tagline": "站到最後",
            "play": "站著硬扛，耗到對手先倒。同職也可玩斧。",
            "pros": ["血和防禦最厚", "鍛造成功率暗中高一點", "硬吃招式也不太會死"],
            "cons": ["傷害是最低的幾種之一", "清雜魚很慢", "追不上也逃不掉"]
        },
        "zh_CN": {
            "name": "锤",
            "title": "维京·锤",
            "tagline": "屹立至最后一刻",
            "play": "正面硬抗耐受打击，静待对手力竭倒下。同职业亦可使用战斧。",
            "pros": ["血量与防御极为厚实", "锻造成功几率暗藏加成", "硬接强力招式亦不至殒命"],
            "cons": ["伤害位列最低梯队之一", "清理小怪效率低下", "追击与退避皆受限制"]
        },
        "en": {
            "name": "Hammer",
            "title": "Viking · Hammer",
            "tagline": "Last One Standing",
            "play": "Stand firm, soak damage, and outlast the foe. The axe is also playable in this class.",
            "pros": ["Thickest health and defense", "Slightly boosted forge success chance", "Survives heavy strikes without faltering"],
            "cons": ["Lowest damage tier", "Slow at clearing small mobs", "Cannot chase or escape easily"]
        },
        "ja": {
            "name": "槌",
            "title": "ヴァイキング・槌",
            "tagline": "最後まで立ち続ける者",
            "play": "直撃を耐え忍び、相手が倒れるまで消耗させる。同職で斧も扱える。",
            "pros": ["HPと防御力が最も高い", "鍛造の成功率が密かに少し高い", "強烈な一撃を受けても耐え抜く"],
            "cons": ["ダメージが最低クラス", "雑魚の殲滅に時間がかかる", "追撃も離脱も難しい"]
        },
        "ko": {
            "name": "망치",
            "title": "바이킹·망치",
            "tagline": "끝까지 버티는 자",
            "play": "버텨내며 적이 먼저 쓰러질 때까지 소모전을 벌입니다. 같은 직업으로 도끼도 선택할 수 있습니다.",
            "pros": ["생명력과 방어력이 가장 높음", "단조 성공 확률이 은밀히 더 높음", "강력한 공격을 맞아도 쉽게 쓰러지지 않음"],
            "cons": ["피해량이 가장 낮은 축에 속함", "일반 몬스터 처리가 느림", "추격과 탈출이 모두 어려움"]
        },
        "es": {
            "name": "Martillo",
            "title": "Vikingo · Martillo",
            "tagline": "El Último en Pie",
            "play": "Resiste a pie firme hasta desgastar al adversario. Esta clase también puede usar hacha.",
            "pros": ["Mayor vitalidad y defensa", "Ligera bonificación oculta al forjar", "Soporta golpes demoledores sin caer"],
            "cons": ["Uno de los daños más bajos", "Lento para eliminar enemigos menores", "Difícil perseguir o escapar"]
        }
    },
    "dagger": {
        "zh_TW": {
            "name": "匕首",
            "title": "忍者·匕",
            "tagline": "藏在袖裡的殺意",
            "play": "貼上去急刺連段。同職也可玩鏢。",
            "pros": ["貼身爆發高", "森羅連刺節奏兇", "暴擊好"],
            "cons": ["身板薄", "被風箏就難", "容錯低"]
        },
        "zh_CN": {
            "name": "匕首",
            "title": "忍者·匕",
            "tagline": "藏匿袖中的凛冽杀意",
            "play": "近身贴战疾刺连段。同职业亦可使用飞镖。",
            "pros": ["贴身爆发极高", "森罗连刺攻势凶猛", "暴击属性极佳"],
            "cons": ["身躯脆弱抗性薄弱", "遭受风筝牵制难以应对", "容错率较低"]
        },
        "en": {
            "name": "Dagger",
            "title": "Ninja · Dagger",
            "tagline": "Killing Intent Hidden in the Sleeve",
            "play": "Get in close with rapid stabbing combos. Darts are also playable in this class.",
            "pros": ["Fierce point-blank burst", "Relentless multi-stab rhythm", "High critical strikes"],
            "cons": ["Fragile frame", "Vulnerable to kiting", "Low room for error"]
        },
        "ja": {
            "name": "短剣",
            "title": "忍者・短剣",
            "tagline": "袖に秘めた殺意",
            "play": "間合いを詰めて素早く連続急所突き。同職で鏢も扱える。",
            "pros": ["近接での瞬間火力が高い", "怒涛の連続刺突が鋭い", "会心性能に優れる"],
            "cons": ["打たれ弱い", "遠距離から翻弄されると厳しい", "ミスへの許容度が低い"]
        },
        "ko": {
            "name": "단검",
            "title": "닌자·단검",
            "tagline": "소매 속에 감춘 살의",
            "play": "바짝 붙어 빠른 연속 찌르기를 펼칩니다. 같은 직업으로 표창도 선택할 수 있습니다.",
            "pros": ["초근접 순간 폭딜이 뛰어남", "맹렬한 연속 찌르기 리듬", "치명타 성능이 우수함"],
            "cons": ["방어력이 취약함", "거리 유지를 당하면 고전함", "실수에 대한 허용치가 낮음"]
        },
        "es": {
            "name": "Daga",
            "title": "Ninja · Daga",
            "tagline": "Instinto Asesino Bajo la Manga",
            "play": "Acércate rápidamente con combos de estocadas veloces. Esta clase también puede usar dardos.",
            "pros": ["Gran ráfaga a quemarropa", "Rápido ritmo de estocadas continuas", "Excelente crítico"],
            "cons": ["Constitución frágil", "Vulnerable al hostigamiento a distancia", "Bajo margen de error"]
        }
    },
    "dart": {
        "zh_TW": {
            "name": "鏢",
            "title": "忍者·鏢",
            "tagline": "真假同色的一手",
            "play": "高速真假鏢影。同職也可玩匕首。",
            "pros": ["連擊速度快", "很吃白霧那種看破的打法", "暴擊和命中都好"],
            "cons": ["單下低", "撐不了幾下", "很看走位"]
        },
        "zh_CN": {
            "name": "镖",
            "title": "忍者·镖",
            "tagline": "虚实交织的一掷",
            "play": "高速穿梭虚实镖影。同职业亦可使用匕首。",
            "pros": ["连击频率迅捷", "高度契合看破战法的敏捷风格", "暴击与命中俱佳"],
            "cons": ["单次伤害较低", "难以持久承受重击", "极其依赖走位操作"]
        },
        "en": {
            "name": "Dart",
            "title": "Ninja · Dart",
            "tagline": "A Feint and Strike as One",
            "play": "High-speed feints and dart volleys. Daggers are also playable in this class.",
            "pros": ["Rapid combo speed", "Synergizes with reading tells through white fog", "Great crit and accuracy"],
            "cons": ["Low single-hit damage", "Cannot take many hits", "Heavily reliant on footwork"]
        },
        "ja": {
            "name": "鏢",
            "title": "忍者・鏢",
            "tagline": "虚実一体の一投",
            "play": "高速の残像を交えた鏢の乱舞。同職で短剣も扱える。",
            "pros": ["連撃速度が速い", "白霧を見切る立ち回りと好相性", "会心と命中がともに優秀"],
            "cons": ["単発の威力が低い", "数回の直撃で窮地に陥る", "位置取りに大きく依存する"]
        },
        "ko": {
            "name": "표창",
            "title": "닌자·표창",
            "tagline": "허와 실을 담은 한 수",
            "play": "빠른 잔상과 함께 표창을 연사합니다. 같은 직업으로 단검도 선택할 수 있습니다.",
            "pros": ["연타 속도가 매우 빠름", "안개 속에서 적을 간파하는 스타일에 적합", "치명타와 명중률이 모두 우수함"],
            "cons": ["단일 타격 피해량이 낮음", "피격을 오래 버티지 못함", "위치 선정이 매우 중요함"]
        },
        "es": {
            "name": "Dardo",
            "title": "Ninja · Dardo",
            "tagline": "Finta y Golpe en un Solo Movimiento",
            "play": "Ráfagas veloces de dardos y sombras engañosas. Esta clase también puede usar dagas.",
            "pros": ["Velocidad de combo muy rápida", "Gran sinergia con el estilo de anticipación en la niebla", "Excelente crítico y puntería"],
            "cons": ["Bajo daño por impacto", "No resiste muchos golpes", "Depende mucho del posicionamiento"]
        }
    },
    "fist": {
        "zh_TW": {
            "name": "拳",
            "title": "武鬥·拳",
            "tagline": "破勢在勤",
            "play": "貼上去連打。同職也可玩爪。",
            "pros": ["出手快，架勢散得快", "對付道場阿波特別順", "跟危急回血的招很搭"],
            "cons": ["單下不痛", "武器傷害養得慢", "打不到遠的"]
        },
        "zh_CN": {
            "name": "拳",
            "title": "武斗·拳",
            "tagline": "勤能破千般架势",
            "play": "近身紧逼连续搏击。同职业亦可使用利爪。",
            "pros": ["出招迅捷破势极快", "应对道场阿波极为顺手", "高度契合濒危回复招式"],
            "cons": ["单拳伤害偏软", "武器伤害成长较慢", "无法触及远距离敌人"]
        },
        "en": {
            "name": "Fist",
            "title": "Monk · Fist",
            "tagline": "Diligence Breaks Any Stance",
            "play": "Close in for relentless flurry strikes. Claws are also playable in this class.",
            "pros": ["Fast attacks, breaks guard rapidly", "Smooth match against Abo in the dojo", "Pairs well with crisis healing skills"],
            "cons": ["Low single-punch damage", "Slow weapon damage scaling", "Cannot reach distant targets"]
        },
        "ja": {
            "name": "拳",
            "title": "武闘・拳",
            "tagline": "連撃こそが崩し",
            "play": "距離を詰めて連続で打ち込む。同職で爪も扱える。",
            "pros": ["攻撃の出が速く体勢を崩しやすい", "道場のアボ相手に立ち回りやすい", "危機時の回復技と好相性"],
            "cons": ["一撃の威力が低い", "武器攻撃力の伸びが遅い", "遠くの敵には届かない"]
        },
        "ko": {
            "name": "권",
            "title": "무투·권",
            "tagline": "꾸준함이 자세를 무너뜨린다",
            "play": "파고들어 연속 타격을 퍼붓습니다. 같은 직업으로 클로도 선택할 수 있습니다.",
            "pros": ["공격이 빠르고 적의 자세를 쉽게 무너뜨림", "도장 아보를 상대하기 수월함", "위기 회복 기술과 궁합이 좋음"],
            "cons": ["단일 타격 피해가 약함", "무기 공격력 성장이 더딤", "원거리의 적을 타격할 수 없음"]
        },
        "es": {
            "name": "Puño",
            "title": "Monje · Puño",
            "tagline": "La Constancia Rompe Toda Postura",
            "play": "Pégate al enemigo con ráfagas continuas de golpes. Esta clase también puede usar garras.",
            "pros": ["Ataques rápidos que rompen posturas fácilmente", "Muy efectivo contra Abo en el dojo", "Combina bien con curación en situaciones críticas"],
            "cons": ["Poco daño por puñetazo", "Escalado de daño de arma lento", "No alcanza a enemigos lejanos"]
        }
    },
    "claw": {
        "zh_TW": {
            "name": "爪",
            "title": "武鬥·爪",
            "tagline": "撕裂防線",
            "play": "爪痕連切。同職也可玩拳。",
            "pros": ["破勢快", "暴擊與連段兼顧", "虎撲節奏兇"],
            "cons": ["防禦薄", "距離短", "失誤代價高"]
        },
        "zh_CN": {
            "name": "爪",
            "title": "武斗·爪",
            "tagline": "撕裂坚固防线",
            "play": "利爪破空连续撕裂。同职业亦可使用拳套。",
            "pros": ["崩解防守极为迅捷", "兼顾暴击与连招爆发", "扑杀节奏凶悍"],
            "cons": ["防御薄弱", "攻击距离短小", "操作失误代价沉重"]
        },
        "en": {
            "name": "Claw",
            "title": "Monk · Claw",
            "tagline": "Tear the Frontline Open",
            "play": "Rapid claw slash combos. Fists are also playable in this class.",
            "pros": ["Fast guard break", "Combines crit with multi-hit burst", "Aggressive pounce rhythm"],
            "cons": ["Thin defense", "Short reach", "High cost on mistake"]
        },
        "ja": {
            "name": "爪",
            "title": "武闘・爪",
            "tagline": "防壁を切り裂く",
            "play": "鋭い爪痕を連続で刻み込む。同職で拳も扱える。",
            "pros": ["相手の体勢を瞬時に崩す", "会心と連続攻撃を両立", "猛虎のごとき鋭い攻め"],
            "cons": ["防御が薄い", "リーチが短い", "失敗時の代償が大きい"]
        },
        "ko": {
            "name": "클로",
            "title": "무투·클로",
            "tagline": "방어선을 찢다",
            "play": "날카로운 발톱으로 연속 베기를 가합니다. 같은 직업으로 권도 선택할 수 있습니다.",
            "pros": ["적의 방어를 빠르게 붕괴시킴", "치명타와 연타 능력을 겸비", "맹렬한 연격 리듬"],
            "cons": ["방어력이 얇음", "사거리가 짧음", "실수했을 때의 대가가 큼"]
        },
        "es": {
            "name": "Garra",
            "title": "Monje · Garra",
            "tagline": "Desgarra la Línea Defensiva",
            "play": "Encadena zarpazos sucesivos. Esta clase también puede usar puños.",
            "pros": ["Ruptura rápida de guardia", "Combina crítico y ráfaga continua", "Ritmo agresivo de abalanza"],
            "cons": ["Defensa delgada", "Alcance corto", "Alto costo al cometer errores"]
        }
    },
    "magic": {
        "zh_TW": {
            "name": "杖",
            "title": "法師·杖",
            "tagline": "把星屑當墨",
            "play": "靠技能和魂器打節奏。同職也可玩水晶。",
            "pros": ["技能傷害倍率最高", "跟戰魂、觀星配合最好", "打得到一片"],
            "cons": ["物理防禦低", "星屑燒得快", "被近身容易崩"]
        },
        "zh_CN": {
            "name": "杖",
            "title": "法师·杖",
            "tagline": "引星屑为墨",
            "play": "依赖技能与战魂法器把控节奏。同职业亦可使用水晶。",
            "pros": ["技能伤害倍率首屈一指", "与战魂、观星配合效果极佳", "大范围群伤打击"],
            "cons": ["物理抗性极为低下", "星屑消耗速度极快", "被贴身后极易溃败"]
        },
        "en": {
            "name": "Staff",
            "title": "Mage · Staff",
            "tagline": "Stardust as Ink",
            "play": "Set the rhythm with spells and soul vessels. Crystals are also playable in this class.",
            "pros": ["Highest skill damage multiplier", "Best synergy with combat souls and stargazing", "Hits wide areas"],
            "cons": ["Low physical defense", "Burns stardust quickly", "Vulnerable when rushed"]
        },
        "ja": {
            "name": "杖",
            "title": "法師・杖",
            "tagline": "星屑を墨として",
            "play": "技と戦魂の器で戦闘リズムを支配する。同職で水晶も扱える。",
            "pros": ["スキルのダメージ倍率が最高峰", "戦魂や天体観測と最も噛み合う", "広範囲を一掃できる"],
            "cons": ["物理防御力が低い", "星屑の消費が激しい", "接近戦に持ち込まれると脆い"]
        },
        "ko": {
            "name": "지팡이",
            "title": "법사·지팡이",
            "tagline": "별빛 가루를 먹물 삼아",
            "play": "기술과 영혼 그릇으로 전투의 리듬을 조율합니다. 같은 직업으로 수정도 선택할 수 있습니다.",
            "pros": ["스킬 피해 배율이 가장 높음", "전투혼 및 천체 관측과의 시너지가 뛰어남", "넓은 범위를 한 번에 타격"],
            "cons": ["물리 방어력이 낮음", "별빛 가루 소모가 빠름", "접근전을 허용하면 취약함"]
        },
        "es": {
            "name": "Báculo",
            "title": "Mago · Báculo",
            "tagline": "Polvo de Estrellas como Tinta",
            "play": "Marca el ritmo con hechizos y vasijas de almas. Esta clase también puede usar cristal.",
            "pros": ["Mayor multiplicador de daño de habilidad", "Máxima sinergia con almas de batalla y observación estelar", "Impacta en áreas amplias"],
            "cons": ["Baja defensa física", "Consume polvo estelar rápidamente", "Muy vulnerable en combate cuerpo a cuerpo"]
        }
    },
    "crystal": {
        "zh_TW": {
            "name": "水晶",
            "title": "法師·晶",
            "tagline": "把護盾織成刃",
            "play": "穩穩打，靠戰魂和護體撐。同職也可玩杖。",
            "pros": ["防禦、血量和輔助都不錯", "魂槽特別好用", "活得久、耗得起"],
            "cons": ["傷害偏軟", "前期慢熱", "很吃材料"]
        },
        "zh_CN": {
            "name": "水晶",
            "title": "法师·晶",
            "tagline": "聚护盾为锐刃",
            "play": "稳扎稳打，凭借战魂与护体灵光周旋。同职业亦可使用法杖。",
            "pros": ["防御、血量与辅助表现均衡", "战魂插槽增益显著", "生存力持久耐得消耗"],
            "cons": ["输出伤害偏柔和", "战斗前期节奏慢热", "资源材料消耗颇大"]
        },
        "en": {
            "name": "Crystal",
            "title": "Mage · Crystal",
            "tagline": "Weave the Barrier into a Blade",
            "play": "Fight methodically, sustained by combat souls and barriers. The staff is also playable in this class.",
            "pros": ["Solid defense, health, and support", "Soul slots shine exceptionally", "Survives long, outlasts encounters"],
            "cons": ["Milder damage output", "Slow wind-up early game", "Demands significant materials"]
        },
        "ja": {
            "name": "水晶",
            "title": "法師・晶",
            "tagline": "障壁を刃へと紡ぐ",
            "play": "戦魂と護身の光で着実に耐え抜く。同職で杖も扱える。",
            "pros": ["防御・耐久・支援のすべてが優秀", "魂スロットの恩恵が大きい", "長期戦を耐え抜く持久力"],
            "cons": ["攻撃性能はやや控えめ", "序盤の立ち上がりが遅い", "育成素材の要求が多い"]
        },
        "ko": {
            "name": "수정",
            "title": "법사·수정",
            "tagline": "보호막을 날카로운 검으로",
            "play": "전투혼과 호신 결계로 안정적인 전투를 이끕니다. 같은 직업으로 지팡이도 선택할 수 있습니다.",
            "pros": ["방어, 생명력, 보조 능력 모두 우수함", "혼 슬롯 효율이 매우 뛰어남", "장기전을 버텨내는 강인함"],
            "cons": ["피해량이 다소 완만함", "전투 초반 예열이 필요함", "재료 소모가 많은 편"]
        },
        "es": {
            "name": "Cristal",
            "title": "Mago · Cristal",
            "tagline": "Teje el Escudo en una Hoja",
            "play": "Lucha con firmeza, resistiendo con almas de combate y barreras. Esta clase también puede usar báculo.",
            "pros": ["Defensa, salud y apoyo equilibrados", "Las ranuras de alma rinden al máximo", "Gran aguante en combates prolongados"],
            "cons": ["Daño más moderado", "Arranque lento al inicio", "Requiere bastantes materiales"]
        }
    },
    "bow": {
        "zh_TW": {
            "name": "弓",
            "title": "遊俠·弓",
            "tagline": "等風的人",
            "play": "拉開距離再射。同職也可玩火槍。",
            "pros": ["站遠遠地安全輸出", "暴擊愈養愈高", "很吃疾影那種讀時機的打法"],
            "cons": ["被貼身就危險", "怒氣技蓄得比較慢", "防具選擇薄"]
        },
        "zh_CN": {
            "name": "弓",
            "title": "游侠·弓",
            "tagline": "静候风息之人",
            "play": "保持距离从容拉弦射击。同职业亦可使用火枪。",
            "pros": ["极远距离安全输出", "暴击率随养成逐步攀升", "契合静候破绽的战法"],
            "cons": ["一旦被贴身极度凶险", "怒气招式蓄积较为缓慢", "护甲抗性偏于薄弱"]
        },
        "en": {
            "name": "Bow",
            "title": "Ranger · Bow",
            "tagline": "One Who Waits for the Wind",
            "play": "Keep distance and snipe safely. Guns are also playable in this class.",
            "pros": ["Safe damage from long range", "Crit scales higher and higher", "Rewards reading wind and timing"],
            "cons": ["Perilous when foes get close", "Slower rage build-up", "Light armor options"]
        },
        "ja": {
            "name": "弓",
            "title": "レンジャー・弓",
            "tagline": "風を待つ者",
            "play": "間合いを取って安全圏から射貫く。同職で銃も扱える。",
            "pros": ["安全な長距離から安定して攻撃", "会心率が育つほど跳ね上がる", "好機を見極める射撃と噛み合う"],
            "cons": ["接近されると極めて危険", "怒り技のチャージがやや遅い", "防具の選択肢が薄い"]
        },
        "ko": {
            "name": "활",
            "title": "레인저·활",
            "tagline": "바람을 기다리는 자",
            "play": "거리를 벌리고 안전하게 저격합니다. 같은 직업으로 총도 선택할 수 있습니다.",
            "pros": ["먼 거리에서 안전하게 화력을 투사", "성장할수록 치명타율이 급상승", "기회를 엿보는 저격과 어울림"],
            "cons": ["접근을 허용하면 위험함", "분노 기술 충전이 다소 느림", "방어구 선택지가 얇음"]
        },
        "es": {
            "name": "Arco",
            "title": "Guardabosques · Arco",
            "tagline": "Aquel que Espera al Viento",
            "play": "Mantén las distancias y dispara con seguridad. Esta clase también puede usar armas de fuego.",
            "pros": ["Ataque seguro desde lejos", "El crítico escala cada vez más alto", "Recompensa calcular el momento y el viento"],
            "cons": ["Muy peligroso si te acorralan", "Carga de furia algo lenta", "Pocas opciones de armadura pesada"]
        }
    },
    "gun": {
        "zh_TW": {
            "name": "火槍",
            "title": "遊俠·銃",
            "tagline": "一響定生死",
            "play": "遠遠點射。同職也可玩弓。",
            "pros": ["爆發極高", "遠距離有秒殺的機會", "打中很爽"],
            "cons": ["換彈和收招都慢", "被貼身極度危險", "最不容許失誤"]
        },
        "zh_CN": {
            "name": "火枪",
            "title": "游侠·铳",
            "tagline": "一鸣惊响定生死",
            "play": "远距离冷静点射狙杀。同职业亦可使用长弓。",
            "pros": ["单发爆发力极高", "远距离具备一击必杀之势", "命中反馈酣畅淋漓"],
            "cons": ["装填与收招皆显迟缓", "近身肉搏极度凶险", "容错率极其苛刻"]
        },
        "en": {
            "name": "Gun",
            "title": "Ranger · Gun",
            "tagline": "One Crack Decides All",
            "play": "Snipe patiently from afar. The bow is also playable in this class.",
            "pros": ["Extreme burst power", "Potential to eliminate targets at range", "Deeply satisfying hits"],
            "cons": ["Slow reload and recovery", "Deadly dangerous when cornered", "Zero tolerance for mistakes"]
        },
        "ja": {
            "name": "銃",
            "title": "レンジャー・銃",
            "tagline": "一撃が生死を分かつ",
            "play": "遠距離から冷静に狙い撃つ。同職で弓も扱える。",
            "pros": ["瞬間火力が極めて高い", "遠距離から一撃で仕留める破壊力", "命中時の手応えが格別"],
            "cons": ["装填と硬直が長い", "詰め寄られると致命的", "一瞬の失誤も許されない"]
        },
        "ko": {
            "name": "총",
            "title": "레인저·총",
            "tagline": "한 발의 굉음이 생사를 가른다",
            "play": "원거리에서 침착하게 조준 사격합니다. 같은 직업으로 활도 선택할 수 있습니다.",
            "pros": ["순간 폭발력이 극도로 높음", "원거리에서 일격필살의 기회 제공", "적중 시 뛰어난 손맛"],
            "cons": ["재장전과 후딜레이가 긺", "접근전을 허용하면 극도로 위험", "실수를 용납하지 않음"]
        },
        "es": {
            "name": "Pistola",
            "title": "Guardabosques · Pistola",
            "tagline": "Un Disparo Decide la Vida o la Muerte",
            "play": "Apunta y dispara con paciencia desde lejos. Esta clase también puede usar arco.",
            "pros": ["Potencia de ráfaga extrema", "Oportunidad de abatir objetivos a distancia", "Disparos muy contundentes"],
            "cons": ["Recarga y recuperación lentas", "Peligro extremo en distancias cortas", "Tolerancia nula a los errores"]
        }
    }
}

def main():
    print("=== 1. 生成各語系 weapon_class.json ===")
    for lc in LOCALES:
        lc_dir = os.path.join(CONTENT_I18N_DIR, lc)
        os.makedirs(lc_dir, exist_ok=True)
        out_data = {}
        for cid, trans in WEAPON_CLASSES_I18N.items():
            out_data[cid] = trans[lc]
        
        target_path = os.path.join(lc_dir, "weapon_class.json")
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(out_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  ✓ 寫入 {target_path} (12 流派)")

    print("\n=== 2. 更新各語系 ui.json 補齊流派名稱與修復 S/E 問題 ===")
    for lc in LOCALES:
        ui_path = os.path.join(CONTENT_I18N_DIR, lc, "ui.json")
        if not os.path.exists(ui_path):
            continue
        with open(ui_path, "r", encoding="utf-8") as f:
            ui_data = json.load(f)

        # 修正 S / E 問題
        if lc == "en" and ui_data.get("劍") == "S":
            ui_data["劍"] = "Sword"
            print("  ✓ 修復 en/ui.json: '劍': 'S' -> 'Sword'")
        elif lc == "es" and ui_data.get("劍") == "E":
            ui_data["劍"] = "Espada"
            print("  ✓ 修復 es/ui.json: '劍': 'E' -> 'Espada'")
        elif lc == "zh_TW":
            ui_data["劍"] = "劍"

        none_map = {
            "zh_TW": "未選武器流派",
            "zh_CN": "未选武器流派",
            "en": "No weapon path",
            "ja": "流派 未選択",
            "ko": "유파 미선택",
            "es": "Sin estilo"
        }
        ui_data["未選武器流派"] = none_map[lc]

        # 補齊 12 流派短名、稱號、標語、按鈕字
        for cid, trans in WEAPON_CLASSES_I18N.items():
            tw = trans["zh_TW"]
            cur = trans[lc]
            
            # 短名
            ui_data[tw["name"]] = cur["name"]
            # 稱號
            ui_data[tw["title"]] = cur["title"]
            # 標語
            ui_data[tw["tagline"]] = cur["tagline"]
            # 玩法句
            ui_data[tw["play"]] = cur["play"]
            # 優點第一條
            ui_data[tw["pros"][0]] = cur["pros"][0]
            # 繁中格式按鈕字 key: "劍·騎士·劍"
            btn_key = f"{tw['name']}·{tw['title']}"
            sep = " · " if lc in ["en", "es"] else ("・" if lc == "ja" else "·")
            ui_data[btn_key] = f"{cur['name']}{sep}{cur['title']}"

        with open(ui_path, "w", encoding="utf-8") as f:
            json.dump(ui_data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  ✓ 成功同步 {ui_path}")

if __name__ == "__main__":
    main()
