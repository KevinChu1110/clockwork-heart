const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8998;
const PROOF_DIR = '/opt/side/bravesoul-game/proofs/web_thirteen_races';

if (!fs.existsSync(PROOF_DIR)) {
    fs.mkdirSync(PROOF_DIR, { recursive: true });
}

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
        '.txt': 'text/plain; charset=utf-8'
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

async function main() {
    const server = await startServer();
    const browser = await chromium.launch({
        headless: true,
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-gpu']
    });

    try {
        console.log('=== [1/2] 桌面寬度 (1280x800) 驗證 ===');
        const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
        const page = await context.newPage();
        await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });
        await page.evaluate(async () => {
            const selectors = Array.from(document.images);
            await Promise.all(selectors.map(img => {
                if (img.complete) {
                    return img.decode ? img.decode().catch(() => {}) : Promise.resolve();
                }
                return new Promise(resolve => {
                    img.onload = () => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()).then(resolve);
                    img.onerror = resolve;
                });
            }));
        });
        await page.waitForTimeout(500);

        const raceCardData = await page.evaluate(() => {
            const cards = Array.from(document.querySelectorAll('.races-grid .race-card'));
            return cards.map((card, idx) => {
                const name = card.querySelector('.race-card__name')?.innerText.trim() || '';
                const badge = card.querySelector('.race-card__badge')?.innerText.trim() || '';
                const weapon = card.querySelector('.race-card__weapon')?.innerText.trim() || '';
                const desc = card.querySelector('.race-card__desc')?.innerText.trim() || '';
                const img = card.querySelector('.race-card__media img');
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
                    img_natural_h: img?.naturalHeight || 0
                };
            });
        });

        console.log(`Found ${raceCardData.length} race cards in .races-grid:`);
        raceCardData.forEach(c => {
            console.log(`  Card ${c.index}: [${c.name}] (${c.badge}) - Weapon: ${c.weapon} | img: ${c.img_natural_w}x${c.img_natural_h}, complete: ${c.img_complete}`);
        });

        const cards = await page.$$('.races-grid .race-card');

        // Screenshot each of the last 4 cards: Tortoise, Elephant, Frog, Panda
        if (cards.length >= 13) {
            // Elephant (11)
            await cards[10].scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            const elephantBuf = await cards[10].screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_card_11_elephant.png'), elephantBuf);

            // Frog (12)
            await cards[11].scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            const frogBuf = await cards[11].screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_card_12_frog.png'), frogBuf);

            // Panda (13)
            await cards[12].scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            const pandaBuf = await cards[12].screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_card_13_panda.png'), pandaBuf);

            // Tortoise (10)
            await cards[9].scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            const tortoiseBuf = await cards[9].screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_card_10_tortoise.png'), tortoiseBuf);
        }

        // Entire races showcase screenshot
        const showcase = await page.$('.races-showcase');
        if (showcase) {
            await showcase.scrollIntoViewIfNeeded();
            await page.waitForTimeout(300);
            const showcaseBuf = await showcase.screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_desktop_races_showcase.png'), showcaseBuf);
            console.log('Saved proof_desktop_races_showcase.png');
        }

        await context.close();

        console.log('=== [2/2] 手機寬度 (390x844) 響應式驗證 ===');
        const mobContext = await browser.newContext({
            viewport: { width: 390, height: 844 },
            isMobile: true,
            hasTouch: true
        });
        const mobPage = await mobContext.newPage();
        await mobPage.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });
        await mobPage.evaluate(async () => {
            const selectors = Array.from(document.images);
            await Promise.all(selectors.map(img => {
                if (img.complete) {
                    return img.decode ? img.decode().catch(() => {}) : Promise.resolve();
                }
                return new Promise(resolve => {
                    img.onload = () => (img.decode ? img.decode().catch(() => {}) : Promise.resolve()).then(resolve);
                    img.onerror = resolve;
                });
            }));
        });
        await mobPage.waitForTimeout(500);

        const mobCards = await mobPage.$$('.races-grid .race-card');
        if (mobCards.length >= 13) {
            await mobCards[12].scrollIntoViewIfNeeded();
            await mobPage.waitForTimeout(300);
            const mobPandaBuf = await mobCards[12].screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_mobile_card_13_panda.png'), mobPandaBuf);
        }

        const mobShowcase = await mobPage.$('.races-showcase');
        if (mobShowcase) {
            await mobShowcase.scrollIntoViewIfNeeded();
            await mobPage.waitForTimeout(300);
            const mobShowcaseBuf = await mobShowcase.screenshot();
            fs.writeFileSync(path.join(PROOF_DIR, 'proof_mobile_races_showcase.png'), mobShowcaseBuf);
            console.log('Saved proof_mobile_races_showcase.png');
        }

        await mobContext.close();
        console.log('=== 驗證與截圖全數完成！ ===');
    } finally {
        await browser.close();
        server.close();
    }
}

main().catch(err => {
    console.error('Error running verification:', err);
    process.exit(1);
});
