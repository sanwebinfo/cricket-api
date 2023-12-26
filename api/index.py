import random
import requests
from bs4 import BeautifulSoup as bs
from markupsafe import escape
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pytz

# Replace the CORS URL with your's
app = Flask(__name__)
app.json.sort_keys = False
cors = CORS(app, resources={
            r"/score/*": {"origins": [r'^https://.+sanweb.info$', r'^https://.+mskian.com$']}})

user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    # 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    # 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
    # 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile DuckDuckGo/5 Safari/537.36',
    # 'Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    # 'Mozilla/5.0 (Android 10; Mobile; rv:102.0) Gecko/102.0 Firefox/102.0'
]
get_random_agent = random.choice(user_agent_list)

headers = {
    'User-Agent': get_random_agent,
    'Cache-Control': 'no-cache'
}


@app.route('/')
def hello():
    return jsonify({'Code': 200, 'message': 'Python - Free Cricket Score API - JSON'})


@app.route('/score', methods=['GET'])
def score():
    get_id = request.args.get('id')
    id = escape(get_id)
    if id:
        session_object = requests.Session()
        r = session_object.get(
            'https://www.cricbuzz.com/live-cricket-scores/' + id, headers=headers)
        soup = bs(r.content, 'lxml')
        try:
            update = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"}) else 'Match Stats will Update Soon'
            process = soup.find_all(
                "div", attrs={"class": "cb-text-inprogress"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inprogress"}) else 'Match Stats will Update Soon'
            noresult = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"}) else 'Match Stats will Update Soon'
            stumps = soup.find_all(
                "div", attrs={"class": "cb-text-stumps"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-stumps"}) else 'Match Stats will Update Soon'
            lunch = soup.find_all(
                "div", attrs={"class": "cb-text-lunch"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-lunch"}) else 'Match Stats will Update Soon'
            inningsbreak = soup.find_all(
                "div", attrs={"class": "cb-text-inningsbreak"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inningsbreak"}) else 'Match Stats will Update Soon'
            tea = soup.find_all("div", attrs={"class": "cb-text-tea"})[0].text.strip() if soup.find(
                "div", attrs={"class": "cb-text-tea"}) else 'Match Stats will Update Soon'
            rain_break = soup.find_all("div", attrs={"class": "cb-text-rain"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-rain"}) else 'Match Stats will Update Soon'
            wet_outfield = soup.find_all("div", attrs={"class": "cb-text-wetoutfield"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-wetoutfield"}) else 'Match Stats will Update Soon'
            match_date_element = soup.find('span', itemprop='startDate')
            if match_date_element:
                match_time = match_date_element.get('content')
                new_dt = match_time.split('+')[0]
                utc_time = datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
                utc_time_utc = utc_time.replace(tzinfo=pytz.UTC)
                target_timezone = pytz.timezone("Asia/Kolkata")
                local_time = utc_time_utc.astimezone(target_timezone)
                formatted_local_time = local_time.strftime(
                    "Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
                match_date = formatted_local_time
            else:
                match_date = 'Match Stats will Update Soon'
            live_score = soup.find(
                "span", attrs={"class": "cb-font-20 text-bold"}).text.strip() if soup.find("span", attrs={"class": "cb-font-20 text-bold"}) else 'Data Not Found'
            title = soup.find(
                "h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}).text.strip().replace(", Commentary", "") if soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}) else 'Data Not Found'
            run_rate = soup.find_all(
                "span", attrs={"class": "cb-font-12 cb-text-gray"})[0].text.strip().replace("CRR:\u00a0", "") if soup.find_all("span", attrs={"class": "cb-font-12 cb-text-gray"}) else 'Data Not Found'
            batter_one = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            batter_two = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            batter_one_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_two_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_one_ball = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_two_ball = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[3].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_one_sr = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 ab text-right"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-14 ab text-right"}) else 'Data Not Found'
            batter_two_sr = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 ab text-right"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-14 ab text-right"}) else 'Data Not Found'
            bowler_one = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[4].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            bowler_two = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            bowler_one_over = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[4].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_two_over = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[6].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_one_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_two_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[7].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_one_eco = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 text-right"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            bowler_two_eco = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 text-right"})[3].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            bowler_one_wicket = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-8 text-right"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-8 text-right"}) else 'Data Not Found'
            bowler_two_wicket = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-8 text-right"})[7].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-8 text-right"}) else 'Data Not Found'
        except IndexError:
            update = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"}) else 'Match Stats will Update Soon'
            process = soup.find_all(
                "div", attrs={"class": "cb-text-inprogress"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inprogress"}) else 'Match Stats will Update Soon'
            noresult = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"}) else 'Match Stats will Update Soon'
            stumps = soup.find_all(
                "div", attrs={"class": "cb-text-stumps"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-stumps"}) else 'Match Stats will Update Soon'
            lunch = soup.find_all(
                "div", attrs={"class": "cb-text-lunch"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-lunch"}) else 'Match Stats will Update Soon'
            inningsbreak = soup.find_all(
                "div", attrs={"class": "cb-text-inningsbreak"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inningsbreak"}) else 'Match Stats will Update Soon'
            tea = soup.find_all("div", attrs={"class": "cb-text-tea"})[0].text.strip() if soup.find(
                "div", attrs={"class": "cb-text-tea"}) else 'Match Stats will Update Soon'
            rain_break = soup.find_all("div", attrs={"class": "cb-text-rain"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-rain"}) else 'Match Stats will Update Soon'
            wet_outfield = soup.find_all("div", attrs={"class": "cb-text-wetoutfield"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-wetoutfield"}) else 'Match Stats will Update Soon'
            match_date_element = soup.find('span', itemprop='startDate')
            if match_date_element:
                match_time = match_date_element.get('content')
                new_dt = match_time.split('+')[0]
                utc_time = datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
                utc_time_utc = utc_time.replace(tzinfo=pytz.UTC)
                target_timezone = pytz.timezone("Asia/Kolkata")
                local_time = utc_time_utc.astimezone(target_timezone)
                formatted_local_time = local_time.strftime(
                    "Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
                match_date = formatted_local_time
            else:
                match_date = 'Match Stats will Update Soon'
            live_score = soup.find(
                "span", attrs={"class": "cb-font-20 text-bold"}).text.strip() if soup.find("span", attrs={"class": "cb-font-20 text-bold"}) else 'Data Not Found'
            title = soup.find(
                "h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}).text.strip().replace(", Commentary", "") if soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}) else 'Data Not Found'
            run_rate = 'Match Stats will Update Soon'
            batter_one = 'Match Stats will Update Soon'
            batter_two = 'Match Stats will Update Soon'
            batter_one_run = 'Match Stats will Update Soon'
            batter_two_run = 'Match Stats will Update Soon'
            batter_one_ball = 'Match Stats will Update Soon'
            batter_two_ball = 'Match Stats will Update Soon'
            batter_one_sr = 'Match Stats will Update Soon'
            batter_two_sr = 'Match Stats will Update Soon'
            bowler_one = 'Match Stats will Update Soon'
            bowler_two = 'Match Stats will Update Soon'
            bowler_one_over = 'Match Stats will Update Soon'
            bowler_two_over = 'Match Stats will Update Soon'
            bowler_one_run = 'Match Stats will Update Soon'
            bowler_two_run = 'Match Stats will Update Soon'
            bowler_one_eco = 'Match Stats will Update Soon'
            bowler_two_eco = 'Match Stats will Update Soon'
            bowler_one_wicket = 'Match Stats will Update Soon'
            bowler_two_wicket = 'Match Stats will Update Soon'
        if (update != 'Match Stats will Update Soon'):
            status = update
        elif (process != 'Match Stats will Update Soon'):
            status = process
        elif (noresult != 'Match Stats will Update Soon'):
            status = noresult
        elif (stumps != 'Match Stats will Update Soon'):
            status = stumps
        elif (lunch != 'Match Stats will Update Soon'):
            status = lunch
        elif (inningsbreak != 'Match Stats will Update Soon'):
            status = inningsbreak
        elif (tea != 'Match Stats will Update Soon'):
            status = tea
        elif (rain_break != 'Match Stats will Update Soon'):
            status = rain_break
        elif (wet_outfield != 'Match Stats will Update Soon'):
            status = wet_outfield
        elif (match_date != 'Match Stats will Update Soon'):
            status = match_date
        else:
            status = 'Match Stats will Update Soon...'
        return jsonify({
            'title': title,
            'update': status,
            'livescore': live_score,
            'runrate': 'CRR: ' + run_rate,
            'batterone': batter_one,
            'batsmanonerun': batter_one_run,
            'batsmanoneball': '(' + batter_one_ball + ')',
            'batsmanonesr': batter_one_sr,
            'battertwo': batter_two,
            'batsmantworun': batter_two_run,
            'batsmantwoball': '(' + batter_two_ball + ')',
            'batsmantwosr': batter_two_sr,
            'bowlerone': bowler_one,
            "bowleroneover": bowler_one_over,
            "bowleronerun": bowler_one_run,
            "bowleronewickers": bowler_one_wicket,
            "bowleroneeconomy": bowler_one_eco,
            'bowlertwo': bowler_two,
            "bowlertwoover": bowler_two_over,
            "bowlertworun": bowler_two_run,
            "bowlertwowickers": bowler_two_wicket,
            "bowlertwoeconomy": bowler_two_eco

        })
    else:
        return jsonify({
            'title': 'Data not Found',
            'update': 'Data not Found',
            'livescore': 'Data not Found',
            'runrate': 'Data not Found',
            'batterone': 'Data not Found',
            'batsmanonerun': 'Data not Found',
            'batsmanoneball': 'Data not Found',
            'batsmanonesr': 'Data not Found',
            'battertwo': 'Data not Found',
            'batsmantworun': 'Data not Found',
            'batsmantwoball': 'Data not Found',
            'batsmantwosr': 'Data not Found',
            'bowlerone': 'Data not Found',
            "bowleroneover": 'Data not Found',
            "bowleronerun": 'Data not Found',
            "bowleronewickers": 'Data not Found',
            "bowleroneeconomy": 'Data not Found',
            'bowlertwo': 'Data not Found',
            "bowlertwoover": 'Data not Found',
            "bowlertworun": 'Data not Found',
            "bowlertwowickers": 'Data not Found',
            "bowlertwoeconomy": 'Data not Found',

        })


@app.route('/score/live', methods=['GET'])
def live():
    get_id = request.args.get('id')
    id = escape(get_id)
    if id:
        session_object = requests.Session()
        r = session_object.get(
            'https://www.cricbuzz.com/live-cricket-scores/' + id, headers=headers)
        soup = bs(r.content, 'lxml')
        try:
            update = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"}) else 'Match Stats will Update Soon'
            process = soup.find_all(
                "div", attrs={"class": "cb-text-inprogress"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inprogress"}) else 'Match Stats will Update Soon'
            noresult = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"}) else 'Match Stats will Update Soon'
            stumps = soup.find_all(
                "div", attrs={"class": "cb-text-stumps"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-stumps"}) else 'Match Stats will Update Soon'
            lunch = soup.find_all(
                "div", attrs={"class": "cb-text-lunch"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-lunch"}) else 'Match Stats will Update Soon'
            inningsbreak = soup.find_all(
                "div", attrs={"class": "cb-text-inningsbreak"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inningsbreak"}) else 'Match Stats will Update Soon'
            tea = soup.find_all("div", attrs={"class": "cb-text-tea"})[0].text.strip() if soup.find(
                "div", attrs={"class": "cb-text-tea"}) else 'Match Stats will Update Soon'
            rain_break = soup.find_all("div", attrs={"class": "cb-text-rain"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-rain"}) else 'Match Stats will Update Soon'
            wet_outfield = soup.find_all("div", attrs={"class": "cb-text-wetoutfield"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-wetoutfield"}) else 'Match Stats will Update Soon'
            match_date_element = soup.find('span', itemprop='startDate')
            if match_date_element:
                match_time = match_date_element.get('content')
                new_dt = match_time.split('+')[0]
                utc_time = datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
                utc_time_utc = utc_time.replace(tzinfo=pytz.UTC)
                target_timezone = pytz.timezone("Asia/Kolkata")
                local_time = utc_time_utc.astimezone(target_timezone)
                formatted_local_time = local_time.strftime(
                    "Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
                match_date = formatted_local_time
            else:
                match_date = 'Match Stats will Update Soon'
            live_score = soup.find(
                "span", attrs={"class": "cb-font-20 text-bold"}).text.strip() if soup.find("span", attrs={"class": "cb-font-20 text-bold"}) else 'Data Not Found'
            title = soup.find(
                "h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}).text.strip().replace(", Commentary", "") if soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}) else 'Data Not Found'
            run_rate = soup.find_all(
                "span", attrs={"class": "cb-font-12 cb-text-gray"})[0].text.strip().replace("CRR:\u00a0", "") if soup.find_all("span", attrs={"class": "cb-font-12 cb-text-gray"}) else 'Data Not Found'
            batter_one = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            batter_two = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            batter_one_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_two_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_one_ball = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_two_ball = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 ab text-right"})[3].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            batter_one_sr = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 ab text-right"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-14 ab text-right"}) else 'Data Not Found'
            batter_two_sr = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 ab text-right"})[1].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-14 ab text-right"}) else 'Data Not Found'
            bowler_one = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[4].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            bowler_two = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-50"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-50"}) else 'Data Not Found'
            bowler_one_over = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[4].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_two_over = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[6].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_one_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_two_run = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-10 text-right"})[7].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 text-right"}) else 'Data Not Found'
            bowler_one_eco = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 text-right"})[2].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            bowler_two_eco = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-14 text-right"})[3].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-10 ab text-right"}) else 'Data Not Found'
            bowler_one_wicket = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-8 text-right"})[5].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-8 text-right"}) else 'Data Not Found'
            bowler_two_wicket = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-8 text-right"})[7].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-8 text-right"}) else 'Data Not Found'
        except IndexError:
            update = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-min-stts cb-text-complete"}) else 'Match Stats will Update Soon'
            process = soup.find_all(
                "div", attrs={"class": "cb-text-inprogress"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inprogress"}) else 'Match Stats will Update Soon'
            noresult = soup.find_all(
                "div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-col cb-col-100 cb-font-18 cb-toss-sts cb-text-abandon"}) else 'Match Stats will Update Soon'
            stumps = soup.find_all(
                "div", attrs={"class": "cb-text-stumps"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-stumps"}) else 'Match Stats will Update Soon'
            lunch = soup.find_all(
                "div", attrs={"class": "cb-text-lunch"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-lunch"}) else 'Match Stats will Update Soon'
            inningsbreak = soup.find_all(
                "div", attrs={"class": "cb-text-inningsbreak"})[0].text.strip() if soup.find_all("div", attrs={"class": "cb-text-inningsbreak"}) else 'Match Stats will Update Soon'
            tea = soup.find_all("div", attrs={"class": "cb-text-tea"})[0].text.strip() if soup.find(
                "div", attrs={"class": "cb-text-tea"}) else 'Match Stats will Update Soon'
            rain_break = soup.find_all("div", attrs={"class": "cb-text-rain"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-rain"}) else 'Match Stats will Update Soon'
            wet_outfield = soup.find_all("div", attrs={"class": "cb-text-wetoutfield"})[0].text.strip(
            ) if soup.find("div", attrs={"class": "cb-text-wetoutfield"}) else 'Match Stats will Update Soon'
            match_date_element = soup.find('span', itemprop='startDate')
            if match_date_element:
                match_time = match_date_element.get('content')
                new_dt = match_time.split('+')[0]
                utc_time = datetime.strptime(new_dt, "%Y-%m-%dT%H:%M:%S")
                utc_time_utc = utc_time.replace(tzinfo=pytz.UTC)
                target_timezone = pytz.timezone("Asia/Kolkata")
                local_time = utc_time_utc.astimezone(target_timezone)
                formatted_local_time = local_time.strftime(
                    "Date: %Y-%m-%d - Time: %I:%M:%S %p (Indian Local Time)")
                match_date = formatted_local_time
            else:
                match_date = 'Match Stats will Update Soon'
            live_score = soup.find(
                "span", attrs={"class": "cb-font-20 text-bold"}).text.strip() if soup.find("span", attrs={"class": "cb-font-20 text-bold"}) else 'Data Not Found'
            title = soup.find(
                "h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}).text.strip().replace(", Commentary", "") if soup.find("h1", attrs={"class": "cb-nav-hdr cb-font-18 line-ht24"}) else 'Data Not Found'
            run_rate = 'Match Stats will Update Soon'
            batter_one = 'Match Stats will Update Soon'
            batter_two = 'Match Stats will Update Soon'
            batter_one_run = 'Match Stats will Update Soon'
            batter_two_run = 'Match Stats will Update Soon'
            batter_one_ball = 'Match Stats will Update Soon'
            batter_two_ball = 'Match Stats will Update Soon'
            batter_one_sr = 'Match Stats will Update Soon'
            batter_two_sr = 'Match Stats will Update Soon'
            bowler_one = 'Match Stats will Update Soon'
            bowler_two = 'Match Stats will Update Soon'
            bowler_one_over = 'Match Stats will Update Soon'
            bowler_two_over = 'Match Stats will Update Soon'
            bowler_one_run = 'Match Stats will Update Soon'
            bowler_two_run = 'Match Stats will Update Soon'
            bowler_one_eco = 'Match Stats will Update Soon'
            bowler_two_eco = 'Match Stats will Update Soon'
            bowler_one_wicket = 'Match Stats will Update Soon'
            bowler_two_wicket = 'Match Stats will Update Soon'
        if (update != 'Match Stats will Update Soon'):
            status = update
        elif (process != 'Match Stats will Update Soon'):
            status = process
        elif (noresult != 'Match Stats will Update Soon'):
            status = noresult
        elif (stumps != 'Match Stats will Update Soon'):
            status = stumps
        elif (lunch != 'Match Stats will Update Soon'):
            status = lunch
        elif (inningsbreak != 'Match Stats will Update Soon'):
            status = inningsbreak
        elif (tea != 'Match Stats will Update Soon'):
            status = tea
        elif (rain_break != 'Match Stats will Update Soon'):
            status = rain_break
        elif (wet_outfield != 'Match Stats will Update Soon'):
            status = wet_outfield
        elif (match_date != 'Match Stats will Update Soon'):
            status = match_date
        else:
            status = 'Match Stats will Update Soon...'
        return jsonify({
            "success": 'true',
            "livescore": {
                'title': title,
                'update': status,
                'current': live_score,
                'runrate': 'CRR: ' + run_rate,
                'batsman': batter_one,
                'batsmanrun': batter_one_run,
                'ballsfaced': '(' + batter_one_ball + ')',
                'sr': batter_one_sr,
                'batsmantwo': batter_two,
                'batsmantworun': batter_two_run,
                'batsmantwoballfaced':  '(' + batter_two_ball + ')',
                'batsmantwosr': batter_two_sr,
                'bowler': bowler_one,
                "bowlerover": bowler_one_over,
                "bowlerruns": bowler_one_run,
                "bowlerwickets": bowler_one_wicket,
                "bowlereconomy": bowler_one_eco,
                'bowlertwo': bowler_two,
                "bowlertwoover": bowler_two_over,
                "bowlertworuns": bowler_two_run,
                "bowlertwowickets": bowler_two_wicket,
                "bowlertwoeconomy": bowler_two_eco
            }

        })
    else:
        return jsonify({
            "success": 'true',
            "livescore": {
                'title': 'Data not Found',
                'update': 'Data not Found',
                'current': 'Data not Found',
                'runrate': 'Data not Found',
                'batsman': 'Data not Found',
                'batsmanrun': 'Data not Found',
                'ballsfaced': 'Data not Found',
                'sr': 'Data not Found',
                'batsmantwo': 'Data not Found',
                'batsmantworun': 'Data not Found',
                'batsmantwoballfaced': 'Data not Found',
                'batsmantwosr': 'Data not Found',
                'bowler': 'Data not Found',
                "bowlerover": 'Data not Found',
                "bowlerruns": 'Data not Found',
                "bowlerwickets": 'Data not Found',
                "bowlereconomy": 'Data not Found',
                'bowlertwo': 'Data not Found',
                "bowlertwoover": 'Data not Found',
                "bowlertworuns": 'Data not Found',
                "bowlertwowickets": 'Data not Found',
                "bowlertwoeconomy": 'Data not Found'
            }

        })


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({
        'title': 'Data not Found',
        'update': 'Data not Found',
        'livescore': 'Data not Found',
        'runrate': 'Data not Found',
        'batterone': 'Data not Found',
        'batsmanonerun': 'Data not Found',
        'batsmanoneball': 'Data not Found',
        'batsmanonesr': 'Data not Found',
        'battertwo': 'Data not Found',
        'batsmantworun': 'Data not Found',
        'batsmantwoball': 'Data not Found',
        'batsmantwosr': 'Data not Found',
        'bowlerone': 'Data not Found',
        "bowleroneover": 'Data not Found',
        "bowleronerun": 'Data not Found',
        "bowleronewickers": 'Data not Found',
        "bowleroneeconomy": 'Data not Found',
        'bowlertwo': 'Data not Found',
        "bowlertwoover": 'Data not Found',
        "bowlertworun": 'Data not Found',
        "bowlertwowickers": 'Data not Found',
        "bowlertwoeconomy": 'Data not Found',

    })


@app.errorhandler(500)
def invalid_route(e):
    return jsonify({
        'title': 'Data not Found',
        'update': 'Data not Found',
        'livescore': 'Data not Found',
        'runrate': 'Data not Found',
        'batterone': 'Data not Found',
        'batsmanonerun': 'Data not Found',
        'batsmanoneball': 'Data not Found',
        'batsmanonesr': 'Data not Found',
        'battertwo': 'Data not Found',
        'batsmantworun': 'Data not Found',
        'batsmantwoball': 'Data not Found',
        'batsmantwosr': 'Data not Found',
        'bowlerone': 'Data not Found',
        "bowleroneover": 'Data not Found',
        "bowleronerun": 'Data not Found',
        "bowleronewickers": 'Data not Found',
        "bowleroneeconomy": 'Data not Found',
        'bowlertwo': 'Data not Found',
        "bowlertwoover": 'Data not Found',
        "bowlertworun": 'Data not Found',
        "bowlertwowickers": 'Data not Found',
        "bowlertwoeconomy": 'Data not Found',

    })


if __name__ == '__main__':
    app.run()
    # app.run(
    #    host="0.0.0.0",
    #    port=int("5000")
    # )
