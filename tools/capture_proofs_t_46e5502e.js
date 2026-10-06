const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT_DIR = '/opt/side/bravesoul-game/proofs/t_46e5502e';
fs.mkdirSync(OUT_DIR, { recursive: true });

async function run() {
  console.log('Launching headless Chrome...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  // 1. Desktop Context
  const desktopContext = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await desktopContext.newPage();

  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER ERROR:', err));

  console.log('Navigating to http://localhost:8089/...');
  await page.goto('http://localhost:8089/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Reveal all animations immediately
  await page.evaluate(() => {
    document.querySelectorAll('.reveal-fade-up').forEach(el => el.classList.add('is-revealed'));
  });

  // Shot 1: Hero Idle
  console.log('Capturing 01_hero_zerotype_idle.png...');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '01_hero_zerotype_idle.png') });

  // Shot 2: Hero Winding Active (Wind to 15/15)
  console.log('Capturing 02_hero_key_winding_active.png...');
  await page.locator('#btn-wind-full').click();
  await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(OUT_DIR, '02_hero_key_winding_active.png') });

  // Shot 3: Hero Heartbeat Released
  console.log('Capturing 03_hero_key_heartbeat_release.png...');
  await page.locator('#btn-wind-release').click();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT_DIR, '03_hero_key_heartbeat_release.png') });

  // Shot 4: Thirteen Races Showcase (Rabbit)
  console.log('Capturing 04_races_showcase_rabbit.png...');
  await page.evaluate(() => {
    document.getElementById('races').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '04_races_showcase_rabbit.png') });

  // Shot 5: Races Showcase (Lion)
  console.log('Capturing 05_races_showcase_lion.png...');
  await page.locator('.race-nav-btn').nth(1).click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '05_races_showcase_lion.png') });

  // Shot 6: Races Showcase (Panda)
  console.log('Capturing 06_races_showcase_panda.png...');
  await page.locator('.race-nav-btn').nth(12).click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '06_races_showcase_panda.png') });

  // Shot 7: Core Pillars (Dark Glassmorphism)
  console.log('Capturing 07_core_pillars_dark_glass.png...');
  await page.evaluate(() => {
    document.getElementById('pillars').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(600);
  const firstCard = page.locator('.aww-tilt-card').first();
  await firstCard.hover();
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT_DIR, '07_core_pillars_dark_glass.png') });

  // Shot 8: Cinematic Theater
  console.log('Capturing 08_theater_cinematic.png...');
  await page.evaluate(() => {
    document.getElementById('theater').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '08_theater_cinematic.png') });

  // Shot 9: Download Portal
  console.log('Capturing 09_download_community.png...');
  await page.evaluate(() => {
    document.getElementById('download').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '09_download_community.png') });

  // Shot 10: Fullpage Desktop
  console.log('Capturing 10_fullpage_desktop.png...');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.join(OUT_DIR, '10_fullpage_desktop.png'), fullPage: true });

  await desktopContext.close();

  // 2. Mobile Context (iPhone 14 Pro: 393 x 852)
  console.log('Creating mobile context...');
  const mobileContext = await browser.newContext({
    viewport: { width: 393, height: 852 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto('http://localhost:8089/', { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(800);
  await mobilePage.evaluate(() => {
    document.querySelectorAll('.reveal-fade-up').forEach(el => el.classList.add('is-revealed'));
  });

  // Mobile Hero
  console.log('Capturing 11_mobile_hero.png...');
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '11_mobile_hero.png') });

  // Mobile Races
  console.log('Capturing 12_mobile_races.png...');
  await mobilePage.evaluate(() => {
    document.getElementById('races').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await mobilePage.waitForTimeout(600);
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '12_mobile_races.png') });

  await mobileContext.close();
  await browser.close();

  console.log('All proofs captured successfully into ' + OUT_DIR);
}

run().catch(err => {
  console.error('Capture failed:', err);
  process.exit(1);
});
