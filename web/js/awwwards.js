/**
 * Clockwork Heart · Award-Winning Experience Engine
 * Awwwards / Webby / Zerotype Standard Interactive System
 */

(function () {
  'use strict';

  // =========================================================================
  // 1. Data Model: 13 Clockwork Races
  // =========================================================================
  const RACES_DATA = [
    {
      id: 'rabbit',
      name: '白金兔 · 小白',
      role: '晨曦劍士 · 時間守護者',
      shortRole: '劍士',
      image: 'media/hero/char_rabbit.png',
      idle: 'media/hero/rabbit_idle.png',
      quote: '「齒輪咔嗒作響時，就是弱點鬆脫的一刻。」',
      desc: '先行者小白經典族系，中央大鐘的時間守護者。米白金屬板件與黃銅發條鑰匙，長耳能清晰聽辨機關卡死異響，直擊敵人核心弱點。',
      weaponName: '晨曦發條單手長劍',
      weaponDesc: '冷軋精鋼打造，內嵌高速離合齒輪，可在刺入瞬間高速旋轉造成破甲撕裂。',
      stamina: 15,
      breakRate: 96,
      agility: 92,
      defense: 84,
      weakness: '聽聲鎖定 (長耳精準共振)',
      trait: '部位破壞 (零件逐塊擊落)',
      material: '鍛造米白合金板件 · 黃銅發條鑰匙 · 翡翠能量核心'
    },
    {
      id: 'lion',
      name: '烈鬃獅',
      role: '皇家近衛 · 騎士長',
      shortRole: '騎士',
      image: 'media/hero/char_lion.png',
      idle: 'media/hero/lion_idle.png',
      quote: '「金屬的咆哮，是玩具王國最堅固的長城。」',
      desc: '黃銅都市發條樞紐守護者，胡桃鉗皇家近衛儀隊之首。身披重裝鍛造板件與烈火般的黃銅鬃毛，衝鋒勢不可擋。',
      weaponName: '皇家黃銅突刺長槍',
      weaponDesc: '雙螺旋重型突刺長槍，衝鋒時帶動背部重力飛輪蓄力，擊碎一切堅固工事。',
      stamina: 15,
      breakRate: 90,
      agility: 78,
      defense: 98,
      weakness: '裝甲鉸鏈處 (過熱排氣孔)',
      trait: '重裝衝鋒 (剛體霸體貫穿)',
      material: '黃銅雕花重甲 · 鎢鋼骨架 · 烈焰能量核心'
    },
    {
      id: 'fox',
      name: '靈尾狐',
      role: '星盤秘術師 · 占星賢者',
      shortRole: '法師',
      image: 'media/hero/char_fox.png',
      idle: 'media/hero/fox_idle.png',
      quote: '「十四主星軸轉動之處，魔能如發條般蔓延。」',
      desc: '星象觀測台與發條藤蔓守護者。專精十四主星軸共鳴秘術與懸浮連桿星軸長尾，操縱星象符文引發範圍崩解。',
      weaponName: '星盤晶核秘術法杖',
      weaponDesc: '內嵌星盤陀螺儀與翡翠晶核，導引星軸發條共振引發魔能幾何陣列。',
      stamina: 15,
      breakRate: 88,
      agility: 95,
      defense: 72,
      weakness: '星軸連桿關節 (光學核心干擾)',
      trait: '星軸共振 (全場秘法擴散)',
      material: '琉璃琺瑯板件 · 懸浮星輪連桿 · 占星翡翠核心'
    },
    {
      id: 'boar',
      name: '鋼牙豕',
      role: '鍛爐工兵 · 重破壞者',
      shortRole: '戰士',
      image: 'media/hero/char_boar.png',
      idle: 'media/hero/boar_idle.png',
      quote: '「沒有什麼是一鐵砧鎚砸不爛的，如果有，就兩鎚。」',
      desc: '耐熱高溫鍛爐的重裝工兵。外露鎢鋼長獠牙與履帶紋底盤，專克泰坦巨甲，任何金屬在鐵砧重鎚前皆為齏粉。',
      weaponName: '鍛爐鐵砧重型戰鎚',
      weaponDesc: '重型鍛造鐵砧鎚頭，下砸時釋放高壓蒸氣衝擊波，震碎重型板件。',
      stamina: 15,
      breakRate: 98,
      agility: 65,
      defense: 94,
      weakness: '背部蒸氣閥洩壓口',
      trait: '碎甲猛擊 (破甲值翻倍)',
      material: '耐火鑄鐵板件 · 鎢鋼獠牙 · 蒸氣高壓氣閥'
    },
    {
      id: 'monkey',
      name: '靈爪猴',
      role: '千機巧匠 · 靈動客',
      shortRole: '武術家',
      image: 'media/hero/char_monkey.png',
      idle: 'media/hero/monkey_idle.png',
      quote: '「只要給我一根連桿，我就能撬起整座玩具城堡。」',
      desc: '齒輪高塔的靈巧工匠。四肢配備微型發條抓鉤，能在機關立柱間疾速攀爬，以精密千機棍拆卸敵人齒輪軸心。',
      weaponName: '千機伸縮發條長棍',
      weaponDesc: '多節連桿伸縮長棍，可隨發條釋放瞬間延長三倍，精準挑開暗扣。',
      stamina: 15,
      breakRate: 92,
      agility: 99,
      defense: 70,
      weakness: '抓鉤伸縮捲簧卡滯',
      trait: '疾風跳躍 (滯空連段拆解)',
      material: '輕量鋁合金板件 · 微型發條捲簧 · 琥珀動能核心'
    },
    {
      id: 'tiger',
      name: '烈焰虎',
      role: '熾火斥候 · 瞬影者',
      shortRole: '忍者',
      image: 'media/hero/char_tiger.png',
      idle: 'media/hero/tiger_idle.png',
      quote: '「在火星迸發的剎那，勝負早已底定。」',
      desc: '黑曜石熔火盆地的先鋒斥候。純黑曜石烤漆與赤金發條，雙手裝備高頻震盪苦無，擅長在高速位移中進行背刺部位破壞。',
      weaponName: '赤金高頻震盪苦無',
      weaponDesc: '發條高速旋轉帶動鋸齒高頻震動，切金斷玉如裂薄紙。',
      stamina: 15,
      breakRate: 94,
      agility: 98,
      defense: 75,
      weakness: '高速散熱排氣葉片',
      trait: '瞬影背刺 (暴擊部位必斷)',
      material: '黑曜烤漆鋼板 · 鈦合金利爪 · 赤金蓄能發條'
    },
    {
      id: 'crane',
      name: '雲嵐鶴',
      role: '天際巡音 · 狙擊手',
      shortRole: '遊俠',
      image: 'media/hero/char_crane.png',
      idle: 'media/hero/crane_idle.png',
      quote: '「羽翼劃過長空，唯留精準貫穿的彈道。」',
      desc: '浮空島浮雲頂層的守望者。修長銀白板件與展開式滑翔翼翼弦，手持長管發條風壓銃，超遠距離精準擊破敵方脆弱發條。',
      weaponName: '雲嵐超長管發條風壓銃',
      weaponDesc: '利用三段式發條壓縮氣囊，釋放音速穿甲氣彈，超視距破壞部位。',
      stamina: 15,
      breakRate: 93,
      agility: 94,
      defense: 68,
      weakness: '滑翔翼展鉸鏈節點',
      trait: '鷹眼狙擊 (弱點倍率增幅)',
      material: '航空超輕銀白合金 · 碳纖維滑翔翼 · 蔚藍氣動核心'
    },
    {
      id: 'bear',
      name: '玄軸熊',
      role: '重盾壁壘 · 守護者',
      shortRole: '戰士',
      image: 'media/hero/char_bear.png',
      idle: 'media/hero/bear_idle.png',
      quote: '「若我立於此處，王國大門絕不陷落。」',
      desc: '極北冰原發條防線的不可撼動之盾。全身包裹多層防禦板件與重型減震液壓阻尼，以巨型齒輪重盾抵禦一切狂轟濫炸。',
      weaponName: '玄鐵旋轉齒輪巨盾',
      weaponDesc: '邊緣具備高速咬合旋轉齒輪，能碾碎近身攻擊並反彈動能。',
      stamina: 15,
      breakRate: 85,
      agility: 62,
      defense: 100,
      weakness: '液壓阻尼活塞密封圈',
      trait: '絕對壁壘 (格擋反震崩解)',
      material: '玄鐵多層裝甲 · 液壓減震筒 · 寒霜動能核心'
    },
    {
      id: 'penguin',
      name: '蒸氣企鵝',
      role: '霜河航海士 · 連射手',
      shortRole: '遊俠',
      image: 'media/hero/char_penguin.png',
      idle: 'media/hero/penguin_idle.png',
      quote: '「蒸氣在鳴笛，這片海域由我的雙銃主宰。」',
      desc: '冰河運河的巡邏領航員。身著潛水銅盔造型裝甲與背負式微型蒸氣鍋爐，手持雙持發條連發銃，在滑行中持續壓制敵人。',
      weaponName: '雙持蒸氣連動旋轉銃',
      weaponDesc: '雙管交替供彈，每分鐘釋放 600 發發條鋼珠，造成密集壓制破甲。',
      stamina: 15,
      breakRate: 89,
      agility: 88,
      defense: 80,
      weakness: '背部微型鍋爐壓力表',
      trait: '滑行射擊 (保持距離擊破)',
      material: '黃銅抗腐蝕合金 · 耐寒生膠密封件 · 蒸氣動力背包'
    },
    {
      id: 'turtle',
      name: '玄機龜',
      role: '古軸占星師 · 陣法使',
      shortRole: '法師',
      image: 'media/hero/char_turtle.png',
      idle: 'media/hero/turtle_idle.png',
      quote: '「古老陣盤轉動時，時間將在此停滯。」',
      desc: '深淵遺跡的千古陣法學者。背負碩大星盤羅盤甲殼，能引導古代發條密碼，製造重力遲滯力場並瓦解大範圍敵方機關。',
      weaponName: '古代星軸八卦陣盤',
      weaponDesc: '八層重疊銅環陣盤，轉動時釋放時空遲滯重力場，定住敵人部件。',
      stamina: 15,
      breakRate: 87,
      agility: 58,
      defense: 99,
      weakness: '甲殼底盤中軸滑槽',
      trait: '時空力場 (範圍降速易碎)',
      material: '古青銅包覆板件 · 隕鐵重力軸心 · 星象占卜陣列'
    },
    {
      id: 'elephant',
      name: '鋼岳象',
      role: '泰坦破城者 · 先鋒隊',
      shortRole: '戰士',
      image: 'media/hero/char_elephant.png',
      idle: 'media/hero/elephant_idle.png',
      quote: '「鋼鐵的重壓下，城壘化為齏粉。」',
      desc: '攻城戰線的巨型泰坦先鋒。龐大的身軀以高張力鋼板與多級齒輪變速箱驅動，長象鼻為重型液壓破城鎚，踐踏震撼大地。',
      weaponName: '液壓多級破城重象鼻',
      weaponDesc: '內建三級增壓活塞，正面撞擊能將重型防禦裝甲一次性徹底擊碎。',
      stamina: 15,
      breakRate: 99,
      agility: 55,
      defense: 99,
      weakness: '頸部液壓主管道鉸鍊',
      trait: '泰坦踐踏 (全場霸體擊飛)',
      material: '高張力複合鋼板 · 三級行星齒輪箱 · 泰坦液壓桿'
    },
    {
      id: 'frog',
      name: '碧簧蛙',
      role: '暗夜跳躍者 · 毒刃客',
      shortRole: '忍者',
      image: 'media/hero/char_frog.png',
      idle: 'media/hero/frog_idle.png',
      quote: '「彈簧收緊的瞬間，即是獵物命運的落幕。」',
      desc: '青竹秘境暗夜潛行者。高彈性發條避震彈簧腿與外露雙眼光學核心，以機關旋刃鏢與疾速跳躍突襲見長。',
      weaponName: '碧葉旋刃機關鏢',
      weaponDesc: '旋轉飛鏢附帶回力倒鉤，投擲後可高速切割並回收發條動能。',
      stamina: 15,
      breakRate: 91,
      agility: 99,
      defense: 66,
      weakness: '腿部簧片蓄力僵直',
      trait: '彈簧跳躍 (旋刃突刺割裂)',
      material: '碧綠烤漆板件 · 鎢鋼彈簧腿 · 光學偵測眼'
    },
    {
      id: 'panda',
      name: '瓷韻熊貓',
      role: '太極拳聖 · 禪武者',
      shortRole: '武術家',
      image: 'media/hero/char_panda.png',
      idle: 'media/hero/panda_idle.png',
      quote: '「以柔克剛，借彼之力，化萬物為發條律動。」',
      desc: '雲頂禪道古剎的武道修行者。羊脂白瓷板件與黑曜生漆光澤，手戴太極機關拳套，擅長借力打力與寸勁破勢連打。',
      weaponName: '乾坤太極機關拳套',
      weaponDesc: '拳套內置太極陰陽雙發條，剛柔並濟，引導對手力量反震並擊碎部位。',
      stamina: 15,
      breakRate: 95,
      agility: 90,
      defense: 88,
      weakness: '生漆關節防潮保養期',
      trait: '陰陽化勁 (寸勁破勢連打)',
      material: '羊脂白瓷板件 · 黑曜生漆護手 · 陰陽太極發條'
    }
  ];

  let currentRaceIdx = 0;

  // =========================================================================
  // 2. Astrolabe Canvas & Gold Dust Particle Engine
  // =========================================================================
  function initAstrolabeCanvas() {
    const canvas = document.getElementById('hero-astrolabe-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = 0, height = 0;
    let animationFrameId = null;

    const PARTICLE_COUNT = 75;
    const particles = [];

    // Shockwave ripples on heartbeat
    const shockwaves = [];

    window._triggerAstrolabePulse = function () {
      shockwaves.push({
        radius: 40,
        maxRadius: Math.max(width, height) * 0.75,
        alpha: 0.8,
        speed: 9
      });
    };

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 0.6,
        alpha: Math.random() * 0.7 + 0.2,
        speedX: (Math.random() - 0.5) * 0.35,
        speedY: -Math.random() * 0.45 - 0.15,
        twinkleSpeed: Math.random() * 0.02 + 0.008,
        twinkleAngle: Math.random() * Math.PI * 2
      });
    }

    let gearAngle1 = 0;
    let gearAngle2 = 0;

    function render() {
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Subtle Rotating Gear Background
      ctx.save();
      const centerX = width * 0.5;
      const centerY = height * 0.45;
      ctx.translate(centerX, centerY);

      // Outer Astrolabe Ring 1
      gearAngle1 += 0.0012;
      ctx.save();
      ctx.rotate(gearAngle1);
      ctx.strokeStyle = 'rgba(229, 195, 104, 0.07)';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(0, 0, 360, 0, Math.PI * 2);
      ctx.stroke();

      ctx.setLineDash([8, 16]);
      ctx.beginPath();
      ctx.arc(0, 0, 340, 0, Math.PI * 2);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.restore();

      // Outer Astrolabe Ring 2 (Counter-rotate)
      gearAngle2 -= 0.0018;
      ctx.save();
      ctx.rotate(gearAngle2);
      ctx.strokeStyle = 'rgba(62, 207, 191, 0.05)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(0, 0, 260, 0, Math.PI * 2);
      ctx.stroke();

      for (let g = 0; g < 12; g++) {
        const rad = (g * Math.PI * 2) / 12;
        ctx.beginPath();
        ctx.arc(Math.cos(rad) * 260, Math.sin(rad) * 260, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(229, 195, 104, 0.18)';
        ctx.fill();
      }
      ctx.restore();

      // Draw active shockwaves
      for (let s = shockwaves.length - 1; s >= 0; s--) {
        const wave = shockwaves[s];
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 0, wave.radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(62, 207, 191, ${wave.alpha * 0.6})`;
        ctx.lineWidth = 2.5;
        ctx.shadowColor = '#3ECFBF';
        ctx.shadowBlur = 14;
        ctx.stroke();
        ctx.restore();

        wave.radius += wave.speed;
        wave.alpha -= 0.015;
        if (wave.alpha <= 0 || wave.radius >= wave.maxRadius) {
          shockwaves.splice(s, 1);
        }
      }

      ctx.restore();

      // 2. Draw Gold Dust Particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        p.twinkleAngle += p.twinkleSpeed;
        const currentAlpha = p.alpha + Math.sin(p.twinkleAngle) * 0.2;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(229, 195, 104, ${Math.max(0.1, currentAlpha)})`;
        ctx.shadowColor = '#FFE580';
        ctx.shadowBlur = 6;
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;
      }

      animationFrameId = requestAnimationFrame(render);
    }

    render();
  }

  // =========================================================================
  // 3. Custom Clockwork Cursor
  // =========================================================================
  function initCustomCursor() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    let cursor = document.querySelector('.c-cursor');
    if (!cursor) {
      cursor = document.createElement('div');
      cursor.className = 'c-cursor';
      cursor.innerHTML = '<div class="c-cursor__dot"></div><div class="c-cursor__ring"></div>';
      document.body.appendChild(cursor);
    }

    let mouseX = -100, mouseY = -100;
    let ringX = -100, ringY = -100;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0)`;
    }, { passive: true });

    function animateRing() {
      ringX += (mouseX - ringX) * 0.22;
      ringY += (mouseY - ringY) * 0.22;
      const ring = cursor.querySelector('.c-cursor__ring');
      if (ring) {
        ring.style.transform = `translate3d(${ringX - mouseX}px, ${ringY - mouseY}px, 0)`;
      }
      requestAnimationFrame(animateRing);
    }
    animateRing();

    document.querySelectorAll('a, button, [role="button"], .race-nav-btn, .aww-tilt-card, .theater-tab-btn, .physical-key').forEach((el) => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
      el.addEventListener('mousedown', () => cursor.classList.add('is-active'));
      el.addEventListener('mouseup', () => cursor.classList.remove('is-active'));
    });
  }

  // =========================================================================
  // 4. Hero Focal Object: Zerotype Tactile Physical Winding Key Micro-interaction
  // =========================================================================
  function initPhysicalWindingKey() {
    const key = document.getElementById('physical-key');
    const mount = document.getElementById('keycap-mount');
    const stage = document.getElementById('keycap-stage');
    const ticksGroup = document.getElementById('dial-ticks-group');
    const cadenceMeter = document.getElementById('keycap-cadence-meter');
    const statusDot = document.getElementById('hud-status-dot');
    const statusLabel = document.getElementById('hud-status-label');
    const metricNumber = document.getElementById('hud-metric-number');
    const heartGem = document.getElementById('hub-heart-gem');
    const socketGlow = document.getElementById('socket-glow-ring');
    const sparksContainer = document.getElementById('key-sparks-container');

    const btnStep = document.getElementById('btn-wind-step');
    const btnFull = document.getElementById('btn-wind-full');
    const btnRelease = document.getElementById('btn-wind-release');

    if (!key || !mount) return;

    let tension = 0; // 0 to 15
    const MAX_TENSION = 15;
    let heartbeatTimer = null;
    let audioCtx = null;

    // A. Populate Dial Ticks in SVG (15 calibrated steps around perimeter)
    if (ticksGroup) {
      ticksGroup.innerHTML = '';
      const cx = 170, cy = 170, rInner = 138, rOuter = 152;
      for (let i = 0; i < MAX_TENSION; i++) {
        const deg = (i * 360 / MAX_TENSION) - 90;
        const rad = (deg * Math.PI) / 180;

        const x1 = cx + Math.cos(rad) * rInner;
        const y1 = cy + Math.sin(rad) * rInner;
        const x2 = cx + Math.cos(rad) * rOuter;
        const y2 = cy + Math.sin(rad) * rOuter;

        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1.toFixed(1));
        line.setAttribute('y1', y1.toFixed(1));
        line.setAttribute('x2', x2.toFixed(1));
        line.setAttribute('y2', y2.toFixed(1));
        line.setAttribute('class', 'dial-tick-line');
        line.setAttribute('id', `dial-tick-line-${i}`);
        ticksGroup.appendChild(line);

        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', x2.toFixed(1));
        dot.setAttribute('cy', y2.toFixed(1));
        dot.setAttribute('r', '2.5');
        dot.setAttribute('class', 'dial-tick-dot');
        dot.setAttribute('id', `dial-tick-dot-${i}`);
        ticksGroup.appendChild(dot);
      }
    }

    // B. Populate Cadence Meter Segments (15 blocks)
    if (cadenceMeter) {
      cadenceMeter.innerHTML = '';
      for (let i = 0; i < MAX_TENSION; i++) {
        const seg = document.createElement('div');
        seg.className = 'cadence-segment';
        seg.id = `cadence-seg-${i}`;
        cadenceMeter.appendChild(seg);
      }
    }

    // C. Web Audio API Sound Synthesizer (Realistic Gear Ratchet & Heartbeat)
    function getAudioContext() {
      if (!audioCtx) {
        const AudioCtor = window.AudioContext || window.webkitAudioContext;
        if (AudioCtor) audioCtx = new AudioCtor();
      }
      if (audioCtx && audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      return audioCtx;
    }

    function playRatchetSound(step) {
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const t = ctx.currentTime;
        const pitch = 0.95 + (step / MAX_TENSION) * 0.65;

        // Metallic tooth oscillator
        const osc = ctx.createOscillator();
        const oscGain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1250 * pitch, t);
        osc.frequency.exponentialRampToValueAtTime(340 * pitch, t + 0.04);
        oscGain.gain.setValueAtTime(0.28, t);
        oscGain.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
        osc.connect(oscGain);
        oscGain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.04);

        // Mechanical snap noise burst
        const bufferSize = ctx.sampleRate * 0.025;
        const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
        const data = noiseBuffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        const noise = ctx.createBufferSource();
        noise.buffer = noiseBuffer;
        const filter = ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(2800 * pitch, t);
        filter.Q.setValueAtTime(4, t);
        const noiseGain = ctx.createGain();
        noiseGain.gain.setValueAtTime(0.22, t);
        noiseGain.gain.exponentialRampToValueAtTime(0.001, t + 0.025);
        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(ctx.destination);
        noise.start(t);
        noise.stop(t + 0.025);
      } catch (e) {}
    }

    function playHeartbeatSound() {
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        [0, 0.18].forEach((delay, idx) => {
          const t = ctx.currentTime + delay;
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(idx === 0 ? 100 : 75, t);
          osc.frequency.exponentialRampToValueAtTime(32, t + 0.16);
          gain.gain.setValueAtTime(0.42, t);
          gain.gain.exponentialRampToValueAtTime(0.001, t + 0.16);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(t);
          osc.stop(t + 0.18);
        });
      } catch (e) {}
    }

    // D. Visual Feedback & Spark Particles
    function emitSparks(count = 5) {
      if (!sparksContainer) return;
      for (let i = 0; i < count; i++) {
        const spark = document.createElement('div');
        spark.className = 'key-spark';
        spark.style.left = '50%';
        spark.style.top = '50%';
        const angle = Math.random() * Math.PI * 2;
        const dist = 35 + Math.random() * 65;
        spark.style.setProperty('--dx', `${(Math.cos(angle) * dist).toFixed(1)}px`);
        spark.style.setProperty('--dy', `${(Math.sin(angle) * dist).toFixed(1)}px`);
        sparksContainer.appendChild(spark);
        setTimeout(() => spark.remove(), 600);
      }
    }

    // E. Tension State Updater
    function setTension(newTension, playSound = true) {
      tension = Math.max(0, Math.min(MAX_TENSION, newTension));
      const angle = tension * (360 / MAX_TENSION);

      key.style.transform = `rotate(${angle}deg)`;

      // Update dial tick dots
      for (let i = 0; i < MAX_TENSION; i++) {
        const dot = document.getElementById(`dial-tick-dot-${i}`);
        if (dot) {
          if (i < tension) {
            dot.classList.add('is-lit');
          } else {
            dot.classList.remove('is-lit');
          }
        }
      }

      // Update cadence progress segments
      for (let i = 0; i < MAX_TENSION; i++) {
        const seg = document.getElementById(`cadence-seg-${i}`);
        if (seg) {
          if (i < tension) {
            seg.classList.add('is-active');
            if (tension === MAX_TENSION) seg.classList.add('is-full');
            else seg.classList.remove('is-full');
          } else {
            seg.classList.remove('is-active', 'is-full');
          }
        }
      }

      if (metricNumber) {
        metricNumber.innerHTML = `${tension} <small>/ 15 點</small>`;
      }
      if (cadenceMeter) {
        cadenceMeter.setAttribute('aria-valuenow', tension);
      }

      if (playSound && tension > 0) {
        playRatchetSound(tension);
        emitSparks(4);
        if (socketGlow) socketGlow.classList.add('is-active');
      }

      if (heartGem) {
        heartGem.classList.remove('is-pulsing');
      }
      if (statusDot) {
        statusDot.classList.remove('is-active');
      }

      if (statusLabel) {
        if (tension === 0) {
          statusLabel.textContent = '待命狀態 · 點擊鑰匙開始上鍊';
        } else if (tension === MAX_TENSION) {
          statusLabel.textContent = '滿鍊蓄力完成 · 點擊放開釋放動能';
        } else {
          statusLabel.textContent = `正在上鍊 · 齒輪咬合蓄力 (CADENCE: ${tension}/15)`;
        }
      }
    }

    // F. Release Tension -> Heartbeat Awakening Sequence
    function releaseKey() {
      if (tension === 0) {
        setTension(MAX_TENSION, true);
      }

      key.classList.add('is-releasing');
      key.style.transform = `rotate(${tension * (360 / MAX_TENSION) + 360}deg)`;

      setTimeout(() => {
        key.classList.remove('is-releasing');
      }, 1200);

      // Trigger Heart Gem Pulse
      if (heartGem) {
        heartGem.classList.add('is-pulsing');
      }
      if (statusDot) {
        statusDot.classList.add('is-active');
      }
      if (statusLabel) {
        statusLabel.textContent = '已完全上鍊 · 心臟正在跳動 (HEARTBEAT RUNNING · 60 BPM)';
      }

      playHeartbeatSound();
      emitSparks(12);

      // Canvas shockwave ripple
      if (typeof window._triggerAstrolabePulse === 'function') {
        window._triggerAstrolabePulse();
      }

      // Sustained Heartbeat interval for 10 beats
      if (heartbeatTimer) clearInterval(heartbeatTimer);
      let beatsRemaining = 10;
      heartbeatTimer = setInterval(() => {
        playHeartbeatSound();
        if (typeof window._triggerAstrolabePulse === 'function') {
          window._triggerAstrolabePulse();
        }
        beatsRemaining--;
        if (beatsRemaining <= 0) {
          clearInterval(heartbeatTimer);
          heartbeatTimer = null;
        }
      }, 1000);
    }

    // G. Event Listeners for Buttons & Key Clicks
    if (btnStep) {
      btnStep.addEventListener('click', (e) => {
        e.preventDefault();
        setTension(tension < MAX_TENSION ? tension + 1 : 1, true);
      });
    }

    if (btnFull) {
      btnFull.addEventListener('click', (e) => {
        e.preventDefault();
        let step = tension;
        const interval = setInterval(() => {
          step++;
          setTension(step, true);
          if (step >= MAX_TENSION) {
            clearInterval(interval);
          }
        }, 35);
      });
    }

    if (btnRelease) {
      btnRelease.addEventListener('click', (e) => {
        e.preventDefault();
        releaseKey();
      });
    }

    key.addEventListener('click', (e) => {
      e.preventDefault();
      if (tension >= MAX_TENSION) {
        releaseKey();
      } else {
        setTension(tension + 1, true);
      }
    });

    // H. 3D Perspective Tilt on Mouse Movement
    if (stage) {
      stage.addEventListener('mousemove', (e) => {
        const rect = mount.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = (e.clientX - cx) / (rect.width / 2);
        const dy = (e.clientY - cy) / (rect.height / 2);

        const tiltX = -dy * 9;
        const tiltY = dx * 11;
        mount.style.transform = `perspective(1200px) rotateX(${tiltX.toFixed(2)}deg) rotateY(${tiltY.toFixed(2)}deg)`;
      });

      stage.addEventListener('mouseleave', () => {
        mount.style.transform = 'perspective(1200px) rotateX(0deg) rotateY(0deg)';
      });
    }

    // Initialize initial visual state
    setTension(0, false);

    // Automation helpers for testing & QA verification
    window.testWindFull = function () {
      setTension(MAX_TENSION, true);
    };
    window.testRelease = function () {
      releaseKey();
    };
  }

  // =========================================================================
  // 5. Thirteen Clockwork Races Interactive Showcase
  // =========================================================================
  function initRacesShowcase() {
    const rail = document.getElementById('race-nav-rail');
    if (!rail) return;

    rail.innerHTML = '';
    RACES_DATA.forEach((race, index) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `race-nav-btn ${index === 0 ? 'is-active' : ''}`;
      btn.setAttribute('role', 'tab');
      btn.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      btn.dataset.index = index;

      const idxStr = String(index + 1).padStart(2, '0');
      btn.innerHTML = `
        <span class="race-nav-btn__idx">${idxStr}</span>
        <span class="race-nav-btn__name">${race.name.split('·')[0].trim()}</span>
        <span class="race-nav-btn__role">${race.shortRole}</span>
      `;

      btn.addEventListener('click', () => switchRace(index));
      rail.appendChild(btn);
    });

    const prevBtn = document.getElementById('race-prev-btn');
    const nextBtn = document.getElementById('race-next-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        const prev = (currentRaceIdx - 1 + RACES_DATA.length) % RACES_DATA.length;
        switchRace(prev);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const next = (currentRaceIdx + 1) % RACES_DATA.length;
        switchRace(next);
      });
    }

    updateRaceView(0);
  }

  function switchRace(targetIndex) {
    if (targetIndex === currentRaceIdx) return;
    currentRaceIdx = targetIndex;

    const btns = document.querySelectorAll('.race-nav-btn');
    btns.forEach((btn, idx) => {
      if (idx === targetIndex) {
        btn.classList.add('is-active');
        btn.setAttribute('aria-selected', 'true');
        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      } else {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-selected', 'false');
      }
    });

    const mainImg = document.getElementById('stage-main-img');
    if (mainImg) {
      mainImg.style.opacity = '0';
      mainImg.style.transform = 'scale(0.92) translateY(12px)';
    }

    setTimeout(() => {
      updateRaceView(targetIndex);
      if (mainImg) {
        mainImg.style.opacity = '1';
        mainImg.style.transform = 'scale(1) translateY(0)';
      }
    }, 180);
  }

  function updateRaceView(index) {
    const data = RACES_DATA[index];
    if (!data) return;

    const idxStr = String(index + 1).padStart(2, '0');
    const elIdx = document.getElementById('stage-race-idx');
    const elName = document.getElementById('stage-race-name');
    const elRole = document.getElementById('stage-race-role');
    const elQuote = document.getElementById('stage-race-quote');
    const elDesc = document.getElementById('stage-race-desc');
    const elWeaponName = document.getElementById('stage-weapon-name');
    const elWeaponDesc = document.getElementById('stage-weapon-desc');
    const elMainImg = document.getElementById('stage-main-img');
    const elPixelImg = document.getElementById('stage-pixel-img');

    const barBreak = document.getElementById('spec-bar-break');
    const valBreak = document.getElementById('spec-val-break');
    const barAgility = document.getElementById('spec-bar-agility');
    const valAgility = document.getElementById('spec-val-agility');
    const barDef = document.getElementById('spec-bar-def');
    const valDef = document.getElementById('spec-val-def');

    const elWeakness = document.getElementById('spec-weakness-val');
    const elTrait = document.getElementById('spec-trait-val');
    const elMaterial = document.getElementById('spec-material-val');

    if (elIdx) elIdx.textContent = `№ ${idxStr} / 13`;
    if (elName) elName.textContent = data.name;
    if (elRole) elRole.textContent = data.role;
    if (elQuote) elQuote.textContent = data.quote;
    if (elDesc) elDesc.textContent = data.desc;
    if (elWeaponName) elWeaponName.textContent = data.weaponName;
    if (elWeaponDesc) elWeaponDesc.textContent = data.weaponDesc;

    if (elMainImg) {
      elMainImg.src = data.image;
      elMainImg.alt = `${data.name}立繪展示`;
    }
    if (elPixelImg) {
      elPixelImg.src = data.idle;
      elPixelImg.alt = `${data.name}實機像素素體`;
    }

    if (barBreak && valBreak) {
      barBreak.style.width = `${data.breakRate}%`;
      valBreak.textContent = `${data.breakRate}%`;
    }
    if (barAgility && valAgility) {
      barAgility.style.width = `${data.agility}%`;
      valAgility.textContent = `${data.agility}%`;
    }
    if (barDef && valDef) {
      barDef.style.width = `${data.defense}%`;
      valDef.textContent = `${data.defense}%`;
    }

    if (elWeakness) elWeakness.textContent = data.weakness;
    if (elTrait) elTrait.textContent = data.trait;
    if (elMaterial) elMaterial.textContent = data.material;
  }

  // =========================================================================
  // 6. Core Gameplay 3D Tilt Cards (Unified Dark Glassmorphism)
  // =========================================================================
  function init3DTiltCards() {
    const cards = document.querySelectorAll('.aww-tilt-card');
    cards.forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -9;
        const rotateY = ((x - centerX) / centerX) * 9;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-6px)`;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
      });
    });
  }

  // =========================================================================
  // 7. Official Cinematic Theater Video Switcher
  // =========================================================================
  function initTheaterSwitcher() {
    const tabs = document.querySelectorAll('.theater-tab-btn');
    const screen16x9 = document.getElementById('theater-screen-16x9');
    const chassis9x16 = document.getElementById('theater-chassis-9x16');

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('is-active'));
        tab.classList.add('is-active');

        const mode = tab.dataset.theaterMode;
        const videoSrc = tab.dataset.videoSrc;

        if (mode === 'portrait') {
          if (screen16x9) {
            screen16x9.style.display = 'none';
            const v = screen16x9.querySelector('video');
            if (v) v.pause();
          }
          if (chassis9x16) {
            chassis9x16.style.display = 'block';
            const v = chassis9x16.querySelector('video');
            if (v) {
              v.src = videoSrc;
              v.load();
            }
          }
        } else {
          if (chassis9x16) {
            chassis9x16.style.display = 'none';
            const v = chassis9x16.querySelector('video');
            if (v) v.pause();
          }
          if (screen16x9) {
            screen16x9.style.display = 'block';
            const v = screen16x9.querySelector('video');
            if (v) {
              v.src = videoSrc;
              v.load();
            }
          }
        }
      });
    });
  }

  // =========================================================================
  // 8. Navigation Bar Scroll & Mobile Menu Toggle
  // =========================================================================
  function initNavigation() {
    const nav = document.querySelector('.aww-nav');
    const toggle = document.getElementById('aww-toggle');
    const menu = document.getElementById('aww-menu');

    if (nav) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 20) {
          nav.classList.add('is-scrolled');
        } else {
          nav.classList.remove('is-scrolled');
        }
      }, { passive: true });
    }

    if (toggle && menu) {
      toggle.addEventListener('click', () => {
        const isOpen = menu.classList.contains('is-open');
        if (isOpen) {
          menu.classList.remove('is-open');
          toggle.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        } else {
          menu.classList.add('is-open');
          toggle.classList.add('is-open');
          toggle.setAttribute('aria-expanded', 'true');
        }
      });

      menu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          menu.classList.remove('is-open');
          toggle.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        });
      });
    }
  }

  // =========================================================================
  // 9. Scroll Reveal Observer (IntersectionObserver)
  // =========================================================================
  function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal-fade-up');
    if (!revealElements.length || !('IntersectionObserver' in window)) {
      revealElements.forEach(el => el.classList.add('is-revealed'));
      return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.02,
      rootMargin: '100px 0px 100px 0px'
    });

    revealElements.forEach((el) => observer.observe(el));
  }

  // =========================================================================
  // Bootstrap on DOMContentLoaded
  // =========================================================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  function initAll() {
    initNavigation();
    initAstrolabeCanvas();
    initCustomCursor();
    initPhysicalWindingKey();
    initRacesShowcase();
    init3DTiltCards();
    initTheaterSwitcher();
    initScrollReveal();
  }

})();
