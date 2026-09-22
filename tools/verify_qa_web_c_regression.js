const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8999;
const WS_PROOF_DIR = path.join(process.env.HERMES_KANBAN_WORKSPACE || '/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_c2d088b5', 'proofs');
const REPO_PROOF_DIR = '/opt/side/bravesoul-game/proofs/qa_web_c_regression';

[WS_PROOF_DIR, REPO_PROOF_DIR].forEach(dir => {
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

async function runRegression() {
    const server = await startServer();
    const browser = await chromium.launch({
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    const report = {
        screenshots: {},
        races_grid: {},
        cta_buttons: {},
        trailers: {},
        legacy_elements_audit: {},
        broken_links_audit: {}
    };

    try {
        // ==========================================
        // 1. Link Check (Audit all hrefs & assets)
        // ==========================================
        console.log('\n--- Checking all links and assets in index.html ---');
        const indexHtml = fs.readFileSync(path.join(WEB_ROOT, 'index.html'), 'utf8');
        
        // Find all href and src
        const linkRegex = /(?:href|src|poster)=["']([^"']+)["']/g;
        let match;
        const localAssets = new Set();
        const localAnchors = new Set();
        const externalLinks = new Set();

        while ((match = linkRegex.exec(indexHtml)) !== null) {
            const url = match[1];
            if (url.startsWith('#')) {
                localAnchors.add(url);
            } else if (url.startsWith('http://') || url.startsWith('https://')) {
                externalLinks.add(url);
            } else if (url.startsWith('data:')) {
                // data url
            } else {
                // relative local path
                const clean = url.split('?')[0].split('#')[0];
                if (clean) localAssets.add(clean);
            }
        }

        console.log(`Found ${localAssets.size} local assets/pages, ${localAnchors.size} local anchors, ${externalLinks.size} external links`);
        
        const brokenAssets = [];
        for (const asset of localAssets) {
            const fullP = path.join(WEB_ROOT, asset);
            if (!fs.existsSync(fullP)) {
                brokenAssets.push(asset);
                console.error(`  [404 NOT FOUND] ${asset}`);
            } else {
                console.log(`  [OK 200] ${asset}`);
            }
        }
        report.broken_links_audit.missing_local_files = brokenAssets;
        report.broken_links_audit.total_checked = localAssets.size;

        // Check local anchors in DOM
        // ==========================================
        // 2. Desktop Screenshot & Checks (1280x900)
        // ==========================================
        console.log('\n--- Capturing Desktop (1280x900) ---');
        const desktopPage = await browser.newPage({
            viewport: { width: 1280, height: 900 }
        });

        const consoleErrorsDesktop = [];
        desktopPage.on('console', msg => {
            if (msg.type() === 'error') consoleErrorsDesktop.push(msg.text());
        });

        await desktopPage.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });

        // Ensure all images are loaded
        await desktopPage.evaluate(async () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            for (const img of imgs) {
                img.loading = 'eager';
                if (!img.complete) {
                    await new Promise(r => {
                        img.onload = r;
                        img.onerror = r;
                        setTimeout(r, 1000);
                    });
                }
            }
            // Pause videos for clean shots
            document.querySelectorAll('video').forEach(v => v.pause());
        });

        await desktopPage.waitForTimeout(500);

        // Verify anchors exist on page
        const anchorCheck = await desktopPage.evaluate((anchors) => {
            const results = {};
            for (const a of anchors) {
                const id = a.substring(1);
                const el = document.getElementById(id);
                results[a] = !!el;
            }
            return results;
        }, Array.from(localAnchors));
        report.broken_links_audit.anchor_targets = anchorCheck;
        console.log('Anchor targets check:', anchorCheck);

        // Full page desktop screenshot
        const desktopShotWs = path.join(WS_PROOF_DIR, 'proof_desktop_fullpage.png');
        const desktopShotRepo = path.join(REPO_PROOF_DIR, 'proof_desktop_fullpage.png');
        await desktopPage.screenshot({ path: desktopShotWs, fullPage: true });
        fs.copyFileSync(desktopShotWs, desktopShotRepo);
        report.screenshots.desktop_fullpage = desktopShotRepo;
        console.log(`Saved desktop fullpage screenshot to ${desktopShotRepo}`);

        // Check Races Grid on Desktop
        const desktopRacesData = await desktopPage.evaluate(() => {
            const grid = document.querySelector('.races-grid');
            const gridRect = grid ? grid.getBoundingClientRect() : null;
            const gridStyle = grid ? window.getComputedStyle(grid) : null;
            const cards = Array.from(document.querySelectorAll('.races-grid .race-card')).map((c, i) => {
                const r = c.getBoundingClientRect();
                const name = c.querySelector('.race-card__name')?.innerText?.trim();
                const badge = c.querySelector('.race-card__badge')?.innerText?.trim();
                const weapon = c.querySelector('.race-card__weapon')?.innerText?.trim();
                const img = c.querySelector('.race-card__media img');
                return {
                    idx: i,
                    name,
                    badge,
                    weapon,
                    rect: { x: r.x, y: r.y, width: r.width, height: r.height },
                    imgComplete: img ? img.complete : false,
                    naturalSize: img ? `${img.naturalWidth}x${img.naturalHeight}` : 'none'
                };
            });
            return {
                gridDisplay: gridStyle ? gridStyle.display : null,
                gridColumns: gridStyle ? gridStyle.gridTemplateColumns : null,
                cardCount: cards.length,
                cards
            };
        });
        report.races_grid.desktop = desktopRacesData;
        console.log(`Desktop Races Grid: ${desktopRacesData.cardCount} cards, columns: ${desktopRacesData.gridColumns}`);

        // Check CTA buttons on Desktop
        const ctaCheckDesktop = await desktopPage.evaluate(() => {
            const btns = [
                { name: '立即啟動 (amber)', selector: '.btn-workshop--amber' },
                { name: '探索世界 (emerald)', selector: '.btn-workshop--emerald' },
                { name: '養成細節', selector: '.workshop-features-links a[href*="systems"]' },
                { name: '新手指南', selector: '.workshop-features-links a[href*="guide"]' },
                { name: '下載 PC 測試包 (hero)', selector: '.workshop-features-links a[href*="download"]' },
                { name: '下載測試包 (finale)', selector: '.cta-finale a[href*="download"]' },
                { name: '官方粉專 (finale)', selector: '#cta-finale-facebook' }
            ];

            return btns.map(b => {
                const el = document.querySelector(b.selector);
                if (!el) return { name: b.name, found: false };
                const r = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return {
                    name: b.name,
                    found: true,
                    href: el.getAttribute('href'),
                    visible: r.width > 0 && r.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
                    rect: { width: Math.round(r.width), height: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) },
                    clickable: style.pointerEvents !== 'none'
                };
            });
        });
        report.cta_buttons.desktop = ctaCheckDesktop;
        console.log('Desktop CTA buttons:', ctaCheckDesktop);

        // Check Trailers layout on Desktop
        const trailersDesktop = await desktopPage.evaluate(() => {
            const filmGrid = document.querySelector('.film-grid');
            const landscapeCard = document.querySelector('.film-card--landscape');
            const portraitCard = document.querySelector('.film-card--portrait');
            const phoneMockup = document.querySelector('.film-phone');

            const lRect = landscapeCard ? landscapeCard.getBoundingClientRect() : null;
            const pRect = portraitCard ? portraitCard.getBoundingClientRect() : null;
            const phoneRect = phoneMockup ? phoneMockup.getBoundingClientRect() : null;

            return {
                gridFound: !!filmGrid,
                landscape: {
                    found: !!landscapeCard,
                    rect: lRect ? { width: Math.round(lRect.width), height: Math.round(lRect.height), x: Math.round(lRect.x), y: Math.round(lRect.y) } : null,
                    aspectRatio: lRect ? (lRect.width / lRect.height).toFixed(2) : null
                },
                portrait: {
                    found: !!portraitCard,
                    rect: pRect ? { width: Math.round(pRect.width), height: Math.round(pRect.height), x: Math.round(pRect.x), y: Math.round(pRect.y) } : null,
                    phoneRect: phoneRect ? { width: Math.round(phoneRect.width), height: Math.round(phoneRect.height) } : null
                },
                isSideBySide: lRect && pRect ? Math.abs(lRect.y - pRect.y) < 50 : false
            };
        });
        report.trailers.desktop = trailersDesktop;
        console.log('Desktop Trailers layout:', trailersDesktop);

        // Check for legacy visual elements or world canon violations
        const legacyCheck = await desktopPage.evaluate(() => {
            const textContent = document.body.innerText;
            const htmlContent = document.body.innerHTML;

            const forbiddenPatterns = [
                { pattern: '神殿', reason: '可能殘留舊版神殿文字' },
                { pattern: '希臘', reason: '可能殘留舊版希臘柱/神殿概念' },
                { pattern: 'itch.io', reason: '可能殘留舊版 itch 平台連結' },
                { pattern: 'Steam', reason: '可能殘留舊版 Steam 預約' },
                { pattern: '毛皮', reason: '世界觀禁忌：零毛皮（若是正文宣導零毛皮則正常）' }
            ];

            const matches = [];
            for (const f of forbiddenPatterns) {
                const count = (textContent.match(new RegExp(f.pattern, 'g')) || []).length;
                matches.push({ term: f.pattern, reason: f.reason, count });
            }

            // Check if old hero elements or fx-layer are visible
            const fxLayer = document.querySelector('.fx-layer');
            const fxVisible = fxLayer ? window.getComputedStyle(fxLayer).display !== 'none' : false;

            return {
                matches,
                fxLayerVisible: fxVisible,
                heroWorkshopActive: !!document.querySelector('.hero--workshop')
            };
        });
        report.legacy_elements_audit = legacyCheck;
        console.log('Legacy elements audit:', legacyCheck);

        await desktopPage.close();

        // ==========================================
        // 3. Mobile Screenshot & Checks (390x844)
        // ==========================================
        console.log('\n--- Capturing Mobile (390x844 iPhone 12/13/14 emulation) ---');
        const mobileContext = await browser.newContext({
            viewport: { width: 390, height: 844 },
            userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            isMobile: true,
            hasTouch: true,
            deviceScaleFactor: 1
        });

        const mobilePage = await mobileContext.newPage();
        await mobilePage.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });

        await mobilePage.evaluate(async () => {
            const imgs = Array.from(document.querySelectorAll('img'));
            for (const img of imgs) {
                img.loading = 'eager';
                if (!img.complete) {
                    await new Promise(r => {
                        img.onload = r;
                        img.onerror = r;
                        setTimeout(r, 1000);
                    });
                }
            }
            document.querySelectorAll('video').forEach(v => v.pause());
        });

        await mobilePage.waitForTimeout(500);

        const mobileShotWs = path.join(WS_PROOF_DIR, 'proof_mobile_fullpage.png');
        const mobileShotRepo = path.join(REPO_PROOF_DIR, 'proof_mobile_fullpage.png');
        await mobilePage.screenshot({ path: mobileShotWs, fullPage: true });
        fs.copyFileSync(mobileShotWs, mobileShotRepo);
        report.screenshots.mobile_fullpage = mobileShotRepo;
        console.log(`Saved mobile fullpage screenshot to ${mobileShotRepo}`);

        // Check Races Grid on Mobile
        const mobileRacesData = await mobilePage.evaluate(() => {
            const grid = document.querySelector('.races-grid');
            const gridStyle = grid ? window.getComputedStyle(grid) : null;
            const cards = Array.from(document.querySelectorAll('.races-grid .race-card')).map((c, i) => {
                const r = c.getBoundingClientRect();
                const name = c.querySelector('.race-card__name')?.innerText?.trim();
                const img = c.querySelector('.race-card__media img');
                return {
                    idx: i,
                    name,
                    rect: { x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height) },
                    imgComplete: img ? img.complete : false
                };
            });
            return {
                gridDisplay: gridStyle ? gridStyle.display : null,
                gridColumns: gridStyle ? gridStyle.gridTemplateColumns : null,
                cardCount: cards.length,
                cards
            };
        });
        report.races_grid.mobile = mobileRacesData;
        console.log(`Mobile Races Grid: ${mobileRacesData.cardCount} cards, columns: ${mobileRacesData.gridColumns}`);

        // Check CTA buttons on Mobile
        const ctaCheckMobile = await mobilePage.evaluate(() => {
            const btns = [
                { name: '立即啟動 (amber)', selector: '.btn-workshop--amber' },
                { name: '探索世界 (emerald)', selector: '.btn-workshop--emerald' },
                { name: '養成細節', selector: '.workshop-features-links a[href*="systems"]' },
                { name: '新手指南', selector: '.workshop-features-links a[href*="guide"]' },
                { name: '下載 PC 測試包 (hero)', selector: '.workshop-features-links a[href*="download"]' },
                { name: '下載測試包 (finale)', selector: '.cta-finale a[href*="download"]' },
                { name: '官方粉專 (finale)', selector: '#cta-finale-facebook' }
            ];

            return btns.map(b => {
                const el = document.querySelector(b.selector);
                if (!el) return { name: b.name, found: false };
                const r = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return {
                    name: b.name,
                    found: true,
                    href: el.getAttribute('href'),
                    visible: r.width > 0 && r.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
                    rect: { width: Math.round(r.width), height: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) },
                    clickable: style.pointerEvents !== 'none'
                };
            });
        });
        report.cta_buttons.mobile = ctaCheckMobile;
        console.log('Mobile CTA buttons:', ctaCheckMobile);

        // Check Trailers layout on Mobile
        const trailersMobile = await mobilePage.evaluate(() => {
            const filmGrid = document.querySelector('.film-grid');
            const landscapeCard = document.querySelector('.film-card--landscape');
            const portraitCard = document.querySelector('.film-card--portrait');
            const phoneMockup = document.querySelector('.film-phone');

            const lRect = landscapeCard ? landscapeCard.getBoundingClientRect() : null;
            const pRect = portraitCard ? portraitCard.getBoundingClientRect() : null;
            const phoneRect = phoneMockup ? phoneMockup.getBoundingClientRect() : null;

            return {
                gridFound: !!filmGrid,
                landscape: {
                    found: !!landscapeCard,
                    rect: lRect ? { width: Math.round(lRect.width), height: Math.round(lRect.height), x: Math.round(lRect.x), y: Math.round(lRect.y) } : null
                },
                portrait: {
                    found: !!portraitCard,
                    rect: pRect ? { width: Math.round(pRect.width), height: Math.round(pRect.height), x: Math.round(pRect.x), y: Math.round(pRect.y) } : null,
                    phoneRect: phoneRect ? { width: Math.round(phoneRect.width), height: Math.round(phoneRect.height) } : null
                },
                isStacked: lRect && pRect ? Math.abs(lRect.x - pRect.x) < 20 && pRect.y > lRect.y : false
            };
        });
        report.trailers.mobile = trailersMobile;
        console.log('Mobile Trailers layout:', trailersMobile);

        await mobilePage.close();
        await mobileContext.close();

    } finally {
        await browser.close();
        server.close();
    }

    const reportPathWs = path.join(WS_PROOF_DIR, 'qa_web_regression_report.json');
    const reportPathRepo = path.join(REPO_PROOF_DIR, 'qa_web_regression_report.json');
    fs.writeFileSync(reportPathWs, JSON.stringify(report, null, 2), 'utf8');
    fs.writeFileSync(reportPathRepo, JSON.stringify(report, null, 2), 'utf8');
    console.log(`\n✓ Full QA Regression Report saved to:\n  - ${reportPathWs}\n  - ${reportPathRepo}`);
}

runRegression().catch(err => {
    console.error('Fatal error in regression test:', err);
    process.exit(1);
});
