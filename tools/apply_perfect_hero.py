#!/usr/bin/env python3

with open("/opt/side/bravesoul-game/web/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the hero centerpiece from <div class="aww-keycap-stage ... to </div></div>
start_marker = '<!-- ==================================================================='
end_marker = '<!-- Feature Pillars Tags -->'

hero_component = """<!-- ===================================================================
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

        """

p1 = html.find(start_marker)
p2 = html.find(end_marker)

if p1 != -1 and p2 != -1:
    new_html = html[:p1] + hero_component + html[p2:]
    with open("/opt/side/bravesoul-game/web/index.html", "w", encoding="utf-8") as f:
        f.write(new_html)
    print("Perfect Hero integrated successfully!")
else:
    print("Markers not found:", p1, p2)
