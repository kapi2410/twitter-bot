# CryptoBot24

This is a simple Twitter bot that:

- Posts crypto price updates from time to time.
- Checks for replies to its tweets with cryptocurrency symbols and responds with price charts for those symbols.
- Every ten minutes, snapshots the top 100 crypto prices and posts a price alert tweet if there is a significant change.

### APIs Used
- [CoinMarketCap](https://coinmarketcap.com)
- [Twitter](https://twitter.com)
- [Chart-Img](https://chart-img.com)

Deployed on Heroku.

You can see this bot in action [here](https://twitter.com/CryptoBot24).

**Note**: This project was created in 2022, and the APIs used might have changed since then.

### Files Description
- **history.txt**: Stores history of answered tweets to prevent the bot from replying twice to the same comment.
- **pricehis.pkl**: Stores price history as a dictionary.
- **chart.png**: The script saves the latest chart it creates with this name.

### Few Screenshots
Here are some screenshots demonstrating the bot in action:

![Posting Price Updates](screenshots/1.png)
*Posting price updates*

![Price Alerts](screenshots/2.png)
*Price alerts*

![Price Alerts](screenshots/3.png)
*Price alerts*

![Replying to Replies with Symbols](screenshots/4.png)
*Replying to replies with symbols*
