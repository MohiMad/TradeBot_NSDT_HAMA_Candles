# NSDT HAMA Candles Day-Trading Strategy Algorithm  

## Introduction  
This project involves the implementation of a trading strategy based on multiple indicators applied to the top 500 performing cryptocurrencies by total market capitalization. The strategy used is the [NSDT HAMA Candles](https://www.tradingview.com/script/B4dBAINf-NSDT-HAMA-Candles-STRAT/) strategy, which relies on visual indicators from TradingView. This repository aims to refine the strategy by reducing bias and human error, running the algorithm every 15 minutes to analyze market trends.  

## Strategy  
The core of this strategy is the Heiken Ashi Moving Average (HAMA) candles, which help smooth price fluctuations and identify trends more clearly. To strengthen its predictive accuracy, the algorithm incorporates additional indicators such as exponential moving averages (EMAs) to confirm trend direction and the relative strength index (RSI) to assess overbought and oversold conditions. By analyzing these factors, the algorithm seeks to optimize entry points and increase the probability of successful trades.  

## Results  
While the algorithm is effective at predicting entry points, it still has flaws, particularly a high rate of false positives. The cause of these inaccuracies was unclear at the time the code was written. Despite this, the algorithm provides valuable insights into potential investment opportunities by identifying market trends with reasonable accuracy.  

## Future Improvements  
To reduce the occurrence of false positives, the algorithm needs to store and analyze a larger dataset instead of relying solely on the most recent data point. Another key improvement would be incorporating exit point predictions, as the current implementation only focuses on entry points. Additionally, simulating the strategy with a fictional trading account and tracking its performance over time would help evaluate its average return on investment (ROI) and fine-tune its effectiveness.