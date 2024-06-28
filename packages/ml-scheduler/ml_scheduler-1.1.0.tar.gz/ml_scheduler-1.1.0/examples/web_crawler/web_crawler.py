import asyncio
import json
import random
import re

import aiohttp
import pandas as pd
from aiolimiter import AsyncLimiter
from fake_useragent import UserAgent

import ml_scheduler

limiter = AsyncLimiter(1, time_period=1)
ins_id_regex = re.compile(r'"instrumentId":"(\d+)"')
data_base_url = "https://api.investing.com/api/financialdata/historical/{ins_id}?start-date=2000-01-01&end-date=2024-06-28&time-frame=Monthly&add-missing-rows=false"
ua = UserAgent()
"""-H 'accept: */*' \
  -H 'accept-language: en,zh;q=0.9,zh-CN;q=0.8' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -H 'dnt: 1' \
  -H 'domain-id: cn' \
  -H 'origin: https://cn.investing.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://cn.investing.com/' \
  -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'"""


@ml_scheduler.exp_func
async def crawl(exp: ml_scheduler.Exp, url, session, ins_id=None):

    headers = {
        "User-Agent": ua.chrome,
        "accept": "*/*",
        "accept-language": "en,zh;q=0.9,zh-CN;q=0.8",
        "cache-control": "no-cache",
        "dnt": "1",
        "domain-id": "cn",
        "origin": "https://cn.investing.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://cn.investing.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
    }

    if ins_id is None:
        async with limiter:
            async with session.get(url, headers=headers) as response:
                if response.status == 429:
                    await asyncio.sleep(random.uniform(0, 1))
                    return
                else:
                    text = await response.text()
        print(text)
        ins_id = ins_id_regex.search(text).group(1)
        await exp.report(ins_id=ins_id)

    data_url = data_base_url.format(ins_id=int(ins_id))
    print(data_url)

    async with limiter:
        async with session.get(data_url, headers=headers) as response:
            if response.status == 429:
                await asyncio.sleep(random.uniform(0, 1))
                return
            else:
                text = await response.text()

    print(text)
    data = json.loads(text)['data']
    df = pd.DataFrame(data)
    await exp.report(raw_data=text)

    # select rowDate LIKE 'Jan%', last_openRaw
    records = df[df['rowDate'].str.contains(r'Jan')].to_dict('records')

    # group by year
    agg_vol = df.groupby(df['rowDate'].str.split('-').str[0])['vol'].sum()

    results = {}
    for record, vol in zip(records, agg_vol.values()):
        year = record['rowDate'].split(' ')[0]
        results[year + ' Open'] = record['last_openRaw']
        results[year + ' Vol'] = vol

    await exp.report(**results)


async def main():

    async with aiohttp.ClientSession() as session:
        await crawl.arun_csv('urls copy.csv', ['2024 Open'],
                             extra_kwargs={'session': session})


asyncio.run(main())
