from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import datetime

ckey= '*******************'
csecret= '*******************'
atoken= '*******************'
asecret= '*******************'

timeout420 = 60

class listener(StreamListener):

    def on_data(self, data):
        try:
            fn= 'twitDB-'+datetime.date.today().strftime("%Y-%m-%d")+'.txt'
            saveFile = open(fn, 'a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            return True
        except BaseException:
            #print('Napaka')
            time.sleep(5)
        global timeout420
        timeout420 = 60

    def on_error(self, status):
        print(status)
        if status == 420:
            global timeout420
            time.sleep(timeout420)
            timeout420 = timeout420*2
        else:
            time.sleep(320)


media_list = [] # media twitter ID list

while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(follow=media_list)
    except BaseException as e:
        with open("dnevnikNapak.txt","a") as errFile:
            errFile.write("{}\n{}\n\n".format(time.ctime(), str(e)))
