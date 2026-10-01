/**
 * Clockwork Heart · Award-Winning Experience Engine
 * Awwwards / Webby / FWA Standard Interactive System
 * Zerotype.ai Aesthetic Benchmark & Micro-Interactions
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
      weaponDesc: '頂端鑲嵌精密透鏡與能量晶核，引導星盤齒輪光束穿透敵方防護。',
      stamina: 15,
      breakRate: 88,
      agility: 95,
      defense: 72,
      weakness: '星盤晶核過載散熱間隙',
      trait: '星象共鳴 (範圍元素侵蝕)',
      material: '鍍銀輕質板件 · 靈能紫水晶核 · 懸浮磁力連桿'
    },
    {
      id: 'boar',
      name: '鋼牙豕',
      role: '攻城鍛造者 · 重裝破陣官',
      shortRole: '戰士',
      image: 'media/hero/char_boar.png',
      idle: 'media/hero/boar_idle.png',
      quote: '「只要力道夠大，所有精密零件都是廢鐵。」',
      desc: '鍛造火山高爐的核心爐工。粗壯的生鐵板件與雙螺旋合金獠牙，手持巨型鍛造重鎚，擅長正面硬碰硬砸碎敵方厚實裝甲。',
      weaponName: '熔火雙手鍛造重鎚',
      weaponDesc: '內建氣動加壓活塞，落下瞬間觸發二次爆燃衝擊波。',
      stamina: 15,
      breakRate: 97,
      agility: 68,
      defense: 96,
      weakness: '背部氣閥冷卻管',
      trait: '破陣碎甲 (強制破防暴擊)',
      material: '鑄鐵防爆板件 · 氣動活塞系統 · 高溫耐熱塗層'
    },
    {
      id: 'macaque',
      name: '靈爪猴',
      role: '天樞武鬥家 · 機關行者',
      shortRole: '武術家',
      image: 'media/hero/char_macaque.png',
      idle: 'media/hero/macaque_idle.png',
      quote: '「拳如流星，轉眼間你身上的螺帽就全空了。」',
      desc: '天元竹林機關道場的流浪武僧。全身配備多關節伺服連桿與精鋼爪拳套，以如影隨形的近身連打與徒手拆卸零件名震四方。',
      weaponName: '天樞發條鋼爪拳套',
      weaponDesc: '手腕內藏高速棘輪扳手機構，命中瞬間可強行旋開受擊者外殼螺帽。',
      stamina: 15,
      breakRate: 95,
      agility: 98,
      defense: 76,
      weakness: '關節連桿超轉過載',
      trait: '連鎖拆卸 (極速多段連擊)',
      material: '拉絲黃銅板件 · 柔性鋼絲肌腱 · 橡膠緩衝墊'
    },
    {
      id: 'tiger',
      name: '烈焰虎',
      role: '夜影刺客 · 破曉狂刃',
      shortRole: '忍者',
      image: 'media/hero/char_tiger.png',
      idle: 'media/hero/tiger_idle.png',
      quote: '「黑暗中只有金屬火花閃爍，那是死亡的序曲。」',
      desc: '陰影工坊與廢棄齒輪堆的潛行獵手。淬火黑鋼與幾何幾何導流板，背部微型氣冷推進器能在瞬間爆發超音速衝刺。',
      weaponName: '黑鋼折疊雙短刃',
      weaponDesc: '高頻振動等離子刃口，切開合金護板宛如熱刀切黃油。',
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
      material: '青古銅雕紋甲 · 八卦星盤機構 · 玄武能量核'
    },
    {
      id: 'elephant',
      name: '鋼岳象',
      role: '發條巨靈 · 破城前鋒',
      shortRole: '戰士',
      image: 'media/hero/char_elephant.png',
      idle: 'media/hero/elephant_idle.png',
      quote: '「每一步都是山崩地裂，機關堡壘的終結者。」',
      desc: '黃銅都市中央動力塔的守衛巨靈。啞光鈦灰裝甲板件，身背巨型蒸氣減速箱與液壓鋼鼻，一擊足以崩碎城門。',
      weaponName: '液壓多段衝擊長鼻',
      weaponDesc: '多節液壓鋼環套筒，伸縮間產生千噸撞擊力，伴隨高溫蒸氣排斥。',
      stamina: 15,
      breakRate: 99,
      agility: 58,
      defense: 100,
      weakness: '液壓活塞密封圈老化',
      trait: '巨獸重壓 (粉碎性障礙清除)',
      material: '啞光鈦灰重型裝甲 · 巨型蒸氣減速箱 · 液壓千斤頂'
    },
    {
      id: 'frog',
      name: '碧簧蛙',
      role: '彈簧特攻隊員 · 突擊手',
      shortRole: '忍者',
      image: 'media/hero/char_frog.png',
      idle: 'media/hero/frog_idle.png',
      quote: '「你看到我起跳時，我已經在你的頭頂上拆零件了。」',
      desc: '翠綠烤漆與雙腿高張力發條彈簧。以超高機動力空中突襲與彈射衝擊聞名，能在戰場各角度靈巧跳躍穿梭。',
      weaponName: '高張力發條迴旋雙鏢',
      weaponDesc: '彈射飛鏢由微型鋼絲牽引，飛出後自動收回並切割路徑上的所有機械。',
      stamina: 15,
      breakRate: 93,
      agility: 100,
      defense: 66,
      weakness: '腿部主彈簧疲勞卡死',
      trait: '極限彈跳 (垂直制空突襲)',
      material: '翠綠琺瑯烤漆 · 琴鋼絲高張力彈簧 · 輕量化鋁合金'
    },
    {
      id: 'panda',
      name: '瓷韻熊貓',
      role: '兩儀調和師 · 太極宗師',
      shortRole: '武術家',
      image: 'media/hero/char_panda.png',
      idle: 'media/hero/panda_idle.png',
      quote: '「陰陽齒輪互咬合，靜動之間轉乾坤。」',
      desc: '白瓷與黑曜石雙色板件。將兩儀太極之道融入發條律動，能在戰鬥中吸收敵人的撞擊動能，反向轉化為自身發條爆發力。',
      weaponName: '兩儀玄晶發條竹棍',
      weaponDesc: '竹節內藏同軸差速齒輪，旋轉時可牽引空氣形成渦流力場。',
      stamina: 15,
      breakRate: 92,
      agility: 85,
      defense: 94,
      weakness: '兩儀差速輪軸過熱',
      trait: '動能借力 (反彈蓄力釋放)',
      material: '高嶺土精燒白瓷板 · 磨砂黑曜石 · 太極雙動核心'
    }
  ];

  let currentRaceIdx = 0;
  let audioContext = null;
  let isSoundEnabled = true;
  let burstParticles = [];

  // =========================================================================
  // 2. Web Audio Ratchet Sound Synthesis Engine
  // =========================================================================
  function initAudioEngine() {
    const saved = localStorage.getItem('cw_sound_enabled');
    if (saved !== null) {
      isSoundEnabled = saved === 'true';
    }

    const toggleBtn = document.getElementById('sound-toggle');
    const toggleLabel = document.getElementById('sound-label');

    function updateUi() {
      if (toggleBtn && toggleLabel) {
        if (isSoundEnabled) {
          toggleBtn.classList.remove('is-muted');
          toggleLabel.textContent = '音效 ON';
        } else {
          toggleBtn.classList.add('is-muted');
          toggleLabel.textContent = '音效 OFF';
        }
      }
    }
    updateUi();

    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        isSoundEnabled = !isSoundEnabled;
        localStorage.setItem('cw_sound_enabled', String(isSoundEnabled));
        updateUi();
        if (isSoundEnabled) playTickSound(1200);
      });
    }
  }

  function getAudioContext() {
    if (!audioContext) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) audioContext = new AudioCtx();
    }
    if (audioContext && audioContext.state === 'suspended') {
      audioContext.resume();
    }
    return audioContext;
  }

  // Realistic Clockwork Ratchet Click
  function playTickSound(freq = 1600) {
    if (!isSoundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();

      filter.type = 'highpass';
      filter.frequency.setValueAtTime(800, ctx.currentTime);

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + 0.035);

      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.035);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.04);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  // Resonant Metallic Spring Release Chime
  function playReleaseChime() {
    if (!isSoundEnabled) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;

      const chord = [523.25, 659.25, 783.99, 1046.50]; // C Major Harmonic
      chord.forEach((freq, i) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.04);

        const startTime = ctx.currentTime + i * 0.04;
        gain.gain.setValueAtTime(0.2, startTime);
        gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.65);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(startTime);
        osc.stop(startTime + 0.7);
      });
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  // =========================================================================
  // 3. Canvas Astrolabe Gears & Spark Engine (60FPS)
  // =========================================================================
  function initAstrolabeCanvas() {
    const canvas = document.getElementById('hero-astrolabe-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width = 0, height = 0;
    const dustParticles = [];
    const DUST_COUNT = 45;

    function resize() {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });

    for (let i = 0; i < DUST_COUNT; i++) {
      dustParticles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.8 + 0.6,
        alpha: Math.random() * 0.6 + 0.2,
        speedX: (Math.random() - 0.5) * 0.35,
        speedY: -Math.random() * 0.45 - 0.1,
        twinkle: Math.random() * Math.PI * 2
      });
    }

    let gearAngle1 = 0;
    let gearAngle2 = 0;

    function drawGear(cx, cy, radius, teeth, depth, angle, color) {
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
        const rIn = radius - depth;
        if (i === 0) ctx.moveTo(Math.cos(a1) * rIn, Math.sin(a1) * rIn);
        else ctx.lineTo(Math.cos(a1) * rIn, Math.sin(a1) * rIn);
        ctx.lineTo(Math.cos(a2) * radius, Math.sin(a2) * radius);
        ctx.lineTo(Math.cos(a3) * radius, Math.sin(a3) * radius);
        ctx.lineTo(Math.cos(a4) * rIn, Math.sin(a4) * rIn);
      }
      ctx.closePath();
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.2;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(0, 0, radius * 0.3, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }

    function render() {
      ctx.clearRect(0, 0, width, height);

      // 1. Draw Gold Dust
      dustParticles.forEach(p => {
        p.x += p.speedX;
        p.y += p.speedY;
        p.twinkle += 0.02;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.twinkle));
        if (p.y < -10) { p.y = height + 10; p.x = Math.random() * width; }
        if (p.x < -10) p.x = width + 10;
        if (p.x > width + 10) p.x = -10;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 230, 130, ${Math.max(0, currentAlpha)})`;
        ctx.fill();
      });

      // 2. Draw Astrolabe Gears
      const isMobile = width < 768;
      const cx = isMobile ? width * 0.5 : width * 0.75;
      const cy = isMobile ? height * 0.6 : height * 0.5;

      gearAngle1 += 0.0025;
      gearAngle2 -= 0.0035;

      // Outer delicate armillary rings
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(gearAngle1 * 0.5);
      const rOuter = isMobile ? 180 : 280;
      ctx.beginPath();
      ctx.arc(0, 0, rOuter, 0, Math.PI * 2);
      ctx.strokeStyle = 'rgba(255, 215, 0, 0.22)';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Degree tick marks
      for (let i = 0; i < 36; i++) {
        const a = (i * Math.PI * 2) / 36;
        const len = i % 3 === 0 ? 12 : 6;
        ctx.beginPath();
        ctx.moveTo(Math.cos(a) * (rOuter - len), Math.sin(a) * (rOuter - len));
        ctx.lineTo(Math.cos(a) * rOuter, Math.sin(a) * rOuter);
        ctx.strokeStyle = i % 3 === 0 ? 'rgba(255, 230, 130, 0.55)' : 'rgba(255, 215, 0, 0.2)';
        ctx.lineWidth = 1.2;
        ctx.stroke();
      }
      ctx.restore();

      // Inner Interlocking Gears
      drawGear(cx, cy, isMobile ? 120 : 190, 24, 12, gearAngle1, 'rgba(255, 215, 0, 0.3)');
      drawGear(cx - (isMobile ? 130 : 200), cy - 60, isMobile ? 70 : 110, 16, 8, gearAngle2, 'rgba(62, 207, 191, 0.28)');

      // 3. Render Burst Sparks
      for (let i = burstParticles.length - 1; i >= 0; i--) {
        const sp = burstParticles[i];
        sp.x += sp.vx;
        sp.y += sp.vy;
        sp.vx *= 0.94;
        sp.vy *= 0.94;
        sp.alpha -= sp.decay;

        if (sp.alpha <= 0) {
          burstParticles.splice(i, 1);
        } else {
          ctx.beginPath();
          ctx.arc(sp.x, sp.y, sp.size, 0, Math.PI * 2);
          ctx.fillStyle = sp.color.replace('ALPHA', String(Math.max(0, sp.alpha)));
          ctx.shadowColor = sp.shadow;
          ctx.shadowBlur = 8;
          ctx.fill();
          ctx.shadowBlur = 0;
        }
      }

      requestAnimationFrame(render);
    }
    requestAnimationFrame(render);
  }

  // Spawn High-Energy Key Sparks on Release
  function spawnKeyBurst(originX, originY) {
    const count = 48;
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 9 + 3;
      const isCyan = Math.random() > 0.65;
      burstParticles.push({
        x: originX,
        y: originY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        size: Math.random() * 2.5 + 1.2,
        alpha: 1,
        decay: Math.random() * 0.025 + 0.015,
        color: isCyan ? 'rgba(62, 207, 191, ALPHA)' : 'rgba(255, 230, 130, ALPHA)',
        shadow: isCyan ? '#3ECFBF' : '#FFE580'
      });
    }
  }

  // =========================================================================
  // 4. Central 3D Golden Winding Key Interactive Module (zerotype Alt-Key)
  // =========================================================================
  function initWindingKey() {
    const keyBtn = document.getElementById('winding-key-btn');
    const keyObject = document.getElementById('key-object');
    const dialTicks = document.getElementById('dial-ticks');
    const dialProgress = document.getElementById('dial-progress');
    const bubbleText = document.getElementById('bubble-text');
    const cadenceVal = document.getElementById('hud-cadence-val');
    const cadenceSub = document.getElementById('key-cadence-sub');
    const statusText = document.getElementById('hud-status-text');
    const detailMsg = document.getElementById('hud-detail-msg');
    const stage = document.querySelector('.stage');

    if (!keyBtn || !keyObject) return;

    // Generate 15 Cadence Tick Marks on SVG Dial
    if (dialTicks) {
      dialTicks.innerHTML = '';
      const totalTicks = 15;
      const radius = 148;
      const cx = 160, cy = 160;
      for (let i = 0; i < totalTicks; i++) {
        const a = (i * (Math.PI * 2)) / totalTicks - Math.PI / 2;
        const x1 = cx + Math.cos(a) * (radius - 12);
        const y1 = cy + Math.sin(a) * (radius - 12);
        const x2 = cx + Math.cos(a) * radius;
        const y2 = cy + Math.sin(a) * radius;

        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'rgba(255, 215, 0, 0.35)');
        line.setAttribute('stroke-width', i === 0 ? '3' : '2');
        dialTicks.appendChild(line);
      }
    }

    let isDown = false;
    let currentAngle = 0;
    let targetAngle = 0;
    let cadence = 0;
    let lastTickAngle = 0;
    let animFrame = null;

    const DIAL_CIRCUMFERENCE = 930; // 2 * PI * 148 ≈ 930

    function updateCadenceUi() {
      const displayCadence = Math.min(15, Math.floor(cadence));
      if (cadenceVal) cadenceVal.textContent = `${String(displayCadence).padStart(2, '0')} / 15 發條蓄能`;
      if (cadenceSub) cadenceSub.textContent = `CADENCE ${String(displayCadence).padStart(2, '0')} / 15`;

      if (dialProgress) {
        const progressOffset = DIAL_CIRCUMFERENCE * (1 - displayCadence / 15);
        dialProgress.style.strokeDashoffset = progressOffset;
      }
    }

    function onStart() {
      if (isDown) return;
      isDown = true;
      keyBtn.classList.add('is-down');
      if (stage) stage.classList.add('is-winding');

      if (bubbleText) bubbleText.textContent = '發條上緊中⋯⋯ 齒輪咬合 100%';
      if (statusText) statusText.textContent = '轉動蓄力中';
      if (detailMsg) detailMsg.textContent = '長耳聽辨機關卡死異響 · 發條張力持續攀升';

      playTickSound(1000 + cadence * 40);

      function windLoop() {
        if (!isDown) return;
        targetAngle += 2.8; // Rotate speed
        currentAngle += (targetAngle - currentAngle) * 0.4;
        keyObject.style.transform = `rotate(${currentAngle.toFixed(1)}deg)`;

        // Ratchet tick every 24 degrees
        if (currentAngle - lastTickAngle >= 24) {
          lastTickAngle = currentAngle;
          if (cadence < 15) {
            cadence = Math.min(15, cadence + 1);
            playTickSound(1200 + cadence * 65);
            updateCadenceUi();

            if (cadence === 15) {
              if (bubbleText) bubbleText.textContent = '滿鍊蓄力完成！放開以釋放發條心臟！';
              if (statusText) statusText.textContent = 'MAX 滿鍊就緒';
            }
          }
        }
        animFrame = requestAnimationFrame(windLoop);
      }
      animFrame = requestAnimationFrame(windLoop);
    }

    function onRelease() {
      if (!isDown) return;
      isDown = false;
      keyBtn.classList.remove('is-down');
      if (stage) stage.classList.remove('is-winding');
      if (animFrame) cancelAnimationFrame(animFrame);

      const rect = keyBtn.getBoundingClientRect();
      const originX = rect.left + rect.width / 2;
      const originY = rect.top + rect.height / 2;

      if (cadence > 0) {
        // Trigger celebration & release
        playReleaseChime();
        spawnKeyBurst(originX, originY);

        if (bubbleText) bubbleText.textContent = '發條扣緊！心臟開始跳動 · 能量共鳴！';
        if (statusText) statusText.textContent = '心臟全速跳動中';
        if (detailMsg) detailMsg.textContent = '15/15 發條體力全滿載 · 聽聲拆件戰鬥啟動！';

        // Spin back with inertia
        targetAngle += 360;
        let snapFrames = 0;
        function spinRelease() {
          if (snapFrames < 35) {
            currentAngle += (targetAngle - currentAngle) * 0.18;
            keyObject.style.transform = `rotate(${currentAngle.toFixed(1)}deg)`;
            snapFrames++;
            requestAnimationFrame(spinRelease);
          }
        }
        requestAnimationFrame(spinRelease);

        // Keep cadence fully wound for a rewarding feel, then relax
        cadence = 15;
        updateCadenceUi();
      } else {
        if (bubbleText) bubbleText.textContent = '按住鑰匙上鍊';
        if (statusText) statusText.textContent = '待命上鍊';
      }
    }

    // Pointer events on key
    keyBtn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      onStart();
    });

    window.addEventListener('pointerup', onRelease);
    window.addEventListener('pointercancel', onRelease);

    // Keyboard Spacebar integration
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && !e.repeat && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        const overview = document.getElementById('overview');
        if (!overview) return;
        const rect = overview.getBoundingClientRect();
        if (rect.bottom > 100 && rect.top < window.innerHeight) {
          e.preventDefault();
          onStart();
        }
      }
    });

    window.addEventListener('keyup', (e) => {
      if (e.code === 'Space') {
        onRelease();
      }
    });

    // Initialize UI
    updateCadenceUi();

    // Automation helpers for testing & QA verification
    window.testWindFull = function () {
      isDown = true;
      keyBtn.classList.add('is-down');
      if (stage) stage.classList.add('is-winding');
      cadence = 15;
      targetAngle = 360;
      currentAngle = 360;
      keyObject.style.transform = 'rotate(360deg)';
      updateCadenceUi();
      if (bubbleText) bubbleText.textContent = '滿鍊蓄力完成！放開以釋放發條心臟！';
      if (statusText) statusText.textContent = 'MAX 滿鍊就緒';
      if (detailMsg) detailMsg.textContent = '長耳聽辨機關卡死異響 · 15 點發條蓄滿！';
      playTickSound(2100);
    };

    window.testRelease = function () {
      onRelease();
    };
  }

  // =========================================================================
  // 5. Thirteen Clockwork Races Interactive Showcase
  // =========================================================================
  function initRacesShowcase() {
    const rail = document.getElementById('race-nav-rail');
    if (!rail) return;

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

    document.addEventListener('keydown', (e) => {
      const raceSec = document.getElementById('races');
      if (!raceSec) return;
      const rect = raceSec.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        if (e.key === 'ArrowLeft') {
          const nextIdx = (currentRaceIdx - 1 + RACES_DATA.length) % RACES_DATA.length;
          switchRace(nextIdx);
        } else if (e.key === 'ArrowRight') {
          const nextIdx = (currentRaceIdx + 1) % RACES_DATA.length;
          switchRace(nextIdx);
        }
      }
    });

    updateRaceStage(0, false);
  }

  function switchRace(idx) {
    if (idx === currentRaceIdx) return;
    currentRaceIdx = idx;
    playTickSound(1400);

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

    const idxBig = document.getElementById('stage-race-idx');
    const nameEl = document.getElementById('stage-race-name');
    const roleEl = document.getElementById('stage-race-role');
    const quoteEl = document.getElementById('stage-race-quote');
    const descEl = document.getElementById('stage-race-desc');
    const weaponNameEl = document.getElementById('stage-weapon-name');
    const weaponDescEl = document.getElementById('stage-weapon-desc');
    const mainImgEl = document.getElementById('stage-main-img');
    const pixelImgEl = document.getElementById('stage-pixel-img');

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
      mainImgEl.style.transform = 'scale(0.92) translateY(10px)';
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

      if (barBreak) barBreak.style.width = `${data.breakRate}%`;
      if (barAgility) barAgility.style.width = `${data.agility}%`;
      if (barDef) barDef.style.width = `${data.defense}%`;

      if (valBreak) valBreak.textContent = `${data.breakRate}%`;
      if (valAgility) valAgility.textContent = `${data.agility}%`;
      if (valDef) valDef.textContent = `${data.defense}%`;

      if (weaknessEl) weaknessEl.textContent = data.weakness;
      if (traitEl) traitEl.textContent = data.trait;
      if (matEl) matEl.textContent = data.material;
    }, animate ? 140 : 0);
  }

  // =========================================================================
  // 6. 3D Tilt Parallax Cards (Core Pillars)
  // =========================================================================
  function init3DTiltCards() {
    const cards = document.querySelectorAll('.aww-tilt-card');
    if (!cards.length) return;

    cards.forEach((card) => {
      let bounds = null;

      card.addEventListener('mouseenter', () => {
        bounds = card.getBoundingClientRect();
      });

      card.addEventListener('mousemove', (e) => {
        if (!bounds) bounds = card.getBoundingClientRect();
        const mouseX = e.clientX - bounds.left;
        const mouseY = e.clientY - bounds.top;

        const xPct = (mouseX / bounds.width - 0.5) * 2;
        const yPct = (mouseY / bounds.height - 0.5) * 2;

        const rotateX = -yPct * 8;
        const rotateY = xPct * 8;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;
      });

      card.addEventListener('mouseleave', () => {
        bounds = null;
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
      });
    });
  }

  // =========================================================================
  // 7. Cinematic Theater Switcher
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
  // 8. Navigation Bar & Mobile Menu
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
  // 9. Scroll Reveal Observer
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
      rootMargin: '60px 0px 60px 0px'
    });

    revealElements.forEach((el) => observer.observe(el));
  }

  // =========================================================================
  // Bootstrap
  // =========================================================================
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  function initAll() {
    initAudioEngine();
    initAstrolabeCanvas();
    initWindingKey();
    initRacesShowcase();
    init3DTiltCards();
    initTheaterSwitcher();
    initNavigation();
    initScrollReveal();
  }

})();
