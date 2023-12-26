# Free Cricket API 🍔

Cricket API - Live Cricket Score JSON API 🏏  

***PHP, Node.js and deno Cricket API was not working due to the Cricbuzz Mobile site being Fully Redesigned - The full Site Structure was Changed it's a bit complex to get data - Please Consider using this Python Cricket API Version - Breaking Changes: JSON API Structure was changed update your app or website according to the changes in JSON data***  

unofficial API Data Fetched from `Cricbuzz.com`  

This is an unofficial API and not Linked or Partnered with Any Brands/Company.  

> **Recently we shutdown our Free API Server due to bulk API Calls Personally we Suggest you to Self Host this API on your server - instant Deploy on Vercel or create Docker Container - <https://github.com/sanwebinfo/cricket-api?tab=readme-ov-file#free-deploy->**  

## How it Works? 🤔

Scrape the data using `BeautifulSoup` and export a output via JSON using `Flask` micro web framework.

Everything is scraped live and shown to end users in realtime.

Example: **API URL 🌐**

```sh
# Copy the 5 digit code from cricbuzz Current Live Match URL 
http://127.0.0.1:5000/score?id=<Match ID>
```

## Requirements and Features 📑

- Python 3
- install Required Modules via `requirements.txt`
- Virtual Environment for Running Flask server
- CORS Header
- Multiple timezone Support for get the Match Starting time
- Self-hosting support with gunicorn
- Nginx, Apache2 or Lightspeed for support Proxy
- HTTPS (For Secure SSL Connections)  

## Installation 🍯

- Download or Clone Repo to your Server/localhost

```sh
git clone https://github.com/sanwebinfo/cricket-api
cd cricket-api/api

## install python env
sudo apt install python3-venv

## Create Virtual Env
python3 -m venv venv

## Activate Virtual Env
source venv/bin/activate

## install Modules
python3 -m pip install -r requirements.txt

## verify
python3 -m flask --version

## start the dev server 
flask --app index.py --debug run --host=0.0.0.0 --port=5000

## Exit from Virtual Env
deactivate
```

- Test the API

```sh
## API Home page
http://127.0.0.1:5000/

## GET Match data
http://127.0.0.1:5000/score?id=<Match ID>
```

### Example Response 🌐

![Cricket API](https://raw.githubusercontent.com/sanwebinfo/cricket-api/main/images/screenshot.jpg)  

```json
{
    "title": "Australia vs Pakistan, 2nd Test - Live Cricket Score",
    "update": "Day 1: 3rd Session",
    "livescore": "AUS 168/3 (60)",
    "runrate": "CRR: 2.8",
    "batterone": "Travis Head",
    "batsmanonerun": "5",
    "batsmanoneball": "(5)",
    "batsmanonesr": "100",
    "battertwo": "Marnus Labuschagne",
    "batsmantworun": "36",
    "batsmantwoball": "(98)",
    "batsmantwosr": "36.73",
    "bowlerone": "Shaheen Afridi",
    "bowleroneover": "19",
    "bowleronerun": "61",
    "bowleronewickers": "0",
    "bowleroneeconomy": "3.21",
    "bowlertwo": "Aamer Jamal",
    "bowlertwoover": "12",
    "bowlertworun": "37",
    "bowlertwowickers": "1",
    "bowlertwoeconomy": "3.08"
}
```

## Code Examples ☕

- WordPress

```php
function display_api_response() {
  $base_url = 'http://127.0.0.1:5000/score?id=';
  $match_id = '123456';
  $url = $base_url.$match_id;
  $response = wp_remote_get($url);
  global $body;
  $body = json_decode( $response['body'], true );
}
add_action( 'init', 'display_api_response' );
```

Replace `http://127.0.0.1:5000` with your API URL  

- Fetch API (Javascript)

```js
var match_id = '123456';

async function fetchscore() {
    try {
        const response = await fetch('http://127.0.0.1:5000/score?id=' + match_id);
        const data = await response.json();
        console.log(data);
    } catch (exception) {
        console.log('Connection issue');
    }
}
fetchscore();
```

## Free Deploy 😍

- Deploy on Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fsanwebinfo%2Fcricket-api%2Ftree%2Fmain%2Fapi)  

## Development

- Update Submodule

```sh
git submodule update --remote --merge
```

## Contributing 🙌

Your PR's are Welcome

## Disclaimer 🗃

- This is not an Offical API from Cricbuzz - it's an Unofficial API
- This is for Education Purpose only - use at your own risk on Production Site

All Credits Goes to <https://www.cricbuzz.com/>

## LICENSE 📕

MIT
