const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8999;
const OUT_DIR = '/opt/side/bravesoul-game/proofs/web_tortoise';
const WS_DIR = '/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_12a6be48/proofs/web_tortoise';

[OUT_DIR, WS_DIR].forEach(dir => {
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
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    try {
        const context = await browser.newContext({
            viewport: { width: 1280, height: 900 },
            isMobile: false,
            deviceScaleFactor: 1
        });
        const page = await context.newPage();

        await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });

        // Ensure all images are eager and decoded
        await page.evaluate(async () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            for (const img of imgs) {
                img.loading = 'eager';
            }
            await Promise.all(imgs.map(async img => {
                if (img.decode) {
                    try { await img.decode(); } catch (e) {}
                }
            }));
            const step = 400;
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 20));
            }
            window.scrollTo(0, 0);
            document.querySelectorAll('video').forEach(v => v.pause());
        });

        await page.waitForTimeout(500);

        // 1. Screenshot of the entire #cast section
        const castEl = await page.$('#cast');
        if (castEl) {
            const castPath = path.join(OUT_DIR, 'proof_01_web_cast_all.png');
            await castEl.screenshot({ path: castPath });
            fs.copyFileSync(castPath, path.join(WS_DIR, 'proof_01_web_cast_all.png'));
            console.log('Saved proof_01_web_cast_all.png');
        }

        // 2. Screenshot of .races-showcase (all 10 races)
        const showcaseEl = await page.$('.races-showcase');
        if (showcaseEl) {
            const scPath = path.join(OUT_DIR, 'proof_02_web_races_showcase_ten.png');
            await showcaseEl.screenshot({ path: scPath });
            fs.copyFileSync(scPath, path.join(WS_DIR, 'proof_02_web_races_showcase_ten.png'));
            console.log('Saved proof_02_web_races_showcase_ten.png');
        }

        // 3. Screenshot of the last 4 cards (Crane, Bear, Penguin, Tortoise)
        // Let's scroll to the tortoise card and screenshot it specifically
        const cards = await page.$$('.race-card');
        console.log(`Found ${cards.length} race cards.`);
        if (cards.length >= 10) {
            const tortoiseCard = cards[9];
            await tortoiseCard.scrollIntoViewIfNeeded();
            const tortoisePath = path.join(OUT_DIR, 'proof_03_web_tortoise_card.png');
            await tortoiseCard.screenshot({ path: tortoisePath });
            fs.copyFileSync(tortoisePath, path.join(WS_DIR, 'proof_03_web_tortoise_card.png'));
            console.log('Saved proof_03_web_tortoise_card.png');
        }

        // 4. Also capture mobile (390px)
        const mobContext = await browser.newContext({
            viewport: { width: 390, height: 844 },
            isMobile: true,
            hasTouch: true,
            deviceScaleFactor: 1
        });
        const mobPage = await mobContext.newPage();
        await mobPage.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });
        await mobPage.evaluate(async () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            for (const img of imgs) {
                img.loading = 'eager';
            }
            await Promise.all(imgs.map(async img => {
                if (img.decode) {
                    try { await img.decode(); } catch (e) {}
                }
            }));
            const step = 400;
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                window.scrollTo(0, y);
                await new Promise(r => setTimeout(r, 20));
            }
            window.scrollTo(0, 0);
        });
        await mobPage.waitForTimeout(500);

        const mobCards = await mobPage.$$('.race-card');
        if (mobCards.length >= 10) {
            const mobTortoise = mobCards[9];
            await mobTortoise.scrollIntoViewIfNeeded();
            const mobPath = path.join(OUT_DIR, 'proof_04_mobile_tortoise_card.png');
            await mobTortoise.screenshot({ path: mobPath });
            fs.copyFileSync(mobPath, path.join(WS_DIR, 'proof_04_mobile_tortoise_card.png'));
            console.log('Saved proof_04_mobile_tortoise_card.png');
        }

        console.log('All screenshots captured successfully!');
    } finally {
        await browser.close();
        server.close();
    }
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
