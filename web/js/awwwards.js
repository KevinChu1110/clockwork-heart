/**
 * Clockwork Heart · Award-Winning Experience Engine
 * Awwwards / Webby / FWA Standard Interactive System
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
      breakRate: 99,
      agility: 68,
      defense: 94,
      weakness: '履帶咬合齒 (泥沙卡死)',
      trait: '霸體粉碎 (泰坦裝甲崩解)',
      material: '耐火鑄鐵外殼 · 鎢鋼獠牙 · 蒸氣壓力熔爐'
    },
    {
      id: 'macaque',
      name: '靈爪猴',
      role: '機關武術家 · 行者',
      shortRole: '武術家',
      image: 'media/hero/char_macaque.png',
      idle: 'media/hero/macaque_idle.png',
      quote: '「拳若靈簧，招式無常，機關連打寸勁破甲。」',
      desc: '演武場東方武道機關玩具。以長臂彈簧避震套管與機關銅爪見長，身手如風，可在空中連續踩踏借力。',
      weaponName: '機關發條靈爪護手',
      weaponDesc: '三節彈簧聯動爪刃，可在連打中高速收縮並扣入敵方關節，實施關節拆卸。',
      stamina: 15,
      breakRate: 93,
      agility: 98,
      defense: 75,
      weakness: '避震彈簧回彈延遲',
      trait: '疾速連打 (多段破甲擒拿)',
      material: '生漆胡桃木板件 · 彈簧避震套管 · 銅鍍黃金爪'
    },
    {
      id: 'tiger',
      name: '烈焰虎',
      role: '赤焰暗殺者 · 迅刃',
      shortRole: '忍者',
      image: 'media/hero/char_tiger.png',
      idle: 'media/hero/tiger_idle.png',
      quote: '「暗夜之中，只見雙刃閃過的赤金火花。」',
      desc: '赤焰熔爐耐火試驗工坊淬火玩具。幾何排氣狹縫板件，以極限高速暴擊雙刃見長，瞬息斬斷敵方傳動管線。',
      weaponName: '齒輪發條雙斬刃',
      weaponDesc: '雙刃內嵌自磨高速齒輪，交錯揮砍時迸發高溫熔鐵火花，切割合金。',
      stamina: 15,
      breakRate: 94,
      agility: 99,
      defense: 70,
      weakness: '高速排氣閥門過載',
      trait: '暴擊瞬殺 (殘影疾速位移)',
      material: '淬火黑鋼板件 · 幾何排氣狹縫 · 高溫熔鐵核心'
    },
    {
      id: 'crane',
      name: '雲嵐鶴',
      role: '風弦巡守者 · 神射手',
      shortRole: '遊俠',
      image: 'media/hero/char_crane.png',
      idle: 'media/hero/crane_idle.png',
      quote: '「一羽穿雲，千里之外已定勝負。」',
      desc: '通體冷淬青瓷琺瑯與折疊合金羽翼。以超視距風弦機關弓見長，能精準洞穿百米外敵人的精密發條樞紐。',
      weaponName: '風弦羽翼機關弓',
      weaponDesc: '折疊弓臂由微型絞盤拉緊，射出高轉速鎢鋼穿甲箭矢，附帶微型氣旋。',
      stamina: 15,
      breakRate: 91,
      agility: 94,
      defense: 68,
      weakness: '翼軸伺服馬達受創',
      trait: '超視距穿甲 (弱點致命一擊)',
      material: '冷淬青瓷琺瑯 · 航空鈦合金羽 · 高張力弦索'
    },
    {
      id: 'bear',
      name: '玄軸熊',
      role: '離心狂戰士 · 撼地者',
      shortRole: '戰士',
      image: 'media/hero/char_bear.png',
      idle: 'media/hero/bear_idle.png',
      quote: '「大地在我的重錘之下戰慄，無物能擋離心風暴。」',
      desc: '赤焰熔爐黑曜石淬火神壇的沉穩巨靈。焦糖琥珀漆壓鑄鋼板，以偏心離心重力巨錘與震地重擊令群敵膽寒。',
      weaponName: '玄軸偏心重力錘',
      weaponDesc: '偏心飛輪驅動重力鎚，揮動時離心力指數加劇，產生毀滅性重擊震波。',
      stamina: 15,
      breakRate: 98,
      agility: 65,
      defense: 99,
      weakness: '轉向慣性過大延遲',
      trait: '離心蓄力 (震地範圍衝擊)',
      material: '焦糖琥珀漆壓鑄板 · 偏心離心飛輪 · 厚重生鐵'
    },
    {
      id: 'penguin',
      name: '蒸氣企鵝',
      role: '深海導航員 · 射手',
      shortRole: '遊俠',
      image: 'media/hero/char_penguin.png',
      idle: 'media/hero/char_penguin.png',
      quote: '「冰層與深海之下，發條的律動從不熄滅。」',
      desc: '水下發條宮殿深海導航員。耐壓鍍鈦深藍琺瑯，背部配備蒸氣微型鍋爐與雙管火槍，可在極端環境下精準制導。',
      weaponName: '蒸氣雙管導航火槍',
      weaponDesc: '雙管黃銅發條氣動槍，發射高壓壓縮氣彈與自導向追蹤水銀彈。',
      stamina: 15,
      breakRate: 89,
      agility: 88,
      defense: 86,
      weakness: '鍋爐蒸氣減壓閥',
      trait: '雙管齊射 (高壓氣動推進)',
      material: '耐壓鍍鈦深藍板件 · 蒸氣鍋爐 · 導航陀螺儀'
    },
    {
      id: 'tortoise',
      name: '玄機龜',
      role: '奇門陣法師 · 宗師',
      shortRole: '法師',
      image: 'media/hero/char_tortoise.png',
      idle: 'media/hero/tortoise_idle.png',
      quote: '「八卦星盤定乾坤，機關萬象皆在陣中。」',
      desc: '天元竹林青石古道場的機關術宗師。青古銅龜甲板件，以八卦發條星盤與結界壁壘見長，能以柔克剛化解萬鈞重擊。',
      weaponName: '玄機八卦發條星盤',
      weaponDesc: '八卦齒輪星盤可推演敵方攻勢軌跡，展開多面金屬力場結界防壁。',
      stamina: 15,
      breakRate: 85,
      agility: 62,
      defense: 100,
      weakness: '星盤推演齒輪重置間隙',
      trait: '奇門結界 (力場化勁反震)',
      material: '青古銅雕花龜甲 · 八卦星盤齒輪 · 護體金鐘'
    },
    {
      id: 'elephant',
      name: '鋼岳象',
      role: '重裝工程巨兵 · 開山手',
      shortRole: '戰士',
      image: 'media/hero/char_elephant.png',
      idle: 'media/hero/elephant_idle.png',
      quote: '「踏平山岳，斷裂鋼梁，這便是巨輪的威力。」',
      desc: '黃銅都市巨輪工坊的巨型重裝工兵。六節套筒液壓長鼻與履帶底盤，手持開山重斧，一擊即可劈斷城門主軸。',
      weaponName: '巨輪開山重斧',
      weaponDesc: '重型液壓開山斧，劈斬足以切斷城門鉸鏈與泰坦巨偶支撐骨架。',
      stamina: 15,
      breakRate: 100,
      agility: 60,
      defense: 98,
      weakness: '液壓導管外露接頭',
      trait: '開山劈砍 (粉碎性壓迫)',
      material: '六節套筒液壓長鼻 · 鍛造開山巨斧 · 履帶底盤'
    },
    {
      id: 'frog',
      name: '碧簧蛙',
      role: '青竹暗夜客 · 潛行者',
      shortRole: '忍者',
      image: 'media/hero/char_frog.png',
      idle: 'media/hero/frog_idle.png',
      quote: '「簧片彈動之刻，勝負已於瞬息分曉。」',
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

    // Particles
    const PARTICLE_COUNT = 70;
    const particles = [];

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    // Initialize particles
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 2 + 0.6,
        alpha: Math.random() * 0.7 + 0.2,
        speedX: (Math.random() - 0.5) * 0.4,
        speedY: -Math.random() * 0.5 - 0.15,
        twinkleSpeed: Math.random() * 0.02 + 0.008,
        twinkleAngle: Math.random() * Math.PI * 2
      });
    }

    let gearAngle1 = 0;
    let gearAngle2 = 0;
    let gearAngle3 = 0;

    function drawGear(cx, cy, radius, teeth, toothDepth, angle, strokeStyle, fillStyle) {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(angle);
      ctx.beginPath();
      const step = (Math.PI * 2) / teeth;
      for (let i = 0; i < teeth; i++) {
        const a1 = i * step;
        const a2 = a1 + step * 0.25;
        const a3 = a1 + step * 0.5;
        const a4 = a1 + step * 0.75;

        const rIn = radius - toothDepth;
        const rOut = radius;

        if (i === 0) {
          ctx.moveTo(Math.cos(a1) * rIn, Math.sin(a1) * rIn);
        } else {
          ctx.lineTo(Math.cos(a1) * rIn, Math.sin(a1) * rIn);
        }
        ctx.lineTo(Math.cos(a2) * rOut, Math.sin(a2) * rOut);
        ctx.lineTo(Math.cos(a3) * rOut, Math.sin(a3) * rOut);
        ctx.lineTo(Math.cos(a4) * rIn, Math.sin(a4) * rIn);
      }
      ctx.closePath();

      if (fillStyle) {
        ctx.fillStyle = fillStyle;
        ctx.fill();
      }
      if (strokeStyle) {
        ctx.strokeStyle = strokeStyle;
        ctx.lineWidth = 1.4;
        ctx.stroke();
      }

      // Inner axle circle
      ctx.beginPath();
      ctx.arc(0, 0, radius * 0.35, 0, Math.PI * 2);
      ctx.strokeStyle = strokeStyle;
      ctx.lineWidth = 1.2;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(0, 0, radius * 0.1, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(62, 207, 191, 0.4)';
      ctx.fill();
      ctx.stroke();

      ctx.restore();
    }

    function render(timestamp) {
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Gold Dust Particles
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        const p = particles[i];
        p.x += p.speedX;
        p.y += p.speedY;
        p.twinkleAngle += p.twinkleSpeed;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.twinkleAngle));

        if (p.y < -10) {
          p.y = height + 10;
          p.x = Math.random() * width;
        }
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 230, 130, ${Math.max(0, currentAlpha)})`;
        ctx.shadowColor = 'rgba(255, 215, 60, 0.6)';
        ctx.shadowBlur = 6;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      // 2. Draw Celestial Astrolabe Gears
      const isMobile = width < 768;
      const astrolabeCenterX = isMobile ? width * 0.5 : width * 0.72;
      const astrolabeCenterY = isMobile ? height * 0.65 : height * 0.48;

      gearAngle1 += 0.0035;
      gearAngle2 -= 0.0022;
      gearAngle3 += 0.005;

      // Outer Astrolabe Ring with degree tick marks
      ctx.save();
      ctx.translate(astrolabeCenterX, astrolabeCenterY);
      ctx.rotate(gearAngle1 * 0.4);

      const rOuter = isMobile ? 200 : 300;
      ctx.beginPath();
      ctx.arc(0, 0, rOuter, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 230, 130, 0.45)';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Degree ticks
      const ticks = 36;
      for (let i = 0; i < ticks; i++) {
        const a = (i * Math.PI * 2) / ticks;
        const tLen = i % 3 === 0 ? 14 : 7;
        ctx.beginPath();
        ctx.moveTo(Math.cos(a) * (rOuter - tLen), Math.sin(a) * (rOuter - tLen));
        ctx.lineTo(Math.cos(a) * rOuter, Math.sin(a) * rOuter);
        ctx.strokeStyle = i % 3 === 0 ? 'rgba(255, 235, 150, 0.7)' : 'rgba(229, 195, 104, 0.35)';
        ctx.lineWidth = i % 3 === 0 ? 2.5 : 1.5;
        ctx.stroke();
      }
      ctx.restore();

      // Inner Interlocking Gears
      const gearRadius = isMobile ? 140 : 210;
      drawGear(
        astrolabeCenterX,
        astrolabeCenterY,
        gearRadius,
        28,
        14,
        gearAngle1,
        'rgba(255, 220, 110, 0.45)',
        'rgba(229, 195, 104, 0.04)'
      );

      // Secondary meshing gear (offset top-left)
      const offsetDist = gearRadius * 1.35;
      drawGear(
        astrolabeCenterX - offsetDist * 0.7,
        astrolabeCenterY - offsetDist * 0.7,
        gearRadius * 0.6,
        18,
        10,
        gearAngle2,
        'rgba(229, 195, 104, 0.35)',
        null
      );

      // Third meshing gear (offset bottom-right)
      drawGear(
        astrolabeCenterX + offsetDist * 0.65,
        astrolabeCenterY + offsetDist * 0.55,
        gearRadius * 0.45,
        14,
        8,
        gearAngle3,
        'rgba(62, 207, 191, 0.45)',
        null
      );

      animationFrameId = requestAnimationFrame(render);
    }

    animationFrameId = requestAnimationFrame(render);
  }

  // =========================================================================
  // 3. Custom Clockwork Gear Cursor
  // =========================================================================
  function initCustomCursor() {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    const cursorContainer = document.createElement('div');
    cursorContainer.className = 'c-cursor';
    cursorContainer.innerHTML = '<div class="c-cursor__gear"></div><div class="c-cursor__dot"></div>';
    document.body.appendChild(cursorContainer);

    let mouseX = -100, mouseY = -100;
    let gearX = -100, gearY = -100;
    let dotX = -100, dotY = -100;

    window.addEventListener('pointermove', function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    }, { passive: true });

    // Interactive element hover detection
    const interactiveSelectors = 'a, button, input, [role="button"], .aww-tilt-card, .race-nav-btn, .theater-tab-btn, .stage-nav-btn';
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest(interactiveSelectors)) {
        document.body.classList.add('is-hovering');
      }
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest(interactiveSelectors)) {
        document.body.classList.remove('is-hovering');
      }
    });

    function tickCursor() {
      // Smooth interpolation
      gearX += (mouseX - gearX) * 0.18;
      gearY += (mouseY - gearY) * 0.18;
      dotX += (mouseX - dotX) * 0.45;
      dotY += (mouseY - dotY) * 0.45;

      cursorContainer.style.transform = `translate3d(${gearX.toFixed(1)}px, ${gearY.toFixed(1)}px, 0)`;
      requestAnimationFrame(tickCursor);
    }
    requestAnimationFrame(tickCursor);
  }

  // =========================================================================
  // 4. Thirteen Clockwork Races Interactive Showcase
  // =========================================================================
  function initRacesShowcase() {
    const rail = document.getElementById('race-nav-rail');
    if (!rail) return;

    // Render Rail Buttons
    rail.innerHTML = '';
    RACES_DATA.forEach((race, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'race-nav-btn' + (idx === 0 ? ' is-active' : '');
      btn.setAttribute('data-idx', idx);
      btn.innerHTML = `
        <span class="race-nav-btn__idx">${String(idx + 1).padStart(2, '0')}</span>
        <span class="race-nav-btn__name">${race.name.split('·')[0].trim()}</span>
        <span class="race-nav-btn__role">${race.shortRole}</span>
      `;
      btn.addEventListener('click', () => switchRace(idx));
      rail.appendChild(btn);
    });

    // Arrow Nav buttons
    const prevBtn = document.getElementById('race-prev-btn');
    const nextBtn = document.getElementById('race-next-btn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        const nextIdx = (currentRaceIdx - 1 + RACES_DATA.length) % RACES_DATA.length;
        switchRace(nextIdx);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        const nextIdx = (currentRaceIdx + 1) % RACES_DATA.length;
        switchRace(nextIdx);
      });
    }

    // Keyboard support
    document.addEventListener('keydown', (e) => {
      const raceSec = document.getElementById('races');
      if (!raceSec) return;
      const rect = raceSec.getBoundingClientRect();
      const isInView = rect.top < window.innerHeight && rect.bottom > 0;
      if (!isInView) return;

      if (e.key === 'ArrowLeft') {
        const nextIdx = (currentRaceIdx - 1 + RACES_DATA.length) % RACES_DATA.length;
        switchRace(nextIdx);
      } else if (e.key === 'ArrowRight') {
        const nextIdx = (currentRaceIdx + 1) % RACES_DATA.length;
        switchRace(nextIdx);
      }
    });

    // Initial render
    updateRaceStage(0, false);
  }

  function switchRace(idx) {
    if (idx === currentRaceIdx) return;
    currentRaceIdx = idx;

    // Update rail active state
    const railBtns = document.querySelectorAll('.race-nav-btn');
    railBtns.forEach((btn, i) => {
      if (i === idx) {
        btn.classList.add('is-active');
        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      } else {
        btn.classList.remove('is-active');
      }
    });

    updateRaceStage(idx, true);
  }

  function updateRaceStage(idx, animate) {
    const data = RACES_DATA[idx];
    if (!data) return;

    // Elements
    const idxBig = document.getElementById('stage-race-idx');
    const nameEl = document.getElementById('stage-race-name');
    const roleEl = document.getElementById('stage-race-role');
    const quoteEl = document.getElementById('stage-race-quote');
    const descEl = document.getElementById('stage-race-desc');
    const weaponNameEl = document.getElementById('stage-weapon-name');
    const weaponDescEl = document.getElementById('stage-weapon-desc');
    const mainImgEl = document.getElementById('stage-main-img');
    const pixelImgEl = document.getElementById('stage-pixel-img');

    // Spec Bars
    const barBreak = document.getElementById('spec-bar-break');
    const barAgility = document.getElementById('spec-bar-agility');
    const barDef = document.getElementById('spec-bar-def');
    const valBreak = document.getElementById('spec-val-break');
    const valAgility = document.getElementById('spec-val-agility');
    const valDef = document.getElementById('spec-val-def');

    const weaknessEl = document.getElementById('spec-weakness-val');
    const traitEl = document.getElementById('spec-trait-val');
    const matEl = document.getElementById('spec-material-val');

    if (animate && mainImgEl) {
      mainImgEl.style.opacity = '0';
      mainImgEl.style.transform = 'scale(0.92) translateY(12px)';
    }

    setTimeout(() => {
      if (idxBig) idxBig.textContent = `№ ${String(idx + 1).padStart(2, '0')} / 13`;
      if (nameEl) nameEl.textContent = data.name;
      if (roleEl) roleEl.textContent = data.role;
      if (quoteEl) quoteEl.textContent = data.quote;
      if (descEl) descEl.textContent = data.desc;
      if (weaponNameEl) weaponNameEl.textContent = data.weaponName;
      if (weaponDescEl) weaponDescEl.textContent = data.weaponDesc;

      if (mainImgEl) {
        mainImgEl.src = data.image;
        mainImgEl.alt = `${data.name} 2.2頭身發條玩具立繪展示`;
        mainImgEl.style.opacity = '1';
        mainImgEl.style.transform = 'scale(1) translateY(0)';
      }

      if (pixelImgEl) {
        pixelImgEl.src = data.idle;
        pixelImgEl.alt = `${data.name} 實機像素素體`;
      }

      // Spec values
      if (barBreak) barBreak.style.width = `${data.breakRate}%`;
      if (barAgility) barAgility.style.width = `${data.agility}%`;
      if (barDef) barDef.style.width = `${data.defense}%`;

      if (valBreak) valBreak.textContent = `${data.breakRate}%`;
      if (valAgility) valAgility.textContent = `${data.agility}%`;
      if (valDef) valDef.textContent = `${data.defense}%`;

      if (weaknessEl) weaknessEl.textContent = data.weakness;
      if (traitEl) traitEl.textContent = data.trait;
      if (matEl) matEl.textContent = data.material;
    }, animate ? 150 : 0);
  }

  // =========================================================================
  // 5. 3D Tilt Parallax Cards (Core Pillars)
  // =========================================================================
  function init3DTiltCards() {
    const cards = document.querySelectorAll('.aww-tilt-card');
    if (!cards.length) return;

    cards.forEach((card) => {
      let bounds = null;

      function onMouseEnter() {
        bounds = card.getBoundingClientRect();
      }

      function onMouseMove(e) {
        if (!bounds) bounds = card.getBoundingClientRect();
        const mouseX = e.clientX - bounds.left;
        const mouseY = e.clientY - bounds.top;

        const xPct = (mouseX / bounds.width - 0.5) * 2;
        const yPct = (mouseY / bounds.height - 0.5) * 2;

        const rotateX = -yPct * 9; // deg
        const rotateY = xPct * 9;  // deg

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.025, 1.025, 1.025)`;
        card.style.setProperty('--mouse-x', `${(mouseX / bounds.width * 100).toFixed(1)}%`);
        card.style.setProperty('--mouse-y', `${(mouseY / bounds.height * 100).toFixed(1)}%`);
      }

      function onMouseLeave() {
        bounds = null;
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      }

      card.addEventListener('mouseenter', onMouseEnter);
      card.addEventListener('mousemove', onMouseMove);
      card.addEventListener('mouseleave', onMouseLeave);
    });
  }

  // =========================================================================
  // 6. Cinematic Theater Switcher
  // =========================================================================
  function initTheaterSwitcher() {
    const tabs = document.querySelectorAll('.theater-tab-btn');
    const screen16x9 = document.getElementById('theater-screen-16x9');
    const chassis9x16 = document.getElementById('theater-chassis-9x16');

    if (!tabs.length) return;

    tabs.forEach((tab) => {
      tab.addEventListener('click', () => {
        tabs.forEach((t) => t.classList.remove('is-active'));
        tab.classList.add('is-active');

        const mode = tab.getAttribute('data-theater-mode');
        const videoSrc = tab.getAttribute('data-video-src');

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
  // 7. Navigation Bar Scroll & Mobile Menu Toggle
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
  // 8. Scroll Reveal Observer (IntersectionObserver)
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
      threshold: 0.05,
      rootMargin: '80px 0px 80px 0px'
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
    initRacesShowcase();
    init3DTiltCards();
    initTheaterSwitcher();
    initScrollReveal();
  }

})();
