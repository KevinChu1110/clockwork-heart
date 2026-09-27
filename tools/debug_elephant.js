const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('/usr/local/lib/hermes-agent/node_modules/playwright');

const WEB_ROOT = '/opt/side/bravesoul-game/web';
const PORT = 8997;

function getMime(file) {
    const ext = path.extname(file).toLowerCase();
    const map = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.png': 'image/png'
    };
    return map[ext] || 'application/octet-stream';
}

const server = http.createServer((req, res) => {
    let reqPath = decodeURI(req.url.split('?')[0]);
    if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
    const filePath = path.join(WEB_ROOT, reqPath);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        console.log("Serving:", reqPath, fs.statSync(filePath).size);
        res.writeHead(200, { 'Content-Type': getMime(filePath) });
        fs.createReadStream(filePath).pipe(res);
    } else {
        console.log("NOT FOUND:", reqPath);
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(PORT, '127.0.0.1', async () => {
    const browser = await chromium.launch({
        headless: true,
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox', '--disable-gpu']
    });
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    page.on('pageerror', err => console.log('PAGE ERROR:', err));
    page.on('requestfailed', req => console.log('REQUEST FAILED:', req.url(), req.failure().errorText));

    await page.goto(`http://127.0.0.1:${PORT}/index.html`);
    await page.waitForTimeout(1000);

    const elephantImg = await page.$('.race-card img[src*="elephant"]');
    const info = await page.evaluate(el => {
        return {
            src: el.src,
            complete: el.complete,
            naturalWidth: el.naturalWidth,
            naturalHeight: el.naturalHeight,
            currentSrc: el.currentSrc
        };
    }, elephantImg);
    console.log("Elephant img info:", info);

    await browser.close();
    server.close();
});
