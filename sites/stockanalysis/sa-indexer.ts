#!/usr/bin/env bun
/*
 * build the index for company logos from stockanalysis.com
 */
import path from "node:path";
import * as fsPromises from "node:fs/promises";

const SITEMAP_URL =
	"https://sitemap-viewer.fileformat.info/api/sitemap.json?url=https://stockanalysis.com/sitemap.xml";
const USER_AGENT = "LogoSearchBot webmaster@logosear.ch";

type SITEMAP_ENTRY = {
	url: string;
	directory: string[];
	filename: string;
	name: string;
};

type SITEMAP_DATA = {
	status: boolean;
	messages: string[];
	sitemaps: string[];
	entries: SITEMAP_ENTRY[];
};

type INDEX_ENTRY = {
	css?: string;
	name: string;
	img: string;
	src: string;
};

type INDEX_DATA = {
	css?: string;
	handle: string;
	images: INDEX_ENTRY[];
	lastmodified: string;
	name: string;
	provider: string;
	provider_icon: string;
	url: string;
	website?: string;
	logo?: string;
};

async function main() {
	console.log(
		`INFO: ${import.meta.file} starting at ${new Date().toISOString()}`
	);

	const script_dir = import.meta.dir;
	const repo_dir = path.join(script_dir, "..", "..");
	const tmp_dir = path.join(repo_dir, "tmp");

	const stock_data_file = path.join(tmp_dir, "company_tickers.json");
	try {
		await Bun.file(stock_data_file).stat();
		console.log(`INFO: using existing stock data file ${stock_data_file}`);
	} catch (err) {
		if (err.code === "ENOENT") {
			console.log(
				`INFO: downloading stock data file to ${stock_data_file}`
			);
			const response = await fetch(
				"https://www.sec.gov/files/company_tickers.json",
				{
					headers: {
						"User-Agent": USER_AGENT,
					},
				}
			);
			if (!response.ok) {
				throw new Error(
					`Failed to download stock data file: ${response.statusText}`
				);
			}
			const data = await response.arrayBuffer();
			await Bun.write(stock_data_file, data);
		} else {
			throw err;
		}
	}
	const stockData = JSON.parse(await Bun.file(stock_data_file).text());

	const tickerMap = new Map<string, string>();
	for (const index of Object.keys(stockData)) {
		const company = stockData[index];
		if (!company.ticker) {
			continue;
		}
		tickerMap.set(company.ticker, company.title);
	}

	const sitemap_file = path.join(tmp_dir, "sitemap.json");
	try {
		await Bun.file(sitemap_file).stat();
		console.log(`INFO: using existing stock data file ${sitemap_file}`);
	} catch (err) {
		if (err.code === "ENOENT") {
			console.log(`INFO: downloading stock data file to ${sitemap_file}`);
			const response = await fetch(SITEMAP_URL, {
				headers: {
					"User-Agent": USER_AGENT,
				},
			});
			if (!response.ok) {
				throw new Error(
					`Failed to download sitemap: ${response.statusText}`
				);
			}
			const data = await response.arrayBuffer();
			await Bun.write(sitemap_file, data);
		} else {
			throw err;
		}
	}
	const sitemap_data = JSON.parse(
		await Bun.file(sitemap_file).text()
	) as SITEMAP_DATA;

	const tickers = sitemap_data.entries
		.filter((e) => e.directory.length == 1 && e.directory[0] == "stocks")
		.map((e) => e.filename);
	console.log(`INFO: found ${tickers.length.toLocaleString()} stock tickers`);

	const images: INDEX_ENTRY[] = [];

	let missingCount = 0;
	for (const ticker of tickers) {
		const logoUrl = `https://logos.stockanalysis.com/${ticker}.svg`;
		try {
			const response = await fetch(logoUrl, {
				method: "HEAD",
				headers: {
					"User-Agent": USER_AGENT,
				},
			});
			if (response.ok) {
				//console.log(`DEBUG: Logo exists for ticker ${ticker}`);
				images.push({
					img: logoUrl,
					src: `https://stockanalysis.com/stocks/${ticker}/company/`,
					name: ticker.toUpperCase(),
				});
			} else {
				console.log(
					`WARNING: Logo does not exist for ticker ${ticker}`
				);
				missingCount++;
			}
		} catch (err) {
			console.log(
				`ERROR: Failed to check logo for ticker ${ticker}: ${err.message}`
			);
			missingCount++;
		}
	}
	console.log(`INFO: tickers without logos: ${missingCount}`);

	let noName = 0;
	for (const image of images) {
		const name = tickerMap.get(image.name);
		if (name) {
			image.name = `${name} (${image.name})`;
		} else {
			console.log(`INFO: no company name for "${image.name}"`);
			noName++;
		}
	}

	console.log(`INFO: tickers without names: ${noName}`);

	const indexData: INDEX_DATA = {
		handle: "stockanalysis",
		images,
		lastmodified: new Date().toISOString(),
		logo: "https://www.vectorlogo.zone/logos/stockanalysis/stockanalysis-icon.svg",
		name: "stockanalysis.com",
		provider: "remote",
		provider_icon: "https://logosear.ch/images/remote.svg",
		url: "https://stockanalysis.com/",
		website: "https://stockanalysis.com/",
	};

	const output_file = path.join(repo_dir, "dist", "stockanalysis.json");
	await fsPromises.mkdir(path.dirname(output_file), { recursive: true });
	await fsPromises.writeFile(output_file, JSON.stringify(indexData, null, 2));
	console.log(`INFO: index data saved to ${output_file}`);

	console.log(
		`INFO: ${import.meta.file} complete at ${new Date().toISOString()}`
	);
}

if (require.main === module) {
	main()
		.then(() => console.log("INFO: done"))
		.catch((err) => console.error(`ERROR: ${err}`));
}
