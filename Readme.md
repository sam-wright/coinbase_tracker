# Coinbase Tracker (Cryptocurrency Speculation)

This python3 utility can be run as a service(via cron) to monitor the Coinbase market and buy/sell on your behalf based on your set criteria. So far modest returns have been relatively trivial to attain. Although there have been some notiable shortcomings in the simple employed algoritym. 

## To use:
Simply fill in your `config.py` with your coinbase credentials and a gmail address for debugging and notifications. I run my monitor through `cron` to reevaluate the market at set intervals.

## Contributions:

I am absolutely interested in community contributions or feedback. 

## Future Improvements:

- Since you log the prices by default, it would be nice to employ some machine learning to the buy/sell algorithms
- I hope to make this more modular so that it will be simple to drop in new buy/sell algorithms.
- It would be nice to not be tied directly to Coinbase


