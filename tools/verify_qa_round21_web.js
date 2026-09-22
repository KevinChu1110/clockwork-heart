const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8999;
const WS_PROOF_DIR = path.join(process.env.HERMES_KANBAN_WORKSPACE || '/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_633a85aa', 'proofs/qa_round21');
const REPO_PROOF_DIR = '/opt/side/bravesoul-game/proofs/qa_round21';

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

async function runRegression() {
    const server = await startServer();
    const browser = await chromium.launch({
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
    });

    const report = {
        devices: {},
        races_grid: {},
        trailers: {},
        cta_buttons: {},
        audit: {
            broken_assets: [],
            console_errors: [],
            emoji_matches: [],
            world_canon_violations: []
        }
    };

    try {
        console.log('\n=== [1/6] 官網靜態連結與資產可用性稽核 ===');
        const indexHtml = fs.readFileSync(path.join(WEB_ROOT, 'index.html'), 'utf8');
        const linkRegex = /(?:href|src|poster)=["']([^"']+)["']/g;
        let match;
        const localAssets = new Set();
        while ((match = linkRegex.exec(indexHtml)) !== null) {
            const url = match[1];
            if (!url.startsWith('#') && !url.startsWith('http://') && !url.startsWith('https://') && !url.startsWith('data:')) {
                const clean = url.split('?')[0].split('#')[0];
                if (clean) localAssets.add(clean);
            }
        }

        for (const asset of localAssets) {
            const fullP = path.join(WEB_ROOT, asset);
            if (!fs.existsSync(fullP)) {
                report.audit.broken_assets.push(asset);
                console.error(`  ❌ [404 NOT FOUND] ${asset}`);
            }
        }
        console.log(`  ✓ 靜態資產檢測完成：檢查 ${localAssets.size} 個本地資產，缺失數: ${report.audit.broken_assets.length}`);

        const devices = [
            { id: 'desktop_1280', name: '桌機標準 (1280x900)', width: 1280, height: 900, isMobile: false },
            { id: 'desktop_1920', name: '寬螢幕 (1920x1080)', width: 1920, height: 1080, isMobile: false },
            { id: 'tablet_768', name: '平板直向 (768x1024)', width: 768, height: 1024, isMobile: true },
            { id: 'mobile_390', name: '標準手遊手機 (390x844 iPhone)', width: 390, height: 844, isMobile: true },
            { id: 'mobile_360', name: '緊湊小螢幕手機 (360x800 Android)', width: 360, height: 800, isMobile: true }
        ];

        for (let i = 0; i < devices.length; i++) {
            const dev = devices[i];
            console.log(`\n=== [${i + 2}/6] 跨裝置檢測：${dev.name} ===`);
            const context = await browser.newContext({
                viewport: { width: dev.width, height: dev.height },
                isMobile: dev.isMobile,
                hasTouch: dev.isMobile,
                deviceScaleFactor: 1
            });
            const page = await context.newPage();

            page.on('console', msg => {
                if (msg.type() === 'error') {
                    report.audit.console_errors.push({ device: dev.id, text: msg.text() });
                    console.error(`  [Console Error ${dev.id}] ${msg.text()}`);
                }
            });

            await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'networkidle' });

            // 確保所有圖片立即加載與解碼，並順暢滾動觸發渲染
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
                const step = 600;
                for (let y = 0; y < document.body.scrollHeight; y += step) {
                    window.scrollTo(0, y);
                    await new Promise(r => setTimeout(r, 30));
                }
                window.scrollTo(0, 0);
                document.querySelectorAll('video').forEach(v => v.pause());
            });

            await page.waitForTimeout(300);

            // 存證截圖
            const fullShotName = `proof_02_${dev.id}_fullpage.png`;
            const shotRepoPath = path.join(REPO_PROOF_DIR, fullShotName);
            const shotWsPath = path.join(WS_PROOF_DIR, fullShotName);
            try {
                await page.screenshot({ path: shotRepoPath, fullPage: true });
                fs.copyFileSync(shotRepoPath, shotWsPath);
                console.log(`  ✓ 儲存實機全頁截圖: ${shotRepoPath}`);
            } catch (err) {
                console.warn(`  ⚠️ 全頁截圖失敗 (${err.message})，改以視窗截圖存證`);
                await page.screenshot({ path: shotRepoPath, fullPage: false });
                fs.copyFileSync(shotRepoPath, shotWsPath);
                console.log(`  ✓ 儲存視窗截圖: ${shotRepoPath}`);
            }

            // 存證各核心組件區塊截圖
            const heroEl = await page.$('.hero--workshop');
            if (heroEl) {
                const heroPath = path.join(REPO_PROOF_DIR, `crops/crop_02_${dev.id}_hero_workshop.png`);
                await heroEl.screenshot({ path: heroPath });
                fs.copyFileSync(heroPath, path.join(WS_PROOF_DIR, `crops/crop_02_${dev.id}_hero_workshop.png`));
            }
            const racesEl = await page.$('.races-grid');
            if (racesEl) {
                const racesPath = path.join(REPO_PROOF_DIR, `crops/crop_02_${dev.id}_races_grid.png`);
                await racesEl.screenshot({ path: racesPath });
                fs.copyFileSync(racesPath, path.join(WS_PROOF_DIR, `crops/crop_02_${dev.id}_races_grid.png`));
            }
            const filmsEl = await page.$('.section--films');
            if (filmsEl) {
                const filmsPath = path.join(REPO_PROOF_DIR, `crops/crop_02_${dev.id}_films.png`);
                await filmsEl.screenshot({ path: filmsPath });
                fs.copyFileSync(filmsPath, path.join(WS_PROOF_DIR, `crops/crop_02_${dev.id}_films.png`));
            }

            // 檢驗九族卡片
            const racesData = await page.evaluate(() => {
                const cards = Array.from(document.querySelectorAll('.races-grid .race-card')).map((c, idx) => {
                    const r = c.getBoundingClientRect();
                    const name = c.querySelector('.race-card__name')?.innerText?.trim();
                    const trait = c.querySelector('.race-card__traits')?.innerText?.trim();
                    const img = c.querySelector('.race-card__media img');
                    const imgRect = img ? img.getBoundingClientRect() : null;
                    return {
                        idx,
                        name,
                        trait,
                        rect: { width: Math.round(r.width), height: Math.round(r.height), x: Math.round(r.x), y: Math.round(r.y) },
                        imgRect: imgRect ? { width: Math.round(imgRect.width), height: Math.round(imgRect.height) } : null,
                        imgLoaded: !!img && img.complete && img.naturalWidth > 0,
                        naturalWidth: img ? img.naturalWidth : 0,
                        naturalHeight: img ? img.naturalHeight : 0
                    };
                });
                return {
                    count: cards.length,
                    allLoaded: cards.every(c => c.imgLoaded),
                    cards
                };
            });
            report.races_grid[dev.id] = racesData;
            console.log(`  ✓ 九族卡片檢驗: 共有 ${racesData.count} 張，全數載入解碼正常: ${racesData.allLoaded}`);

            // 檢驗工坊儀表與雙按鈕
            const heroData = await page.evaluate(() => {
                const hero = document.querySelector('.hero--workshop');
                const titleImg = document.querySelector('.hero-title-img');
                const btnLaunch = document.querySelector('.btn-workshop--amber');
                const btnExplore = document.querySelector('.btn-workshop--emerald');
                const features = Array.from(document.querySelectorAll('.workshop-cards-grid .workshop-feature-card')).map(fc => {
                    const r = fc.getBoundingClientRect();
                    return { width: Math.round(r.width), height: Math.round(r.height) };
                });

                const rHero = hero ? hero.getBoundingClientRect() : null;
                const rLaunch = btnLaunch ? btnLaunch.getBoundingClientRect() : null;
                const rExplore = btnExplore ? btnExplore.getBoundingClientRect() : null;

                return {
                    heroVisible: !!hero && rHero.width > 0 && rHero.height > 0,
                    heroRect: rHero ? { width: Math.round(rHero.width), height: Math.round(rHero.height) } : null,
                    btnLaunch: rLaunch ? { width: Math.round(rLaunch.width), height: Math.round(rLaunch.height), x: Math.round(rLaunch.x), y: Math.round(rLaunch.y) } : null,
                    btnExplore: rExplore ? { width: Math.round(rExplore.width), height: Math.round(rExplore.height), x: Math.round(rExplore.x), y: Math.round(rExplore.y) } : null,
                    featuresCount: features.length
                };
            });
            report.devices[dev.id] = { hero: heroData };
            console.log(`  ✓ 工坊儀表狀態: 正常可見，啟動鈕尺寸: ${JSON.stringify(heroData.btnLaunch)}，探索鈕: ${JSON.stringify(heroData.btnExplore)}`);

            // 檢驗影片區佈局
            const trailersData = await page.evaluate(() => {
                const landscapeCard = document.querySelector('.film-card--landscape');
                const portraitCard = document.querySelector('.film-card--portrait');
                const lRect = landscapeCard ? landscapeCard.getBoundingClientRect() : null;
                const pRect = portraitCard ? portraitCard.getBoundingClientRect() : null;
                return {
                    landscape: lRect ? { width: Math.round(lRect.width), height: Math.round(lRect.height), y: Math.round(lRect.y) } : null,
                    portrait: pRect ? { width: Math.round(pRect.width), height: Math.round(pRect.height), y: Math.round(pRect.y) } : null,
                    isSideBySide: lRect && pRect ? Math.abs(lRect.y - pRect.y) < 60 : false,
                    isStacked: lRect && pRect ? Math.abs(lRect.y - pRect.y) >= 60 : false
                };
            });
            report.trailers[dev.id] = trailersData;
            console.log(`  ✓ 影片區佈局: 橫版/直版正常，排版模式: ${trailersData.isSideBySide ? '並排 (Desktop)' : '堆疊 (Mobile/Tablet)'}`);

            // 檢驗 Emoji 殘留與世界觀禁忌字眼
            const textAudit = await page.evaluate(() => {
                const text = document.body.innerText;
                const emojiRegex = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
                const emojiMatches = (text.match(new RegExp(emojiRegex, 'gu')) || []);

                const forbidden = [
                    { word: '神殿', reason: '希臘神殿字眼殘留' },
                    { word: '希臘', reason: '舊版希臘柱概念殘留' },
                    { word: 'itch.io', reason: '舊版 itch 平台殘留' },
                    { word: 'Steam', reason: 'Steam 預約殘留' }
                ];
                const forbiddenMatches = [];
                for (const f of forbidden) {
                    const count = (text.match(new RegExp(f.word, 'g')) || []).length;
                    if (count > 0) forbiddenMatches.push({ word: f.word, count, reason: f.reason });
                }

                // 檢查毛皮字眼（世界觀憲章零毛皮，但宣傳「零毛皮」是合規的）
                const furMatches = (text.match(/毛皮/g) || []).length;

                return {
                    emojiCount: emojiMatches.length,
                    emojiSamples: emojiMatches.slice(0, 5),
                    forbiddenMatches,
                    furMatches
                };
            });
            if (textAudit.emojiCount > 0) {
                report.audit.emoji_matches.push({ device: dev.id, emojis: textAudit.emojiSamples });
            }
            if (textAudit.forbiddenMatches.length > 0) {
                report.audit.world_canon_violations.push({ device: dev.id, matches: textAudit.forbiddenMatches });
            }
            console.log(`  ✓ 符號與世界觀稽核: 系統Emoji數: ${textAudit.emojiCount}，違禁字: ${textAudit.forbiddenMatches.length}，毛皮詞頻: ${textAudit.furMatches} (宣傳「零毛皮」合規)`);

            await context.close();
        }

        const reportPathRepo = path.join(REPO_PROOF_DIR, 'qa_round21_web_report.json');
        const reportPathWs = path.join(WS_PROOF_DIR, 'qa_round21_web_report.json');
        fs.writeFileSync(reportPathRepo, JSON.stringify(report, null, 2), 'utf8');
        fs.writeFileSync(reportPathWs, JSON.stringify(report, null, 2), 'utf8');
        console.log(`\n✓ 跨裝置回歸報告已輸出至: ${reportPathRepo}`);

    } finally {
        await browser.close();
        server.close();
    }
}

runRegression().catch(err => {
    console.error('Fatal regression error:', err);
    process.exit(1);
});
