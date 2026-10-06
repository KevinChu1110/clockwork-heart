#!/usr/bin/env python3

CSS_APPEND = """
/* ==========================================================================
   Tactile Physical Winding Key Centerpiece (Zerotype Keycap Architecture)
   ========================================================================== */
.aww-keycap-stage {
  position: relative;
  width: 100%;
  max-width: 900px;
  margin: 1.5rem auto 2.5rem;
  perspective: 1200px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.keycap-perspective-container {
  position: relative;
  background: rgba(14, 14, 18, 0.75);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  padding: 3rem 2rem 2.5rem;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.12),
    inset 0 -1px 0 rgba(0, 0, 0, 0.5),
    0 30px 80px rgba(0, 0, 0, 0.8),
    0 0 40px rgba(229, 195, 104, 0.06);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease;
  transform-style: preserve-3d;
  width: 100%;
}

.keycap-ambient-glow {
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 360px;
  height: 360px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(229, 195, 104, 0.14) 0%, rgba(62, 207, 191, 0.08) 40%, transparent 70%);
  filter: blur(40px);
  pointer-events: none;
  z-index: 0;
  transition: opacity 0.5s ease;
}

/* The Pedestal Base */
.keycap-pedestal {
  position: relative;
  z-index: 2;
  width: 340px;
  height: 340px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  background: radial-gradient(circle at 45% 40%, #1A1822 0%, #0D0C12 60%, #060608 100%);
  border: 2px solid rgba(229, 195, 104, 0.3);
  box-shadow:
    inset 0 2px 6px rgba(255, 255, 255, 0.2),
    inset 0 -4px 12px rgba(0, 0, 0, 0.9),
    0 20px 50px rgba(0, 0, 0, 0.9),
    0 0 30px rgba(229, 195, 104, 0.15);
  transform-style: preserve-3d;
}

.keycap-dial {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.keycap-dial-svg {
  width: 100%;
  height: 100%;
}
.dial-outer-rim {
  fill: none;
  stroke: rgba(229, 195, 104, 0.25);
  stroke-width: 1.5;
}
.dial-track {
  fill: none;
  stroke: rgba(255, 255, 255, 0.05);
  stroke-width: 8;
}
.dial-inner-groove {
  fill: none;
  stroke: rgba(0, 0, 0, 0.6);
  stroke-width: 2;
}

.dial-tick-line {
  stroke: rgba(229, 195, 104, 0.3);
  stroke-width: 1.5;
  transition: stroke 0.2s ease;
}
.dial-tick-dot {
  fill: rgba(255, 255, 255, 0.2);
  transition: fill 0.2s ease, r 0.2s ease, filter 0.2s ease;
}
.dial-tick-dot.is-lit {
  fill: var(--cyan-core);
  filter: drop-shadow(0 0 6px var(--cyan-core));
}

.keycap-socket {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, #050507 0%, #0A0910 80%, #15131C 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow:
    inset 0 6px 16px rgba(0, 0, 0, 0.95),
    inset 0 1px 3px rgba(0, 0, 0, 1),
    0 2px 8px rgba(229, 195, 104, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.socket-glow-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 1.5px solid transparent;
  box-shadow: 0 0 16px rgba(62, 207, 191, 0.2);
  transition: opacity 0.3s ease;
  pointer-events: none;
}
.socket-glow-ring.is-active {
  border-color: var(--cyan-core);
  box-shadow: 0 0 24px var(--cyan-core), inset 0 0 12px var(--cyan-core);
}

.socket-hole {
  width: 24px;
  height: 48px;
  background: #020203;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.9);
  box-shadow: inset 0 0 8px #000;
}

/* The Physical Brass Winding Key */
.physical-key {
  position: relative;
  z-index: 5;
  width: 240px;
  height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  user-select: none;
  -webkit-user-select: none;
  outline: none;
  transition: transform 0.18s cubic-bezier(0.18, 0.89, 0.32, 1.28);
  will-change: transform;
}
.physical-key:active {
  cursor: grabbing;
}
.physical-key.is-winding {
  transition: transform 0.1s linear;
}
.physical-key.is-releasing {
  transition: transform 1.2s cubic-bezier(0.15, 1, 0.3, 1);
}

.key-wings {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 16px 24px rgba(0, 0, 0, 0.85));
}

.key-wing {
  position: relative;
  width: 90px;
  height: 110px;
  background: linear-gradient(135deg, #FFF8DC 0%, #E8CB72 20%, #C4982A 50%, #7A5712 80%, #F5DE98 100%);
  border: 1.5px solid #FFEAA5;
  box-shadow:
    inset 0 2px 4px rgba(255, 255, 255, 0.6),
    inset 0 -3px 6px rgba(0, 0, 0, 0.5),
    0 4px 12px rgba(0, 0, 0, 0.5);
  border-radius: 50% 50% 45% 45% / 60% 60% 40% 40%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.key-wing--left {
  transform: rotate(-18deg) translateX(4px);
  border-top-left-radius: 55%;
}
.key-wing--right {
  transform: rotate(18deg) translateX(-4px);
  border-top-right-radius: 55%;
}

.wing-inner-cutout {
  width: 44px;
  height: 60px;
  background: radial-gradient(circle, #0A0910 0%, #1C1924 100%);
  border: 2px solid rgba(120, 86, 18, 0.9);
  border-radius: 50%;
  box-shadow:
    inset 0 4px 10px rgba(0, 0, 0, 0.9),
    0 1px 2px rgba(255, 255, 255, 0.4);
}

.key-hub {
  position: relative;
  z-index: 6;
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 35%, #FFF0B2 0%, #E0BC58 35%, #9E7418 70%, #5E4108 100%);
  border: 2px solid #FFF8D6;
  box-shadow:
    inset 0 2px 5px rgba(255, 255, 255, 0.8),
    inset 0 -3px 8px rgba(0, 0, 0, 0.7),
    0 8px 20px rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}
.hub-ring {
  position: absolute;
  inset: 6px;
  border-radius: 50%;
  border: 1px dashed rgba(80, 50, 8, 0.6);
}

.hub-heart-gem {
  position: relative;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #A2FFF5 0%, #3ECFBF 40%, #157A6E 80%, #0A423C 100%);
  border: 1.5px solid #C4FFF8;
  box-shadow:
    0 0 14px var(--cyan-core),
    inset 0 1px 3px rgba(255, 255, 255, 0.8),
    inset 0 -2px 4px rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.gem-pulse-core {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #FFF;
  box-shadow: 0 0 8px #FFF, 0 0 16px var(--cyan-core);
}
.hub-heart-gem.is-pulsing {
  animation: keyHeartbeat 1s infinite cubic-bezier(0.2, 0.8, 0.2, 1);
}
@keyframes keyHeartbeat {
  0% { transform: scale(1); filter: drop-shadow(0 0 8px var(--cyan-core)); }
  15% { transform: scale(1.22); filter: drop-shadow(0 0 24px #3ECFBF) brightness(1.3); }
  30% { transform: scale(1.05); }
  45% { transform: scale(1.18); filter: drop-shadow(0 0 20px #3ECFBF) brightness(1.2); }
  60% { transform: scale(1); filter: drop-shadow(0 0 8px var(--cyan-core)); }
  100% { transform: scale(1); }
}

.key-sparks-container {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 10;
  overflow: visible;
}
.key-spark {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #FFE580;
  box-shadow: 0 0 6px #FFE580, 0 0 10px #FFF;
  pointer-events: none;
  animation: sparkFly 0.6s cubic-bezier(0.1, 0.8, 0.3, 1) forwards;
}
@keyframes sparkFly {
  0% { opacity: 1; transform: translate(0, 0) scale(1); }
  100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(0); }
}

/* Interactive HUD Controller & Cadence Bar */
.keycap-hud {
  width: 100%;
  max-width: 620px;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  background: rgba(8, 8, 12, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 1.5rem 1.8rem;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08), 0 12px 30px rgba(0, 0, 0, 0.5);
}

.keycap-hud-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}
.hud-status-indicator {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}
.hud-status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--gold-primary);
  box-shadow: 0 0 8px var(--gold-primary);
  transition: background 0.3s ease, box-shadow 0.3s ease;
}
.hud-status-dot.is-active {
  background: var(--cyan-core);
  box-shadow: 0 0 12px var(--cyan-core);
  animation: cyanPulse 1.2s infinite ease-in-out;
}
.hud-status-label {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--ivory-dim);
}

.hud-metric-box {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}
.hud-metric-title {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: rgba(229, 195, 104, 0.7);
  text-transform: uppercase;
}
.hud-metric-number {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 800;
  color: #FFF;
}
.hud-metric-number small {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--ivory-muted);
}

.keycap-cadence-meter {
  display: grid;
  grid-template-columns: repeat(15, 1fr);
  gap: 5px;
  width: 100%;
  height: 10px;
}
.cadence-segment {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: background 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, transform 0.2s ease;
}
.cadence-segment.is-active {
  background: linear-gradient(180deg, #FFE580 0%, #E5C368 100%);
  box-shadow: 0 0 8px rgba(229, 195, 104, 0.6);
  transform: translateY(-1px);
}
.cadence-segment.is-full {
  background: linear-gradient(180deg, #A2FFF5 0%, #3ECFBF 100%);
  box-shadow: 0 0 10px rgba(62, 207, 191, 0.8);
}

.keycap-action-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
}
.btn-micro-key {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(18, 18, 24, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: var(--ivory-dim);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-micro-key:hover {
  background: rgba(229, 195, 104, 0.15);
  border-color: var(--gold-primary);
  color: #FFF;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), 0 0 10px rgba(229, 195, 104, 0.2);
}
.btn-micro-key:active {
  transform: translateY(1px);
}
.btn-micro-key--release {
  background: rgba(62, 207, 191, 0.12);
  border-color: rgba(62, 207, 191, 0.35);
  color: var(--cyan-core);
}
.btn-micro-key--release:hover {
  background: rgba(62, 207, 191, 0.25);
  border-color: var(--cyan-core);
  color: #FFF;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 0 16px rgba(62, 207, 191, 0.4);
}

.keycap-companion-badge {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  background: rgba(12, 12, 16, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 0.6rem 1rem;
  width: 100%;
}
.companion-avatar {
  width: 38px;
  height: 38px;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.8));
}
.companion-info {
  display: flex;
  flex-direction: column;
  text-align: left;
}
.companion-name {
  font-family: var(--font-serif);
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--ivory-white);
  letter-spacing: 0.04em;
}
.companion-desc {
  font-size: 0.72rem;
  color: var(--ivory-muted);
}
"""

with open("/opt/side/bravesoul-game/web/css/awwwards.css", "a", encoding="utf-8") as f:
    f.write("""
/* 3D Winding Key Absolute Centering */
.key3d {
  position: relative;
  width: clamp(260px, 28vw, 330px);
  height: clamp(260px, 28vw, 330px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
}
.key3d__dial {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.key3d__object {
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%);
  width: 72% !important;
  height: 72% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  will-change: transform;
}
.key3d__svg {
  width: 100%;
  height: 100%;
  display: block;
}
.key3d__sub {
  position: absolute;
  bottom: -32px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.2em;
  color: var(--gold-primary);
  font-weight: 600;
  white-space: nowrap;
}
""")
print("Appended centering styles successfully!")
