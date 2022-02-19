This is simple twitter bot that:
 -posts crypto price updates from time to time,
 -checks for replies to its tweets with cryptocyrrency symbols and will 
    asnwear them with price charts for that symbol,
 -every ten minutes snapshots top100 cryptos prices and if there is huge
    change it will post price alert tweet,

Mostly based on APIs:
    -https://coinmarketcap.com
    -https://twitter.com/
    -https://chart-img.com/ 

Deployed on heroku.

You can see this bot in "action"* here : https://twitter.com/CryptoBot24

*Sadly it doesnt work 24/7 as i didnt want to pay for apis/heroku.

files describtion:
    -history.txt - stores history of answeared tweets so bot doesnt reply twice to one comment
    -pricehis.pkl - stores price history as dictionary
    -chart.png - everytime script creates chart it saves it like this
    