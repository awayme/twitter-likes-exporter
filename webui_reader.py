import json
import random

from dateutil.parser import parse
from loguru import logger
from pywebio import pin
from pywebio.pin import *
from pywebio.output import *
from pywebio.session import set_env
from pywebio.input import NUMBER
from tinydb import TinyDB, Query

from parse_tweets_json_to_html import ParseTweetsJSONtoHTML

with open("config.json") as json_data_file:
    config_data = json.load(json_data_file)
    db = TinyDB(config_data.get('OUTPUT_JSON_FILE_PATH'))
    db_del = TinyDB(config_data.get('OUTPUT_JSON_DELBAK_FILE_PATH'))
    webui_port = config_data.get('WEBUI_PORT')

def delete_tweet(tweet_id):
    #TODO mark deleted tweet on page
    tweet = Query()
    for t in db.search(tweet.tweet_id==tweet_id):
        db_del.insert(t)
    deled = db.remove(tweet.tweet_id==tweet_id)
    logger.info(f"Del:{tweet_id}, result:{deled}")
    toast(f"Del:{tweet_id}, Done:[{deled}]", duration=10)

def submit(action):
    kw = pin['keyword']
    num = pin['num']
    random_pick = True if pin['random'] else False
    clear = True if pin['clear'] else False

    results = db.all()
    logger.info(f"Loaded Tweets: {len(results)}")
    if kw:
        kw = kw.lower()
        results = list(filter(lambda x: kw in x['tweet_content'].lower(), results))
        logger.info(f"After filtered, Tweets: {len(results)}")

    if random_pick:
        results = random.sample(results, min(num, len(results)))
        results = sorted(results, key=lambda x: parse(x['tweet_created_at']), reverse=True)
    else:
        results = sorted(results, key=lambda x: parse(x['tweet_created_at']), reverse=True)
        results = results[:min(num, len(results))]

    t2h = ParseTweetsJSONtoHTML()
    t2h.download_images = False

    with use_scope('result', clear=clear):
        for result in results:
            tweet_html = t2h.create_tweet_html(result, write=False)
            put_html(tweet_html)
            put_buttons([{"label":"Delete", "value":f"{result['tweet_id']}"}], small=True, onclick=delete_tweet)
            put_markdown('---')

def main():
    set_env(title='Tweets liked')

    put_markdown('# Random Tweets liked')

    put_row([
        put_input(label='Keyword', name='keyword'),
        put_input(label='Number', name='num', type=NUMBER, value=5),
    ])
    put_row([
        put_checkbox(name='random', options=[{'label':'random', "value":True, "checked":True}]),
        put_checkbox(name='clear', options=[{'label':'clear', "value":True, "checked":False}])
    ])
    put_buttons([{"label":"Submit", "value":"submit"}], onclick=submit)
    put_markdown('---')
    put_scope('result', content=[])

if __name__ == "__main__":
    from pywebio import start_server

    # start_server(main, port=webui_port, debug=True, cdn=False)
    start_server(main, port=webui_port)