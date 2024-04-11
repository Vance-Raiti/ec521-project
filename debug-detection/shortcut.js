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
	await page.goto(url);
	
	const listeners = await client.send(
		'Runtime.evaluate',
		{
			expression: "getEventListeners(document)",
		}
	)
	console.log(listeners)		

	await browser.close();
})();
