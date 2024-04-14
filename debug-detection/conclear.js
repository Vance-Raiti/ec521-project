const puppeteer = require("puppeteer");
const fs = require('node:fs');

const url = process.argv[2];

function delay(time) {
	return new Promise(
	(resolve) => {
		setTimeout(resolve, time);
	});
}



(async() => {	
	const browser = await puppeteer.launch({
		headless: false,
	});
	const page = await browser.newPage();
	const client = await page.createCDPSession();		
	await client.send('Runtime.enable');
	await page.goto(url);
	let numCallsToConsoleClear = 0;
	await client.on(
		'Runtime.consoleAPICalled',
		(a,b,c,d,e,f) => {
			numCallsToConsoleClear += 1;
		}
	)
	await delay(3000);
	console.log(numCallsToConsoleClear);		
	
})();
