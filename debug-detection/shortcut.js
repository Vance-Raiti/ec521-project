const puppeteer = require("puppeteer");


const url = process.argv[2];



(async() => {
	const browser = await puppeteer.launch({
		headless: true,
	});
	const page = await browser.newPage();
	const client = await page.createCDPSession();	
	await page.goto(url);
	const {result: {objectId: docId}} = await client.send(
		'Runtime.evaluate',
		{
			expression: 'document'
		}
	)
	const listeners = await client.send(
		'DOMDebugger.getEventListeners',
		{
			objectId: docId,
			depth: -1,
		}
	)
	console.log(listeners)		

	await browser.close();
})();
