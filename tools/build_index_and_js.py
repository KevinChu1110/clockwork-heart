#!/usr/bin/env python3
import os

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>發條之心 (Clockwork Heart) — 橫屏動作 RPG 官方網站</title>
  <meta name="description" content="《發條之心》橫屏動作 RPG 官方網站。扮演金屬發條兔「小白」，用 15 點發條節奏打仗、聽弱點拆卸部位零件。十三發條種族開局可選，主線單機可通關，鍛造永不碎裝降階。" />
  <meta name="keywords" content="發條之心, Clockwork Heart, 發條玩具, 動作手遊, Action RPG, 部位破壞, 小白, 十三種族, Awwwards, Zerotype" />
  <meta name="theme-color" content="#070709" />
  <link rel="canonical" href="https://kevinchu1110.github.io/clockwork-heart/" />
  <link rel="alternate" type="text/plain" href="llms.txt" title="LLMs.txt" />

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="發條之心 · Clockwork Heart" />
  <meta property="og:url" content="https://kevinchu1110.github.io/clockwork-heart/" />
  <meta property="og:title" content="發條之心 — 上鍊，覺醒。放開，心臟開始跳動。" />
  <meta property="og:description" content="2.2頭身發條玩具動作 RPG。15 點發條當體力、部位拆解、十三種族開局可選、單機主線可通關。" />
  <meta property="og:image" content="https://kevinchu1110.github.io/clockwork-heart/media/hero/key_visual_greece_gears.png" />
  <meta property="og:image:alt" content="發條之心官方主視覺" />
  <meta property="og:locale" content="zh_TW" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="發條之心 — 上鍊，覺醒。放開，心臟開始跳動。" />
  <meta name="twitter:description" content="2.2頭身發條玩具動作 RPG。15 點發條當體力、部位拆解、十三種族開局可選。" />
  <meta name="twitter:image" content="https://kevinchu1110.github.io/clockwork-heart/media/hero/key_visual_greece_gears.png" />

  <!-- Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": "https://kevinchu1110.github.io/clockwork-heart/#website",
        "url": "https://kevinchu1110.github.io/clockwork-heart/",
        "name": "發條之心 (Clockwork Heart) 官方網站",
        "inLanguage": "zh-Hant"
      },
      {
        "@type": ["VideoGame", "SoftwareApplication"],
        "@id": "https://kevinchu1110.github.io/clockwork-heart/#game",
        "name": "發條之心",
        "alternateName": ["Clockwork Heart", "發條之心手遊"],
        "description": "橫屏發條玩具動作 RPG。扮演金屬發條兔「小白」，15 點發條打仗、拆敵人零件。十三發條種族開局可選，主線單機可通關。免費遊玩＋內購＋廣告。開發中。",
        "genre": ["Action RPG", "Adventure"],
        "gamePlatform": ["Android", "iOS", "PC", "Web Browser"],
        "operatingSystem": "Android, iOS, Windows, macOS, Linux",
        "applicationCategory": "GameApplication",
        "inLanguage": ["zh-Hant", "zh-Hans", "en", "ja", "ko", "es"],
        "url": "https://kevinchu1110.github.io/clockwork-heart/",
        "image": "https://kevinchu1110.github.io/clockwork-heart/media/hero/key_visual_greece_gears.png",
        "playMode": ["SinglePlayer", "MultiPlayer"],
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "TWD",
          "category": "Free to Play (F2P) with In-App Purchases"
        },
        "character": [{
          "@type": "Person",
          "name": "小白",
          "description": "可玩主角。2.2 頭身米白金屬發條玩具兔，背後有黃銅發條鑰匙，胸口有青綠發條之心，持單手長劍。"
        }],
        "author": {
          "@type": "Organization",
          "name": "發條之心團隊",
          "url": "https://kevinchu1110.github.io/clockwork-heart/"
        },
        "sameAs": [
          "https://www.facebook.com/1335191403004011",
          "https://github.com/KevinChu1110/clockwork-heart"
        ]
      }
    ]
  }
  </script>

  <!-- Typography & Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Noto+Serif+TC:wght@500;700;900&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet" />

  <!-- Unified Zerotype-Grade Dark Minimalist Stylesheet -->
  <link rel="stylesheet" href="css/awwwards.css?v=20261001-zerotype" />

  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='42' fill='%23FFD028' stroke='%231F1A3A' stroke-width='8'/><circle cx='50' cy='50' r='18' fill='%233ECFBF' stroke='%231F1A3A' stroke-width='4'/></svg>" />
</head>
<body data-page="home">

  <!-- =========================================================================
       1. Top Navigation Bar: Glassmorphic Obsidian & Antique Brass
       ========================================================================= -->
  <nav class="aww-nav" aria-label="全站主選單">
    <div class="aww-nav__inner">
      <a class="aww-brand" href="#overview" title="回到首頁頂端">
        <span class="aww-brand__mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="#E5C368" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="8"/>
            <path d="M12 2v3m0 14v3M2 12h3m14 0h3"/>
            <circle cx="12" cy="12" r="3" fill="#3ECFBF"/>
            <path d="M12 9v3l2 2"/>
          </svg>
        </span>
        <div class="aww-brand__titles">
          <span class="aww-brand__name">發條之心</span>
          <span class="aww-brand__sub">CLOCKWORK HEART</span>
        </div>
      </a>

      <ul class="aww-menu" id="aww-menu">
        <li><a class="aww-menu__link active" href="#overview">世界觀</a></li>
        <li><a class="aww-menu__link" href="#races">十三種族</a></li>
        <li><a class="aww-menu__link" href="#pillars">核心三柱</a></li>
        <li><a class="aww-menu__link" href="#theater">神殿劇院</a></li>
        <li><a class="aww-menu__link" href="#download">預約下載</a></li>
        <li><a class="aww-menu__link" href="pages/guide.html">新手指南</a></li>
      </ul>

      <div class="aww-nav__actions">
        <a class="btn-jelly-gold" href="pages/download.html">
          <span>立即試玩</span>
          <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v7.586l2.293-2.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 11.586V4a1 1 0 011-1zM4 17a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1z" clip-rule="evenodd" />
          </svg>
        </a>
        <button type="button" class="aww-toggle" id="aww-toggle" aria-label="切換導航選單" aria-expanded="false" aria-controls="aww-menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>

  <main>
    <!-- =========================================================================
         2. Fullscreen Immersive Hero Section (對標 zerotype.ai 頂級暗黑極簡)
         ========================================================================= -->
    <header class="aww-hero" id="overview">
      <!-- 60FPS Canvas Golden Astrolabe & Gold Dust Background -->
      <canvas id="hero-astrolabe-canvas" class="aww-hero__canvas"></canvas>
      <div class="aww-hero__vignette"></div>

      <div class="aww-hero__container">
        <!-- Zerotype Typography Header -->
        <div class="aww-hero__zerotype-header reveal-fade-up">
          <div class="aww-badge-gold">
            <span class="aww-badge-gold__dot"></span>
            ZEROTYPE AESTHETIC SYSTEM · CLOCKWORK HEART
          </div>

          <h1 class="aww-hero__main-title">
            <span class="title-row">上鍊，覺醒。</span>
            <span class="title-row title-row--gold">放開，心臟開始跳動。</span>
          </h1>

          <div class="aww-hero__subtitle-en">
            WIND THE KEY, AWAKEN THE SOUL · RELEASE, AND THE HEART BEGINS TO BEAT
          </div>

          <p class="aww-hero__lead">
            2.2 頭身金屬發條玩具 × 15 點發條律動 × 部位破壞拆解。零毛皮、純機械板件與黃銅發條鑰匙的覺醒玩具世界。
          </p>
        </div>

        <!-- ===================================================================
             Hero Focal Object: 擬真 3D 實體發條鑰匙微交互裝置 (如 zerotype 鍵帽)
             =================================================================== -->
        <div class="stage reveal-fade-up" data-stage>
          <div class="stage__bubble" id="key-hint" aria-live="polite">
            <span class="stage__bubble-icon" aria-hidden="true">⚙</span>
            <span class="stage__bubble-text" id="bubble-text">按住鑰匙上鍊</span>
            <span class="stage__bubble-alt">（或長按空白鍵）</span>
          </div>

          <div class="keywrap">
            <button class="key3d" type="button" id="winding-key-btn" aria-describedby="key-hint" aria-label="實體黃金發條鑰匙：按住上鍊，放開釋放">
              <div class="key3d__glow" aria-hidden="true"></div>

              <!-- Outer Astrolabe Cadence Dial Ring -->
              <svg class="key3d__dial" viewBox="0 0 320 320" aria-hidden="true">
                <circle cx="160" cy="160" r="148" class="dial-track" />
                <circle cx="160" cy="160" r="148" class="dial-progress" id="dial-progress" />
                <g class="dial-ticks" id="dial-ticks">
                  <!-- 15 Cadence Tick Marks generated dynamically -->
                </g>
              </svg>

              <!-- Physical 3D Golden Winding Key -->
              <div class="key3d__object" id="key-object">
                <svg viewBox="0 0 240 240" class="key3d__svg" aria-hidden="true">
                  <defs>
                    <linearGradient id="brassGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#FFF8DC"/>
                      <stop offset="20%" stop-color="#E8CB72"/>
                      <stop offset="50%" stop-color="#C4982A"/>
                      <stop offset="80%" stop-color="#7A5712"/>
                      <stop offset="100%" stop-color="#F5DE98"/>
                    </linearGradient>
                    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#A2FFF5"/>
                      <stop offset="45%" stop-color="#3ECFBF"/>
                      <stop offset="100%" stop-color="#0A423C"/>
                    </linearGradient>
                    <filter id="keyShadow" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="12" stdDeviation="10" flood-color="#000" flood-opacity="0.85"/>
                    </filter>
                  </defs>
                  
                  <g filter="url(#keyShadow)">
                    <!-- Left Wing -->
                    <path d="M 110,95 C 65,45 15,55 15,120 C 15,185 65,195 110,145 Z" fill="url(#brassGrad)" stroke="#FFEAA5" stroke-width="2"/>
                    <path d="M 98,102 C 68,68 38,72 38,120 C 38,168 68,172 98,138 Z" fill="#0A0910" stroke="#8A6618" stroke-width="2"/>

                    <!-- Right Wing -->
                    <path d="M 130,95 C 175,45 225,55 225,120 C 225,185 175,195 130,145 Z" fill="url(#brassGrad)" stroke="#FFEAA5" stroke-width="2"/>
                    <path d="M 142,102 C 172,68 202,72 202,120 C 202,168 172,172 142,138 Z" fill="#0A0910" stroke="#8A6618" stroke-width="2"/>

                    <!-- Key Stem / Shaft -->
                    <rect x="108" y="145" width="24" height="48" rx="4" fill="url(#brassGrad)" stroke="#FFEAA5" stroke-width="1.5"/>
                    <rect x="102" y="172" width="36" height="8" rx="2" fill="#D4AF37" stroke="#7A5712" stroke-width="1"/>

                    <!-- Center Hub -->
                    <circle cx="120" cy="120" r="32" fill="url(#brassGrad)" stroke="#FFF8D6" stroke-width="2.5"/>
                    <circle cx="120" cy="120" r="26" fill="none" stroke="#684A10" stroke-width="1" stroke-dasharray="3,3"/>
                    
                    <!-- Cyan Heart Gem Core -->
                    <circle cx="120" cy="120" r="16" fill="url(#coreGrad)" stroke="#C4FFF8" stroke-width="2"/>
                    <circle cx="120" cy="120" r="6" fill="#FFFFFF" opacity="0.9"/>
                  </g>
                </svg>
              </div>

              <!-- Cadence Sub-label -->
              <span class="key3d__sub" id="key-cadence-sub">CADENCE 00 / 15</span>
              <span class="key3d__led" id="key-led" aria-hidden="true"></span>
            </button>
          </div>

          <!-- Bottom HUD Controller Panel -->
          <div class="hud" role="status">
            <div class="hud__pill">
              <span class="hud__dot" aria-hidden="true"></span>
              <span class="hud__val" id="hud-cadence-val">00 / 15 發條蓄能</span>
            </div>
            <div class="hud__meter">
              <span class="hud__meter-label" id="hud-status-text">待命上鍊</span>
              <span class="hud__msg" id="hud-detail-msg">長按鑰匙旋轉扣緊齒輪，放開即刻釋放動能</span>
            </div>
            <div class="hud__stats">
              <span class="hud-stat">咬合率 100%</span>
              <span class="hud-stat">聲音定位 READY</span>
            </div>
          </div>
        </div>

        <!-- Feature Pillars Tags -->
        <div class="aww-hero__tags reveal-fade-up">
          <span class="aww-hero__tag"><span class="aww-hero__tag-icon">✦</span>單機主線可通關</span>
          <span class="aww-hero__tag"><span class="aww-hero__tag-icon">✦</span>15 點發條當體力</span>
          <span class="aww-hero__tag"><span class="aww-hero__tag-icon">✦</span>部位拆解裝甲</span>
          <span class="aww-hero__tag"><span class="aww-hero__tag-icon">✦</span>十三專屬種族</span>
          <span class="aww-hero__tag"><span class="aww-hero__tag-icon">✦</span>鍛造失敗不降階</span>
        </div>

        <!-- Hero Actions -->
        <div class="aww-hero__actions reveal-fade-up">
          <a href="#races" class="btn-jelly-gold">
            <span>探索十三種族展台</span>
            <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
              <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </a>
          <a href="#theater" class="btn-obsidian-gold">
            <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <span>觀看神殿劇院實機</span>
          </a>
          <a href="pages/download.html" class="btn-pillar-link">PC 測試包</a>
        </div>

        <!-- Bottom Scroll Indicator -->
        <a href="#races" class="aww-scroll-cue" aria-label="向下捲動探索十三種族">
          <span class="aww-scroll-cue__text">EXPLORE ARCHIVE</span>
          <div class="aww-scroll-cue__icon">
            <div class="aww-scroll-cue__wheel"></div>
          </div>
        </a>
      </div>
    </header>

    <!-- =========================================================================
         3. Thirteen Clockwork Races Interactive Showcase
         Unified Dark Glassmorphism Specification
         ========================================================================= -->
    <section class="aww-races-section" id="races">
      <div class="aww-section-header reveal-fade-up">
        <div class="aww-section-header__kicker">№ 02 · CLOCKWORK CAST SHOWCASE</div>
        <h2 class="aww-section-header__title">十三發條種族互動陳列室</h2>
        <p class="aww-section-header__lead">
          2.2 頭身純金屬機械玩具世界。零毛皮、全金屬板件與黃銅發條鑰匙。開局自由啟動，每種族皆具備專屬武裝與獨門部位破壞拆解戰術：
        </p>
      </div>

      <!-- Horizontal Race Selector Rail -->
      <div class="race-nav-container reveal-fade-up">
        <div class="race-nav-rail" id="race-nav-rail" role="tablist" aria-label="十三發條種族選擇器">
          <!-- Dynamically populated by awwwards.js -->
        </div>
      </div>

      <!-- High-End Interactive Showcase Stage (Dark Glassmorphism) -->
      <div class="race-stage reveal-fade-up" id="race-stage">
        <!-- Left: Lore & Armament -->
        <div class="race-info-col">
          <div class="race-idx-big" id="stage-race-idx">№ 01 / 13</div>
          <div class="race-title-group">
            <h3 class="race-name" id="stage-race-name">白金兔 · 小白</h3>
            <span class="race-role-badge" id="stage-race-role">晨曦劍士 · 時間守護者</span>
          </div>
          <blockquote class="race-lore-quote" id="stage-race-quote">
            「齒輪咔嗒作響時，就是弱點鬆脫的一刻。」
          </blockquote>
          <p class="race-lore-desc" id="stage-race-desc">
            先行者小白經典族系，中央大鐘的時間守護者。米白金屬板件與黃銅發條鑰匙，長耳能清晰聽辨機關卡死異響，直擊敵人核心弱點。
          </p>

          <div class="race-armament-box">
            <div class="race-armament-box__title">專屬武裝體系 · SIGNATURE ARMAMENT</div>
            <div class="race-armament-box__name" id="stage-weapon-name">晨曦發條單手長劍</div>
            <p class="race-armament-box__desc" id="stage-weapon-desc">
              冷軋精鋼打造，內嵌高速離合齒輪，可在刺入瞬間高速旋轉造成破甲撕裂。
            </p>
          </div>
        </div>

        <!-- Center: Character Art Capsule (Museum-Grade Chassis, No Raw Color Blocks) -->
        <div class="race-art-col">
          <div class="race-art-ring" aria-hidden="true"></div>
          <div class="race-art-capsule">
            <div class="race-art-capsule__tag" id="stage-capsule-tag">SPECIMEN № 01</div>
            <div class="race-art-capsule__vignette" aria-hidden="true"></div>
            <img id="stage-main-img" class="race-art-capsule__img" src="media/hero/char_rabbit.png" alt="白金兔·小白立繪展示" />
            <div class="race-pixel-badge">
              <img id="stage-pixel-img" class="race-pixel-badge__img" src="media/hero/rabbit_idle.png" alt="白金兔實機像素素體" />
              <span class="race-pixel-badge__label">實機 2.2 頭身素體</span>
            </div>
          </div>
        </div>

        <!-- Right: Specs HUD -->
        <div class="race-specs-col">
          <div class="specs-header">
            <span class="specs-header__title">機關運轉數值 · SPECS</span>
            <span class="specs-header__tag">CALIBRATION OK</span>
          </div>

          <div class="spec-bars-group">
            <div class="spec-bar-item">
              <div class="spec-bar-label-row">
                <span>發條體力儲備</span>
                <span>15 / 15</span>
              </div>
              <div class="spec-bar-track">
                <div class="spec-bar-fill" style="width: 100%;"></div>
              </div>
            </div>

            <div class="spec-bar-item">
              <div class="spec-bar-label-row">
                <span>部位破壞效率</span>
                <span id="spec-val-break">96%</span>
              </div>
              <div class="spec-bar-track">
                <div class="spec-bar-fill" id="spec-bar-break" style="width: 96%;"></div>
              </div>
            </div>

            <div class="spec-bar-item">
              <div class="spec-bar-label-row">
                <span>機構靈動度</span>
                <span id="spec-val-agility">92%</span>
              </div>
              <div class="spec-bar-track">
                <div class="spec-bar-fill" id="spec-bar-agility" style="width: 92%;"></div>
              </div>
            </div>

            <div class="spec-bar-item">
              <div class="spec-bar-label-row">
                <span>裝甲耐衝擊</span>
                <span id="spec-val-def">84%</span>
              </div>
              <div class="spec-bar-track">
                <div class="spec-bar-fill" id="spec-bar-def" style="width: 84%;"></div>
              </div>
            </div>
          </div>

          <div class="spec-trait-cards">
            <div class="spec-trait-card">
              <div class="spec-trait-card__name">機關弱點</div>
              <div class="spec-trait-card__val" id="spec-weakness-val">聽聲鎖定 (長耳精準共振)</div>
            </div>
            <div class="spec-trait-card">
              <div class="spec-trait-card__name">作戰特性</div>
              <div class="spec-trait-card__val" id="spec-trait-val">部位破壞 (零件逐塊擊落)</div>
            </div>
            <div class="spec-trait-card">
              <div class="spec-trait-card__name">機身材質</div>
              <div class="spec-trait-card__val" id="spec-material-val">鍛造米白合金板件 · 黃銅發條鑰匙 · 翡翠能量核心</div>
            </div>
          </div>

          <div class="stage-arrow-nav">
            <button type="button" class="stage-nav-btn" id="race-prev-btn" aria-label="切換至上一個種族">
              <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span>上一種族</span>
            </button>
            <button type="button" class="stage-nav-btn" id="race-next-btn" aria-label="切換至下一個種族">
              <span>下一種族</span>
              <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         4. Core Gameplay Three Pillars (Unified Dark Glassmorphism 3D Tilt Cards)
         ========================================================================= -->
    <section class="aww-pillars-section" id="pillars">
      <div class="aww-pillars-container">
        <div class="aww-section-header reveal-fade-up">
          <div class="aww-section-header__kicker">№ 03 · TRIPLE PILLARS OF COMBAT</div>
          <h2 class="aww-section-header__title">三件事就夠 · 核心玩法三柱石</h2>
          <p class="aww-section-header__lead">
            揚棄枯燥臃腫的數值堆疊，回歸純粹動作遊戲的極致樂趣。發條之心的三大核心設計：
          </p>
        </div>

        <div class="aww-pillars-grid">
          <!-- Pillar 1: 15點發條律動 -->
          <article class="aww-tilt-card reveal-fade-up">
            <div class="aww-tilt-card__visual">
              <img src="media/hero/feature_card_stamina.png" alt="發條當體力機制卡" class="aww-tilt-card__img" />
              <div class="aww-tilt-card__badge">PILLAR 01 · 體力機制</div>
            </div>
            <div class="aww-tilt-card__body">
              <h3 class="aww-tilt-card__title">15 點發條當體力，節奏自己抓</h3>
              <p class="aww-tilt-card__desc">
                普通攻擊、突刺閃避、奧義釋放皆精準消耗發條點數。轉動即是動能，歸零即刻卡死。在齒輪咬合的律動中掌控攻防呼吸節奏，告別無腦連招，體驗刀尖起舞的極致博弈。
              </p>
              <div class="aww-tilt-card__footer">
                <span>15-STEP CADENCE BAR</span>
                <span class="aww-tilt-card__icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                </span>
              </div>
            </div>
          </article>

          <!-- Pillar 2: 部位破壞拆解 -->
          <article class="aww-tilt-card reveal-fade-up">
            <div class="aww-tilt-card__visual">
              <img src="media/hero/feature_card_break.png" alt="部位破壞拆解機制卡" class="aww-tilt-card__img" />
              <div class="aww-tilt-card__badge">PILLAR 02 · 戰鬥機制</div>
            </div>
            <div class="aww-tilt-card__body">
              <h3 class="aww-tilt-card__title">聽弱點拆部位，一塊塊瓦解機關</h3>
              <p class="aww-tilt-card__desc">
                長耳辨識齒輪咬合的尖銳異響，鎖定機關卡死脆點。告別堆疊無意義的傷害數字，用劍刃直接卸除巨型機械頭目的護甲、關節與重砲，擊落零件為己所用。
              </p>
              <div class="aww-tilt-card__footer">
                <span>ACOUSTIC WEAKPOINT LOCK</span>
                <span class="aww-tilt-card__icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                </span>
              </div>
            </div>
          </article>

          <!-- Pillar 3: 神殿四大殿堂 -->
          <article class="aww-tilt-card reveal-fade-up">
            <div class="aww-tilt-card__visual">
              <img src="media/hero/feature_card_halls.png" alt="四大殿堂養成機制卡" class="aww-tilt-card__img" />
              <div class="aww-tilt-card__badge">PILLAR 03 · 深度養成</div>
            </div>
            <div class="aww-tilt-card__body">
              <h3 class="aww-tilt-card__title">四大殿堂養成，鍛造永不碎裝降階</h3>
              <p class="aww-tilt-card__desc">
                鍛造殿、聚魂殿、工坊殿、演武殿。裝備強化失敗絕不碎裝、絕不掉階；主線關卡百分之百單機可通關，無任何付費卡點，所有成長源自探索與鍛造淬火。
              </p>
              <div class="aww-tilt-card__footer">
                <span>ZERO DROP-TIER · 100% BEATABLE</span>
                <span class="aww-tilt-card__icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
                </span>
              </div>
            </div>
          </article>
        </div>

        <div class="aww-pillar-links reveal-fade-up">
          <a class="btn-pillar-link" href="pages/systems.html">系統細節</a>
          <a class="btn-pillar-link" href="pages/guide.html">新手指南</a>
          <a class="btn-pillar-link" href="pages/weapons.html">武裝圖鑑</a>
          <a class="btn-pillar-link" href="pages/download.html">下載 PC 測試包</a>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         5. Official Cinematic Theater (神殿黑曜石劇院)
         ========================================================================= -->
    <section class="aww-theater-section" id="theater">
      <div class="aww-theater-container">
        <div class="aww-section-header reveal-fade-up">
          <div class="aww-section-header__kicker">№ 04 · CINEMATIC THEATER</div>
          <h2 class="aww-section-header__title">官方短片神殿劇院</h2>
          <p class="aww-section-header__lead">
            黑曜石神殿浮雕，金屬發條與齒輪轉動的宏大篇章。切換視角欣賞精彩實機影像：
          </p>
        </div>

        <!-- Video Switcher Tabs -->
        <div class="theater-tabs reveal-fade-up">
          <button type="button" class="theater-tab-btn is-active" data-theater-mode="landscape" data-video-src="media/promo/trailer_hero_clockwork_15s.mp4">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            <span>16:9 主視覺宣傳片</span>
          </button>
          <button type="button" class="theater-tab-btn" data-theater-mode="portrait" data-video-src="media/promo/trailer_awakening_9x16.mp4">
            <svg viewBox="0 0 24 24"><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>
            <span>9:16 直式《覺醒》短片</span>
          </button>
          <button type="button" class="theater-tab-btn" data-theater-mode="landscape" data-video-src="media/shorts/mk_shorts_five_races_combat_18s.mp4">
            <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
            <span>五大種族實戰連打</span>
          </button>
        </div>

        <!-- Theater Frame -->
        <div class="theater-frame reveal-fade-up">
          <div class="theater-gear-corner theater-gear-corner--tl" aria-hidden="true"></div>
          <div class="theater-gear-corner theater-gear-corner--tr" aria-hidden="true"></div>
          <div class="theater-gear-corner theater-gear-corner--bl" aria-hidden="true"></div>
          <div class="theater-gear-corner theater-gear-corner--br" aria-hidden="true"></div>

          <!-- 16:9 Landscape Screen -->
          <div class="theater-screen-wrapper" id="theater-screen-16x9">
            <video controls playsinline preload="metadata" poster="media/hero/key_visual_greece_gears.png">
              <source src="media/promo/trailer_hero_clockwork_15s.mp4" type="video/mp4" />
              您的瀏覽器不支援 HTML5 影片播放。
            </video>
          </div>

          <!-- 9:16 Portrait Phone Chassis -->
          <div class="theater-portrait-chassis" id="theater-chassis-9x16">
            <video controls playsinline preload="metadata" poster="media/promo/trailer_awakening_9x16_poster.jpg">
              <source src="media/promo/trailer_awakening_9x16.mp4" type="video/mp4" />
              您的瀏覽器不支援 HTML5 影片播放。
            </video>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         6. Download & Community Portal
         ========================================================================= -->
    <section class="aww-download-section" id="download">
      <div class="aww-download-container">
        <div class="aww-section-header reveal-fade-up">
          <div class="aww-section-header__kicker">№ 05 · JOIN THE ADVENTURE</div>
          <h2 class="aww-section-header__title">登上方舟 · 開啟發條冒險</h2>
          <p class="aww-section-header__lead">
            單機單人完整體驗，PC 開發測試包直接免費用玩。追蹤官方社群掌握最新更新進度：
          </p>
        </div>

        <div class="aww-download-grid">
          <!-- PC Download Card -->
          <article class="aww-dl-card reveal-fade-up">
            <div class="aww-dl-card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zM4 6h16v10H4V6z"/></svg>
            </div>
            <h3 class="aww-dl-card__title">PC 開發測試包</h3>
            <p class="aww-dl-card__desc">
              支援 Windows 64-bit 系統，完美適配鍵盤滑鼠與 Xbox / PlayStation 控制手把。
            </p>
            <a href="pages/download.html" class="btn-jelly-gold">
              <span>前往下載</span>
              <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
                <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </a>
          </article>

          <!-- Facebook Community Card -->
          <article class="aww-dl-card reveal-fade-up">
            <div class="aww-dl-card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.34L15.89 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z"/></svg>
            </div>
            <h3 class="aww-dl-card__title">官方 Facebook 粉專</h3>
            <p class="aww-dl-card__desc">
              開發團隊即時回報製作進度、更新日誌、種族設計草稿與社群互動反饋。
            </p>
            <a href="https://www.facebook.com/1335191403004011" target="_blank" rel="noopener" class="btn-obsidian-gold">
              <span>追蹤官方粉專</span>
              <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/>
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/>
              </svg>
            </a>
          </article>

          <!-- GitHub Open Source Card -->
          <article class="aww-dl-card reveal-fade-up">
            <div class="aww-dl-card__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
            </div>
            <h3 class="aww-dl-card__title">GitHub 開發庫</h3>
            <p class="aww-dl-card__desc">
              純粹開放的遊戲開發歷程，包含 Godot 4 引擎架構、數值設定檔與技術文件。
            </p>
            <a href="https://github.com/KevinChu1110/clockwork-heart" target="_blank" rel="noopener" class="btn-obsidian-gold">
              <span>檢視 GitHub</span>
              <svg viewBox="0 0 20 20" width="16" height="16" fill="currentColor">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z"/>
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z"/>
              </svg>
            </a>
          </article>
        </div>
      </div>
    </section>
  </main>

  <!-- =========================================================================
       7. Master Obsidian Luxury Footer
       ========================================================================= -->
  <footer class="aww-footer">
    <div class="aww-footer-inner">
      <div class="aww-footer-top">
        <a class="aww-brand" href="#overview">
          <span class="aww-brand__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="#E5C368" stroke-width="2.2">
              <circle cx="12" cy="12" r="8"/>
              <circle cx="12" cy="12" r="3" fill="#3ECFBF"/>
            </svg>
          </span>
          <div class="aww-brand__titles">
            <span class="aww-brand__name">發條之心 · CLOCKWORK HEART</span>
            <span class="aww-brand__sub">2.2頭身發條玩具動作 RPG</span>
          </div>
        </a>

        <div class="aww-footer-links">
          <a href="#overview">世界觀</a>
          <a href="#races">十三種族</a>
          <a href="#pillars">核心玩法</a>
          <a href="#theater">神殿劇院</a>
          <a href="pages/guide.html">新手指南</a>
          <a href="pages/systems.html">系統細節</a>
          <a href="pages/download.html">下載中心</a>
          <a href="pages/account.html">玩家帳號</a>
        </div>
      </div>

      <div class="aww-footer-bottom">
        <p class="aww-footer-copy">© 2026 發條之心 (Clockwork Heart). 保留所有權利。零毛皮、純機械板件玩具世界。</p>
        <span class="aww-footer-stamp">BUILD: 2026.10-ZEROTYPE-AWWWARDS-EDITION · 60FPS</span>
      </div>
    </div>
  </footer>

  <!-- Unified Interactive Engine -->
  <script src="js/awwwards.js?v=20261001-zerotype"></script>
</body>
</html>
"""

print("Building Zerotype index.html...")
with open("/opt/side/bravesoul-game/web/index.html", "w", encoding="utf-8") as f:
    f.write(INDEX_HTML)
print("Updated web/index.html successfully!")
