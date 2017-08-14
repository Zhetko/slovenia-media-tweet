from django.core.management.base import BaseCommand
from tweet.models import Tweet
import datetime as dt
from datetime import datetime, timedelta
import re
import lemmagen.lemmatizer
from lemmagen.lemmatizer import Lemmatizer
import time
import schedule
import json
import os
from urllib.request import urlopen
from pytz import timezone

class Command(BaseCommand):
    args = '<foo bar>'
    help = 'help string'

    def _create_tweets(self):

        baseurl = '*********' #tweet streaming server
        yesterday = str(dt.date.today() - timedelta(days=1))
        fn= 'twitDB-'+yesterday+'.txt'
        url = baseurl+fn

        filename = urlopen(url)

        for line in filename:
            line = line.decode('ISO-8859-1')
            line = line.strip()
            if line:
                try:

                    json_load = json.loads(line)

                    # parsamo tekst tvita
                    if 'text' in json_load:
                        t_text = json_load[u'text']
                        text_list = []
                        text_list.append(t_text)
                        if any('\n' in s for s in text_list):
                            text_list = [w.replace('\n', ' ') for w in text_list]
                        tweet_text = str(text_list)
                        if 'https:\/\/' in tweet_text:
                            tweet_text = tweet_text.split('https:\/\/')[0]
                        elif 't.co' in tweet_text:
                            tweet_text = tweet_text.split('https://t.co')[0]
                        tweet_text_orig = tweet_text.lower()[2:-2]
                        tweet_text_re = re.findall(r'\w+', tweet_text)

                        lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
                        tweet_text_lem = ''

                        for word in tweet_text_re:
                            tweet_text_lem += ' '
                            tweet_text_lem += lemmatizer.lemmatize(word).lower()


                        stopwords = ['a', 'ali', 'b', 'bi', 'bil', 'bila', 'bile', 'bili', 'bilo', 'biti', 'bo', 'bodo',
                                     'bojo', 'bolj', 'bom', 'bomo', 'boste', 'bova', 'boš', 'c', 'ce', 'cel', 'cela',
                                     'celi', 'celo', 'd', 'da', 'do', 'dokler', 'dol', 'dolg', 'dolga', 'dolgi', 'dovolj',
                                     'e', 'etc', 'f', 'g', 'g', 'ga', 'ga', 'gor', 'h', 'halo', 'i', 'idr', 'ii', 'iii',
                                     'in', 'iv', 'ix', 'iz', 'j', 'jaz', 'je', 'ji', 'jih', 'jim', 'jo', 'k', 'kadarkoli',
                                     'kaj', 'kajti', 'kako', 'kakor', 'kamor', 'kamorkoli', 'kar', 'karkoli', 'katerikoli',
                                     'kdaj', 'kdo', 'kdorkoli', 'ker', 'ki', 'kje', 'kjer', 'kjerkoli', 'ko', 'koder',
                                     'koderkoli', 'koga', 'komu', 'kot', 'l', 'lahka', 'lahke', 'lahki', 'lahko', 'le', 'm',
                                     'malce', 'malo', 'manj', 'me', 'medtem', 'mene', 'mi', 'midva', 'midve', 'mnogo',
                                     'moj', 'moja', 'moje', 'mora', 'morajo', 'moram', 'moramo', 'morate', 'moraš', 'morem',
                                     'mu', 'n', 'na', 'nad', 'naj', 'najina', 'najino', 'najmanj', 'naju', 'nam', 'nas',
                                     'nato', 'ne', 'nek', 'neka', 'nekaj', 'nekatere', 'nekateri', 'nekatero', 'nekdo',
                                     'neke', 'nekega', 'neki', 'nekje', 'neko', 'nekoga', 'nekoč', 'ni', 'nikamor',
                                     'nikdar', 'nikjer', 'nikoli', 'nič', 'nje', 'njega', 'njegov', 'njegova', 'njegovo',
                                     'njej', 'njemu', 'njen', 'njena', 'njeno', 'nji', 'njih', 'njihov', 'njihova',
                                     'njihovo', 'njiju', 'njim', 'njo', 'njun', 'njuna', 'njuno', 'no', 'nocoj', 'npr', 'o',
                                     'ob', 'oba', 'obe', 'oboje', 'od', 'okoli', 'on', 'onadva', 'one', 'oni', 'onidve',
                                     'oz', 'p', 'pa', 'po', 'pod', 'pogosto', 'poleg', 'poln', 'polna', 'polni', 'polno',
                                     'ponavadi', 'ponovno', 'potem', 'povsod', 'pozdravljen', 'pozdravljeni', 'prav',
                                     'prava', 'prave', 'pravi', 'pravo', 'prazen', 'prazna', 'prazno', 'prbl', 'precej',
                                     'pred', 'prej', 'preko', 'pri', 'pribl', 'približno', 'primer', 'pripravljen',
                                     'pripravljena', 'pripravljeni', 'proti', 'prva', 'prvi', 'prvo', 'r', 'ravno', 'redko',
                                     'res', 'reč', 's', 'saj', 'sam', 'sama', 'same', 'sami', 'samo', 'se', 'še', 'sebe',
                                     'sebi', 'sedaj', 'sem', 'seveda', 'si', 'sicer', 'skoraj', 'skozi', 'smo', 'so',
                                     'spet', 'srednja', 'srednji', 'sta', 'ste', 'stran', 'stvar', 'sva', 't', 'ta', 'tak',
                                     'taka', 'take', 'taki', 'tako', 'takoj', 'tam', 'te', 'tebe', 'tebi', 'tega', 'težak',
                                     'težka', 'težki', 'težko', 'ti', 'tista', 'tiste', 'tisti', 'tisto', 'tj', 'tja', 'to',
                                     'toda', 'tu', 'tudi', 'tukaj', 'tvoj', 'tvoja', 'tvoje', 'u', 'v', 'vaju', 'vam',
                                     'vas', 'vaš', 'vaša', 'vaše', 've', 'vedno', 'velik', 'velika', 'veliki', 'veliko',
                                     'vendar', 'ves', 'več', 'vi', 'via', 'vidva', 'vii', 'viii', 'visok', 'visoka',
                                     'visoke', 'visoki', 'vsa', 'vsaj', 'vsak', 'vsaka', 'vsakdo', 'vsake', 'vsaki',
                                     'vsakomur', 'vse', 'vsega', 'vsi', 'vso', 'včasih', 'x', 'z', 'za', 'zadaj', 'zakaj',
                                     'zdaj', 'zelo', 'zunaj', 'č', 'če', 'često', 'čez', 'čigav', 'š', 'ž', 'že', 'co',
                                     'http', 'https', 'rt', 'common', 'replace', 'be', 'part', 'of', 'can', 'whats', 'what']
                        for stopword in stopwords:
                            while stopword in tweet_text_re:
                                tweet_text_re.remove(stopword)

                        tweet_text_stop = ''
                        for word in tweet_text_re:
                            tweet_text_stop += ' '
                            tweet_text_stop += word.lower()

                        # parsamo čas
                        tweet_time = json_load['created_at']
                        tweet_time = time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(tweet_time, '%a %b %d %H:%M:%S +0000 %Y'))
                        tweet_time = datetime.strptime(tweet_time, "%Y-%m-%d %H:%M:%S")
                        # nastavimo lokalni čas
                        slo = timezone('Europe/Ljubljana')
                        utc = timezone('UTC')
                        tweet_time = utc.localize(tweet_time)
                        tweet_time = tweet_time.astimezone(slo)

                        #parsamo uporabnika
                        tweet_user = json_load['user']['screen_name']

                        #shranimo
                        t = Tweet(tweet_user=tweet_user, tweet_date=datetime.date(tweet_time), tweet_text_orig=tweet_text_orig, tweet_text_lem=tweet_text_lem, tweet_text_stop=tweet_text_stop)
                        t.save()

                except Exception as e:
                    print('!error!: ', e)

    def handle(self, *args, **options):
            self._create_tweets()

schedule.every().day.at("00:43").do(Command().handle)

while True:
    schedule.run_pending()
    time.sleep(1)
