const puppeteer = require("puppeteer");

function delay(time) {
	return new Promise(
	(resolve) => {
		setTimeout(resolve, time);
	});
}

const url = process.argv[2];



(async() => {
	const browser = await puppeteer.launch({
		headless: true,
	});
	const page = await browser.newPage();
	const client = await page.createCDPSession();
	
	client.send('Debugger.enable');
	let i = 0;
	client.on(
		'Debugger.paused',
		() => {
			i = i + 1;
			client.send('Debugger.resume');
		}
	)
	
	await page.goto(url);
	await delay(3000);
	console.log(i);
	await browser.close();
})();
