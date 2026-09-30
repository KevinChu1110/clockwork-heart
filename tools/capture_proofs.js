const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT_DIR = '/opt/side/bravesoul-game/proofs/t_9db8f3f7';
fs.mkdirSync(OUT_DIR, { recursive: true });

async function run() {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  // Desktop context
  const desktopContext = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1
  });
  const page = await desktopContext.newPage();

  page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER ERROR:', err));

  await page.goto('http://localhost:8089/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // 1. Desktop Hero
  console.log('Capturing 01_hero_desktop.png...');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '01_hero_desktop.png') });

  // 2. Races Showcase (Rabbit)
  console.log('Capturing 02_races_showcase_rabbit.png...');
  await page.evaluate(() => {
    document.getElementById('races').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(OUT_DIR, '02_races_showcase_rabbit.png') });

  // 3. Races Showcase (Lion)
  console.log('Capturing 03_races_showcase_lion.png...');
  await page.locator('.race-nav-btn').nth(1).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '03_races_showcase_lion.png') });

  // 4. Races Showcase (Fox)
  console.log('Capturing 04_races_showcase_fox.png...');
  await page.locator('.race-nav-btn').nth(2).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '04_races_showcase_fox.png') });

  // 5. Races Showcase (Panda)
  console.log('Capturing 05_races_showcase_panda.png...');
  await page.locator('.race-nav-btn').nth(12).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '05_races_showcase_panda.png') });

  // 6. Core Pillars 3D
  console.log('Capturing 06_core_pillars_3d.png...');
  await page.evaluate(() => {
    document.getElementById('pillars').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(600);
  const firstCard = page.locator('.aww-tilt-card').first();
  await firstCard.hover();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '06_core_pillars_3d.png') });

  // 7. Cinematic Theater (Landscape)
  console.log('Capturing 07_theater_landscape.png...');
  await page.evaluate(() => {
    document.getElementById('theater').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(OUT_DIR, '07_theater_landscape.png') });

  // 8. Cinematic Theater (Portrait 9:16)
  console.log('Capturing 08_theater_portrait.png...');
  await page.locator('.theater-tab-btn').nth(1).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT_DIR, '08_theater_portrait.png') });

  // 9. Download & Community
  console.log('Capturing 09_download_community.png...');
  await page.evaluate(() => {
    document.getElementById('download').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(OUT_DIR, '09_download_community.png') });

  // 10. Fullpage Desktop
  console.log('Capturing 11_fullpage_desktop.png...');
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.waitForTimeout(500);
  // Ensure all reveal elements are fully visible for fullpage shot
  await page.evaluate(() => {
    document.querySelectorAll('.reveal-fade-up').forEach(el => el.classList.add('is-revealed'));
  });
  await page.screenshot({ path: path.join(OUT_DIR, '11_fullpage_desktop.png'), fullPage: true });

  await desktopContext.close();

  // Mobile Context (iPhone 14)
  console.log('Capturing mobile screenshots...');
  const mobileContext = await browser.newContext({
    viewport: { width: 390, height: 844 },
    isMobile: true,
    hasTouch: true
  });
  const mobilePage = await mobileContext.newPage();
  await mobilePage.goto('http://localhost:8089/', { waitUntil: 'networkidle' });
  await mobilePage.waitForTimeout(1000);
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '10_mobile_hero.png') });

  await mobilePage.evaluate(() => {
    document.getElementById('races').scrollIntoView({ behavior: 'instant', block: 'start' });
  });
  await mobilePage.waitForTimeout(800);
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '10_mobile_races.png') });

  await mobilePage.evaluate(() => {
    document.querySelectorAll('.reveal-fade-up').forEach(el => el.classList.add('is-revealed'));
  });
  await mobilePage.screenshot({ path: path.join(OUT_DIR, '10_mobile_fullpage.png'), fullPage: true });

  await mobileContext.close();
  await browser.close();
  console.log('All screenshots captured successfully!');
}

run().catch(err => {
  console.error('Test run failed:', err);
  process.exit(1);
});
