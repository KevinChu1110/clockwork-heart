#!/usr/bin/env python3

with open("/opt/side/bravesoul-game/web/js/awwwards.js", "r", encoding="utf-8") as f:
    js = f.read()

start_marker = "  // =========================================================================\n  // 4. Hero Focal Object: Zerotype Tactile Physical Winding Key Micro-interaction"
end_marker = "  // =========================================================================\n  // 5. Thirteen Clockwork Races Interactive Showcase"

unified_winding_key_func = """  // =========================================================================
  // 4. Hero Focal Object: Zerotype Tactile Physical Winding Key Micro-interaction
  // =========================================================================
  function initPhysicalWindingKey() {
    const keyBtn = document.getElementById('winding-key-btn') || document.getElementById('physical-key');
    const keyObject = document.getElementById('key-object') || keyBtn;
    const dialTicks = document.getElementById('dial-ticks') || document.getElementById('dial-ticks-group');
    const dialProgress = document.getElementById('dial-progress');
    const bubbleText = document.getElementById('bubble-text') || document.getElementById('hud-status-label');
    const cadenceVal = document.getElementById('hud-cadence-val') || document.getElementById('hud-metric-number');
    const cadenceSub = document.getElementById('key-cadence-sub');
    const statusText = document.getElementById('hud-status-text');
    const detailMsg = document.getElementById('hud-detail-msg');
    const stage = document.querySelector('.stage') || document.getElementById('keycap-stage');

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
        line.setAttribute('x1', x1.toFixed(1));
        line.setAttribute('y1', y1.toFixed(1));
        line.setAttribute('x2', x2.toFixed(1));
        line.setAttribute('y2', y2.toFixed(1));
        line.setAttribute('stroke', 'rgba(255, 215, 0, 0.4)');
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
    let audioCtx = null;

    const DIAL_CIRCUMFERENCE = 930;

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

    function playTickSound(freq = 1400) {
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const t = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t);
        osc.frequency.exponentialRampToValueAtTime(320, t + 0.035);
        gain.gain.setValueAtTime(0.25, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + 0.035);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(t);
        osc.stop(t + 0.035);
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
        targetAngle += 4.2;
        currentAngle += (targetAngle - currentAngle) * 0.25;
        keyObject.style.transform = `rotate(${currentAngle.toFixed(1)}deg)`;

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

      if (cadence > 0) {
        playHeartbeatSound();
        if (typeof window._triggerAstrolabePulse === 'function') {
          window._triggerAstrolabePulse();
        }

        if (bubbleText) bubbleText.textContent = '發條扣緊！心臟開始跳動 · 能量共鳴！';
        if (statusText) statusText.textContent = '心臟全速跳動中';
        if (detailMsg) detailMsg.textContent = '15/15 發條體力全滿載 · 聽聲拆件戰鬥啟動！';

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

        cadence = 15;
        updateCadenceUi();
      } else {
        if (bubbleText) bubbleText.textContent = '按住鑰匙上鍊';
        if (statusText) statusText.textContent = '待命上鍊';
      }
    }

    keyBtn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      onStart();
    });

    window.addEventListener('pointerup', onRelease);
    window.addEventListener('pointercancel', onRelease);

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && !e.repeat && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        onStart();
      }
    });

    window.addEventListener('keyup', (e) => {
      if (e.code === 'Space') {
        onRelease();
      }
    });

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

  """

p1 = js.find(start_marker)
p2 = js.find(end_marker)

if p1 != -1 and p2 != -1:
    new_js = js[:p1] + unified_winding_key_func + js[p2:]
    with open("/opt/side/bravesoul-game/web/js/awwwards.js", "w", encoding="utf-8") as f:
        f.write(new_js)
    print("Updated awwwards.js with unified winding key module successfully!")
else:
    print("Markers not found in awwwards.js:", p1, p2)
