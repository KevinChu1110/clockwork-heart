const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8999;
const WS_PROOF_DIR = path.join(process.env.HERMES_KANBAN_WORKSPACE || '/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_8aec2101', 'proofs/qa_round27_web_tortoise');
const REPO_PROOF_DIR = '/opt/side/bravesoul-game/proofs/qa_round27_web_tortoise';

[WS_PROOF_DIR, REPO_PROOF_DIR, path.join(REPO_PROOF_DIR, 'crops'), path.join(WS_PROOF_DIR, 'crops')].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
});

function getMime(file) {
    const ext = path.extname(file).toLowerCase();
    const map = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.json': 'application/json; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.mp4': 'video/mp4',
        '.txt': 'text/plain; charset=utf-8',
        '.xml': 'application/xml',
        '.woff2': 'font/woff2',
        '.woff': 'font/woff',
        '.ttf': 'font/ttf'
    };
    return map[ext] || 'application/octet-stream';
}

function startServer() {
    const server = http.createServer((req, res) => {
        let reqPath = decodeURI(req.url.split('?')[0]);
        if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
        const filePath = path.join(WEB_ROOT, reqPath);

        if (!filePath.startsWith(WEB_ROOT)) {
            res.writeHead(403);
            res.end('Forbidden');
            return;
        }

        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            res.writeHead(200, { 'Content-Type': getMime(filePath) });
            fs.createReadStream(filePath).pipe(res);
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('404 Not Found: ' + reqPath);
        }
    });

    return new Promise(resolve => {
        server.listen(PORT, '127.0.0.1', () => {
            console.log(`Server listening on http://127.0.0.1:${PORT}`);
            resolve(server);
        });
    });
}

function saveDual(filename, buf) {
    const p1 = path.join(REPO_PROOF_DIR, filename);
    const p2 = path.join(WS_PROOF_DIR, filename);
    fs.writeFileSync(p1, buf);
    fs.writeFileSync(p2, buf);
    console.log(`  ✓ Saved proof: ${filename}`);
}

async function runRegression() {
    const server = await startServer();
    const browser = await chromium.launch({
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
    });

    const report = {
        desktop: {},
        mobile: {},
        gallery: {},
        walkthrough: {},
        races_grid: [],
        audit: {
            broken_assets: [],
            console_errors: []
        }
    };

    try {
        console.log('\n=== [1/4] Desktop 桌面寬度 (1280x900) 驗證 ===');
        {
            const context = await browser.newContext({
                viewport: { width: 1280, height: 900 },
                isMobile: false,
                deviceScaleFactor: 1
            });
            const page = await context.newPage();

            page.on('console', msg => {
                if (msg.type() === 'error') report.audit.console_errors.push(`Console error: ${msg.text()}`);
            });
            page.on('pageerror', err => {
                report.audit.console_errors.push(`Page error: ${err.message}`);
            });

            await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'domcontentloaded' });
            await page.waitForTimeout(500);

            // 1. Cast section
            const castEl = await page.$('#cast');
            if (castEl) {
                const castBuf = await castEl.screenshot();
                saveDual('proof_01_desktop_cast_section.png', castBuf);
            }

            // 2. Races showcase (all 10 races)
            const showcaseEl = await page.$('.races-showcase');
            if (showcaseEl) {
                const scBuf = await showcaseEl.screenshot();
                saveDual('proof_02_desktop_races_showcase_ten.png', scBuf);
            }

            // Check race cards details
            const raceCardData = await page.evaluate(() => {
                const cards = Array.from(document.querySelectorAll('.races-grid .race-card'));
                return cards.map((c, idx) => {
                    const img = c.querySelector('.race-card__media img');
                    const name = c.querySelector('.race-card__name')?.textContent.trim() || '';
                    const badge = c.querySelector('.race-card__badge')?.textContent.trim() || '';
                    const weapon = c.querySelector('.race-card__weapon')?.textContent.trim() || '';
                    const desc = c.querySelector('.race-card__desc')?.textContent.trim() || '';
                    const rect = c.getBoundingClientRect();
                    return {
                        index: idx + 1,
                        name,
                        badge,
                        weapon,
                        desc,
                        img_src: img?.getAttribute('src') || '',
                        img_alt: img?.getAttribute('alt') || '',
                        img_complete: img?.complete || false,
                        img_natural_w: img?.naturalWidth || 0,
                        img_natural_h: img?.naturalHeight || 0,
                        card_w: Math.round(rect.width),
                        card_h: Math.round(rect.height),
                        card_x: Math.round(rect.x),
                        card_y: Math.round(rect.y)
                    };
                });
            });
            report.races_grid = raceCardData;
            console.log(`Found ${raceCardData.length} race cards in .races-grid:`);
            raceCardData.forEach(c => {
                console.log(`  Card ${c.index}: [${c.name}] (${c.badge}) - Weapon: ${c.weapon} | img: ${c.img_natural_w}x${c.img_natural_h}, complete: ${c.img_complete}`);
            });

            // Screenshot of the 10th card specifically: Tortoise
            const cards = await page.$$('.races-grid .race-card');
            if (cards.length >= 10) {
                const tortoiseCard = cards[9];
                await tortoiseCard.scrollIntoViewIfNeeded();
                await page.waitForTimeout(200);
                const tBuf = await tortoiseCard.screenshot();
                saveDual('proof_03_desktop_tortoise_card.png', tBuf);
            }

            // Screenshot of hero rabbit card in workshop
            const rabbitWorkshop = await page.$('#workshop-char-card');
            if (rabbitWorkshop) {
                const rwBuf = await rabbitWorkshop.screenshot();
                saveDual('proof_04_desktop_workshop_rabbit_card.png', rwBuf);
            }

            await context.close();
        }

        console.log('\n=== [2/4] Mobile 手機寬度 (390x844) 響應式驗證 ===');
        {
            const mobContext = await browser.newContext({
                viewport: { width: 390, height: 844 },
                isMobile: true,
                hasTouch: true,
                deviceScaleFactor: 1
            });
            const mobPage = await mobContext.newPage();
            await mobPage.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'domcontentloaded' });
            await mobPage.waitForTimeout(500);

            const mobShowcase = await mobPage.$('.races-showcase');
            if (mobShowcase) {
                await mobShowcase.scrollIntoViewIfNeeded();
                const mobScBuf = await mobShowcase.screenshot();
                saveDual('proof_05_mobile_races_showcase.png', mobScBuf);
            }

            const mobCards = await mobPage.$$('.races-grid .race-card');
            if (mobCards.length >= 10) {
                const mobTortoise = mobCards[9];
                await mobTortoise.scrollIntoViewIfNeeded();
                await mobPage.waitForTimeout(200);
                const mobTBuf = await mobTortoise.screenshot();
                saveDual('proof_06_mobile_tortoise_card.png', mobTBuf);
            }

            // Check horizontal overflow on mobile
            const mobOverflow = await mobPage.evaluate(() => {
                const docW = document.documentElement.scrollWidth;
                const winW = window.innerWidth;
                return {
                    scrollWidth: docW,
                    innerWidth: winW,
                    hasOverflow: docW > winW
                };
            });
            report.mobile.overflow = mobOverflow;
            console.log(`Mobile viewport overflow check: scrollWidth=${mobOverflow.scrollWidth}, innerWidth=${mobOverflow.innerWidth}, hasOverflow=${mobOverflow.hasOverflow}`);

            await mobContext.close();
        }

        console.log('\n=== [3/4] 官網圖鑑 / 畫面頁面 (gallery.html) 驗證 ===');
        {
            const galContext = await browser.newContext({
                viewport: { width: 1280, height: 900 },
                deviceScaleFactor: 1
            });
            const galPage = await galContext.newPage();
            await galPage.goto(`http://127.0.0.1:${PORT}/pages/gallery.html`, { waitUntil: 'domcontentloaded' });
            await galPage.waitForTimeout(500);

            const galPromo = await galPage.$('#promo');
            if (galPromo) {
                const galBuf = await galPromo.screenshot();
                saveDual('proof_07_gallery_key_visual.png', galBuf);
            }

            const galCaptionText = await galPage.evaluate(() => {
                return document.querySelector('#promo span')?.textContent.trim() || '';
            });
            report.gallery.caption = galCaptionText;
            console.log(`Gallery caption: "${galCaptionText}"`);

            await galContext.close();
        }

        console.log('\n=== [4/4] 官網攻略世界觀章節 (walkthrough.html) 驗證 ===');
        {
            const wtContext = await browser.newContext({
                viewport: { width: 1280, height: 900 },
                deviceScaleFactor: 1
            });
            const wtPage = await wtContext.newPage();
            await wtPage.goto(`http://127.0.0.1:${PORT}/pages/walkthrough.html`, { waitUntil: 'domcontentloaded' });
            await wtPage.waitForTimeout(500);

            const wtCh1 = await wtPage.$('#ch1');
            if (wtCh1) {
                const wtBuf = await wtCh1.screenshot();
                saveDual('proof_08_walkthrough_ch1.png', wtBuf);
            }

            const wtLeadText = await wtPage.evaluate(() => {
                return document.querySelector('#ch1 .wt-lead')?.textContent.trim() || '';
            });
            report.walkthrough.lead = wtLeadText;
            console.log(`Walkthrough Ch1 lead: "${wtLeadText}"`);

            await wtContext.close();
        }

        // Save report JSON
        const jsonP1 = path.join(REPO_PROOF_DIR, 'qa_round27_web_report.json');
        const jsonP2 = path.join(WS_PROOF_DIR, 'qa_round27_web_report.json');
        fs.writeFileSync(jsonP1, JSON.stringify(report, null, 2));
        fs.writeFileSync(jsonP2, JSON.stringify(report, null, 2));
        console.log('Saved qa_round27_web_report.json');

        console.log('\n=== 官網回歸驗收自動化執行完成 ===');
    } finally {
        await browser.close();
        server.close();
    }
}

runRegression().catch(err => {
    console.error('Fatal regression error:', err);
    process.exit(1);
});
