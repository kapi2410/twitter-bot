from pprint import pprint as pp
import math
import requests
from requests import Session
import shutil
import tweepy
import pickle
import time
import dotenv as de
import os as _os
import pyrebase
de.load_dotenv()

apikey = _os.environ["apikey"]
imgapi = _os.environ["imgapi"]
tkey = _os.environ["tkey"]
tkey_secret = _os.environ["tkey_secret"]
t_access_token = _os.environ["t_access_token"]
t_access_token_sec = _os.environ["t_access_token_sec"]
diskapi = _os.environ["diskapi"]

config = {
  "apiKey": diskapi,
  "authDomain": "ttbot-43e76.firebaseapp.com",
  "projectId": "ttbot-43e76",
  "storageBucket": "ttbot-43e76.appspot.com",
  "messagingSenderId": "1085822555926",
  "appId": "1:1085822555926:web:3734e4144a6bddd82ee237",
  "measurementId": "G-VFV00NPXB5",
  "databaseURL":"https://ttbot-43e76.firebaseio.com"
}


class cmc:
  def __init__(self,key=apikey):
    self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency'
    self.headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': key}
    self.session = Session()
    self.session.headers.update(self.headers)
  
  def allcoins(self,limit=None):
    """
    returns data about every coin listed on coinmarketcap.com
    optional parameter: limit ie. limit = 5 will only return 5 biggest cryptocurriencies
    """
    if limit is None:
      params = {"sort":"cmc_rank"}
    else:
      params = {"limit":limit,"sort":"cmc_rank"}
    url = self.url + '/map'
    r = self.session.get(url,params=params)
    return r.json()['data']
  
  def getsymbols(self):
    """
    returns list of symbols of all coins
    """
    syms = []
    coins = self.allcoins()
    for i in coins:
      syms.append(i['symbol'])
    return syms

  def coinprice(self,symbol):
    """
    returns list with symbol and other price data:
    [symbol, price, 1h change, 24h change]
    """
    if symbol == symbol.upper():
      url = self.url + '/quotes/latest'
      params = {'symbol':symbol}
      r = self.session.get(url,params=params)
      #fpos = list(r..json().keys()[0])
      result = r.json()['data'][symbol]['quote']['USD']
      return [symbol,result["price"],result["percent_change_1h"],result["percent_change_24h"]]
    else:
      url = self.url + '/quotes/latest'
      params = {'slug': symbol}
      r = self.session.get(url,params = params)
      result = r.json()['data'] 
      name = list(result.keys())[0]
      result2 = result[name]['quote']['USD']
      return [symbol,result2['price'],result2["percent_change_1h"],result2["percent_change_24h"]]
  
  def prices4alert(self,pr):
    """
    pr is a dictionary with price history,
    this function returns dictionary updated with new prices and list of symbols
    """
    syms = self.topx(100)
    slug = ''
    for i in syms:
        slug += i+','
    url = self.url + '/quotes/latest'
    params = {'symbol': slug[:-1]}
    r = self.session.get(url,params = params)
    p = r.json()['data']
    #pr = dict()
    for i in syms:
      if i in pr:
        pr[i] = pr[i] + [p[i]['quote']['USD']['price']]
      else:
        pr[i] = [p[i]['quote']['USD']['price']]
    return pr,syms


  def topx(self,limit):
    """
    returns list of n of the biggest cryptos, where n = limit
    """
    x = self.allcoins(limit)
    results = []
    for i in range(limit):
      results.append(x[i]["symbol"])
    return results
  
  def getstats(self,limit):
    """
    returns data about n biggest cryptos excluding stable coins
    where n = limit
    """
    x = self.topx(limit)
    cnt = 0
    for i in x:
      if "US" in i:
        cnt += 1
    x2 = self.topx(limit + cnt)
    cnt2 = 0
    for i in x2:
      if "US" in i:
        cnt2 +=1 
    x3 = self.topx(limit+cnt2)
    results = []
    for i in range(limit+cnt2):
      a = self.coinprice(x3[i])
      if "US" not in a[0]:
        results.append(a)
      else:
        pass
    return results


def dchart(symbol):
  """
  creates png file with chart with requested cryptocurriency
  """
  url = 'https://api.chart-img.com/v1/tradingview/advanced-chart?interval=15m&width=700&height=450&timezone=Etc/UTC&symbol=BINANCE:'+symbol+'USD&key=' + imgapi
  r = requests.get(url,stream=True)
  if r.status_code == 200:
    with open("chart.png",'wb') as f:
      r.raw.decode_content = True
      shutil.copyfileobj(r.raw,f)
    return True
  else:
    return False

class twitter:
  def __init__(self):
    self.consumer_key = tkey
    self.consumer_key_secret = tkey_secret
    self.access_token = t_access_token
    self.access_token_secret = t_access_token_sec
    self.auth = tweepy.OAuth1UserHandler(
      consumer_key = self.consumer_key,
      consumer_secret=self.consumer_key_secret,
      access_token=self.access_token,
      access_token_secret=self.access_token_secret)
    self.api = tweepy.API(self.auth)
    self.id = self.api.get_user(screen_name = "CryptoBot24").id
    self.name = "CryptoBot24"

  def create_tweet(self,text,img,in_reply_to_status_id=None):
    """
    creates tweet with text,img
    optional parameter: in_reply_to_status_id we use it when 
                        we want our status to be reply to tweet 
                        with given id
    """
    self.api.update_status_with_media(status=text,filename=img,in_reply_to_status_id = in_reply_to_status_id)

  def last_tweet_id(self):
    """
    returns last tweet id (last tweet of this account)
    """
    return self.api.user_timeline(screen_name="CryptoBot24")[0].id

  def replies(self):
    """
    returns data about every reply to the bot's tweets
    """
    replies = []
    x = tweepy.Cursor(self.api.search_tweets,q='to:'+self.name,result_type='recent').items(1000)
    for i in x:
      replies.append([i.id,i.text])
    return replies

  

def make_text(text):
  """
  simple function that transforms text so it looks better on twitter
  """
  new_text="         Crypto price update: \n\nCoin |   price   | 1h change | 24h change \n"
  for i in range(len(text)):
    x = text[i]
    n = len(list(str(rn(x[1]))))
    #sp = " "
    new_text = new_text + "{}  |  ${}".format(x[0],rn(x[1]))+" "*(9-n)+"|  {} %   |  {} % \n".format(round(x[2],1),round(x[3],1))
  new_text = new_text + "\n #btc #crypto #eth"
  return new_text

def rn(num):
  """
  this function rounds floats depending on number of digits
  """
  if num > 10*2:
    return round(num,2)
  else:
    return round(num, 4 - int(math.floor(math.log10(abs(num)))) - 1)

def up():
  """
  this function post tweet with top 4 cryptocurriencies info + chart of BTC
  """
  c = cmc()
  x = c.getstats(4)
  p = make_text(x)
  t = twitter()
  if dchart("BTC") is True:
    t.create_tweet(text=p,img="chart.png")
  else:
    pass

def reps():
  """
  this function checks for replies with crypto symbols, and if it finds 
  them, then it replies with chart of asked symbol
  """
  history=[]
  t = twitter()
  c = cmc()
  syms = c.getsymbols()
  reps = t.replies()
  with open("history.txt", 'r') as f:
    hist = [line.rstrip('\n') for line in f]
  for i in reps:
    if str(i[0]) not in hist:
      a = (i[1].replace("@"+t.name+" ","")).upper()
      hist.append(i[0])
      if a in syms:
        if dchart(a) is True:
          t.api.update_status_with_media(status=a+'\n#{} ${}'.format(a,a),filename="chart.png",in_reply_to_status_id= str(i[0]),auto_populate_reply_metadata=True)

  with open("history.txt", 'w') as f:
    for s in hist:
        f.write(str(s) + '\n')


def alert():
  """
  function loads price history from file and updates it with new prices,
  also it checks whether there is any coin that has grew over x% in last
  few minutes and if it does it posts tweet with its chart
  for now x is set to 5
  """
  with open('pricehis.pkl', 'rb') as f:
    pr = pickle.load(f)
  c = cmc()
  t = twitter()
  x = c.prices4alert(pr)
  pr = x[0]
  syms = x[1]
  with open('pricehis.pkl', 'wb') as f:
    pickle.dump(pr, f)
  a = 0 #this is to avoid 30+ posts when whole market goes up
  for i in syms:
    if len(pr[i]) >=2:
      d = (pr[i][-1]/pr[i][-2] -1)*100
      if  d >= 5 and a <= 2:
        a += 1
        if dchart(i) is True:
          t.api.update_status_with_media(status="Price alert! {} is up {} % !!\n#{} ${}".format(i,round(d,2),i,i),filename="chart.png")
      elif d <= -5 and a <=2:
        a+=1
        if dchart(i) is True:
          t.api.update_status_with_media(status="Price alert! {} is down {} % !!\n#{} ${}".format(i,abs(round(d,2)),i,i),filename="chart.png")


def main():
  firebase = pyrebase.initialize_app(config)
  storage = firebase.storage()
  storage.child("history.txt").download("history.txt","history.txt")
  while True:
    up()
    for i in range(16):
      time.sleep(900)
      reps()
      time.sleep(900)
      reps()
      alert()
    storage.child("history.txt").put("history.txt")


if __name__ =='__main__':
  main()
