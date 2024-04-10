import puppeteer from 'puppeteer';

(async () => {
	const browser = await puppeteer.launch();
	const page = await browser.newPage();
	await page.goto('https://www.google.com);
	const element = await page.waitFor('div > .class-name');
	await element.click();
	await element.dispose();
	await browser.close();
})()
