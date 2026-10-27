const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const dir = process.argv[2];
  for (const [mode, w, h] of [['icon', 1024, 1024], ['full', 1024, 1024], ['og', 1200, 630]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto(`file://${dir}/art.html#${mode}`); await p.waitForFunction(() => document.title === 'ready'); await p.waitForTimeout(300);
    await p.screenshot({ path: `${dir}/${mode}.png`, omitBackground: mode === 'icon', clip: { x: 0, y: 0, width: w, height: h } });
  }
  await b.close();
})();
