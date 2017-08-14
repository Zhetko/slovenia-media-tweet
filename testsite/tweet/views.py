from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from tweet.models import Tweet
from datetime import datetime, timedelta
import datetime as dt
import re
from collections import Counter, defaultdict
import lemmagen.lemmatizer
from lemmagen.lemmatizer import Lemmatizer
import operator
import functools
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.cache import cache_page

def index(request):

    try:
        tweet_count = 0
        words = ''
        users = []
        top5 = []
        top = {}
        dates = []
        datesXusers = defaultdict(list)
        enddate = dt.date.today() - timedelta(days = 1)
        startdate = enddate - timedelta(days = 6)

        for tweet in Tweet.objects.filter(tweet_date__range=[startdate, enddate]):
            # število vseh tvitov
            tweet_count += 1
            # top users
            users.append(tweet.tweet_user)
            # timeseries
            dates.append(str(tweet.tweet_date))
            if tweet.tweet_user not in datesXusers[str(tweet.tweet_date)]:
                datesXusers[str(tweet.tweet_date)].append(tweet.tweet_user)
            # wordcloud
            words += ' '
            words += str(tweet.tweet_text_stop)

        # top users
        top_users = Counter(users)
        for key in (top_users):
            top[top_users[key]] = key
        user1 = sorted(top, reverse=True)[:1]
        for key in (sorted(top, reverse=True)[:5]):
            i = []
            i.append(top[key])
            i.append(key)
            i.append(100*int(key)//int(sorted(top, reverse=True)[0]))
            top5.append(i)

        # timeseries
        dates_counted = Counter(dates)
        x = []
        trace1 = []
        trace2 = []
        for key in sorted(dates_counted):
            x.append(key)
            trace1.append(dates_counted[key])
        for key in sorted(datesXusers):
            trace2.append(len(datesXusers[key]))

        # wordcloud
        tweet_text_words = re.findall(r'\w+', words)

        lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
        lem_words = []
        lem_words_count = defaultdict(list)
        for word in tweet_text_words:
            lem_words.append(lemmatizer.lemmatize(word))
            lem_words_count[lemmatizer.lemmatize(word)].append(word)

        word_count = Counter(lem_words).most_common(30)
        word_count_sum = 0
        for word in word_count:
            word_count_sum += word[1]

        tweet_text_list = []
        for word in word_count:
            word_dict = {}
            word_dict['size'] = word[1]*2000//word_count_sum
            word_dict['text'] = Counter(lem_words_count[word[0]]).most_common(1)[0][0]
            tweet_text_list.append(word_dict)

        context = {'tweet_count': tweet_count, 'top5': top5, 'x': x, 'trace1': trace1, 'trace2': trace2, 'top5': top5, 'tweet_text_list': tweet_text_list, 'word_count': word_count}

        return render_to_response('index.html', context)

    except Exception:
        return render_to_response('db-update.html')


def results(request):

    try:
        tweet_count = 0
        words = ''
        users = []
        top5 = []
        top = {}
        dates = []
        datesXusers = defaultdict(list)

        query = request.GET.get('query')
        query_words = re.findall(r'\w+', query)
        query_lem = []
        lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
        for word in query_words:
            query_lem.append(lemmatizer.lemmatize(word).lower())

        for tweet in Tweet.objects.filter(functools.reduce(operator.and_, (Q(tweet_text_lem__icontains=x) for x in query_lem))):
            # število vseh tvitov
            tweet_count += 1
            # top users
            users.append(tweet.tweet_user)
            # timeseries
            dates.append(str(tweet.tweet_date))
            if tweet.tweet_user not in datesXusers[str(tweet.tweet_date)]:
                datesXusers[str(tweet.tweet_date)].append(tweet.tweet_user)
            # wordcloud
            words += ' '
            words += str(tweet.tweet_text_stop)

        # top users
        top_users = Counter(users)
        for key in (top_users):
            top[top_users[key]] = key
        user1 = sorted(top, reverse=True)[:1]
        for key in (sorted(top, reverse=True)[:5]):
            i = []
            i.append(top[key])
            i.append(key)
            i.append(100*int(key)//int(sorted(top, reverse=True)[0]))
            top5.append(i)

        # timeseries
        dates_counted = Counter(dates)
        x = []
        trace1 = []
        trace2 = []
        for key in sorted(dates_counted):
            x.append(key)
            trace1.append(dates_counted[key])
        for key in sorted(datesXusers):
            trace2.append(len(datesXusers[key]))

        # wordcloud
        tweet_text_words = re.findall(r'\w+', words)

        lemmatizer = Lemmatizer(dictionary=lemmagen.DICTIONARY_SLOVENE)
        lem_words = []
        lem_words_count = defaultdict(list)
        for word in tweet_text_words:
            lem_words.append(lemmatizer.lemmatize(word))
            lem_words_count[lemmatizer.lemmatize(word)].append(word)

        word_count = Counter(lem_words).most_common(30)
        word_count_sum = 0
        for word in word_count:
            word_count_sum += word[1]

        tweet_text_list = []
        for word in word_count:
            word_dict = {}
            word_dict['size'] = word[1]*2000//word_count_sum

            word_dict['text'] = Counter(lem_words_count[word[0]]).most_common(1)[0][0]
            tweet_text_list.append(word_dict)

        context = {'tweet_count': tweet_count, 'top5': top5, 'x': x, 'trace1': trace1, 'trace2': trace2, 'top5': top5, 'tweet_text_list': tweet_text_list, 'word_count': word_count, 'query': query}

        return render_to_response('results.html', context)

    except Exception:
        return render_to_response('results-neg.html')

def cookies(request):
    return render_to_response('cookies.html')
