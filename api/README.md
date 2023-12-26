# Python Cricket API

Free Cricket API - Scrape the data using `BeautifulSoup` and export a output via JSON using Flask micro web framework.  

You can Free Deploy it on `Vercel`

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fsanwebinfo%2Fcricket-api%2Ftree%2Fmain%2Fapi)  

## Requirements and Features 📑

- Python 3
- install Required Modules via `requirements.txt`
- Virtual Environment for Running Flask server
- CORS Header
- Multiple timezone Support for get the Match Starting time
- Self-hosting support with gunicorn
- Nginx, Apache2 or Lightspeed for support Proxy
- HTTPS (For Secure SSL Connections)  

## Setup and Development

```sh
## install python env
sudo apt install python3-venv

## Clone the Repo
git clone https://github.com/sanwebinfo/cricket-api.git
cd cricket-api/api

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
```

## Exit from Virtual Env

```sh
deactivate
```

- Edit and Modification in `index.py`

- `index.py` - for Vercel Hosting

## Usage

- API Home Page

```sh
http://127.0.0.1:5000/
```

- Get Live Cricket Score

```sh
# Copy the 5 digit code from cricbuzz Current Live Match URL 
http://127.0.0.1:5000/score?id=<Match ID>
```

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

## Self-hosting

- Replace `app.run()` with `app.run(host="0.0.0.0")` to run in production server

```py
if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run(
    #    host="0.0.0.0",
    #    port=int("5000")
    # )
```

- Create `wsgi.py` file and add the below code

```py
from index import app

if __name__ == "__main__":
    app.run()
```

- Run the API with gunicorn and systemd service

```sh
pip install gunicorn
 ```

- Use Apache or Nginx for proxy server

## Older version support

- if you are using older version of python3.6.x try this below versions

```txt

## requirements.txt file

beautifulsoup4==4.12.2
cchardet==2.1.7
certifi==2023.11.17
charset-normalizer==2.0.12
click==8.0.4
dataclasses==0.8
Flask==2.0.3
Flask-Cors==4.0.0
gunicorn==21.2.0
idna==3.6
importlib-metadata==4.8.3
itsdangerous==2.0.1
Jinja2==3.0.3
lxml==4.9.4
MarkupSafe==2.0.1
packaging==21.3
pkg-resources==0.0.0
pur==7.3.1
pyparsing==3.1.1
pytz==2023.3.post1
requests==2.27.1
six==1.16.0
soupsieve==2.3.2.post1
typing-extensions==4.1.1
urllib3==1.26.18
Werkzeug==2.0.3
zipp==3.6.0

```

- Replace `app.json.sort_keys = False` to `app.config['JSON_SORT_KEYS'] = False` in `index.py`

## Disclaimer 🗃

- This is not an Offical API from Cricbuzz - it's an Unofficial API
- This is for Education Purpose only - use at your own risk on Production Site

All Credits Goes to <https://www.cricbuzz.com/>

## LICENSE

MIT
