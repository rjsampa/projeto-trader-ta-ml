# Summary

A modeling pipeline aimed at constructing machine learning models that generate buy and sell signals for a group of B3 stocks.

## Labels

The signals used for model training are based on the method presented by Sezer & Ozbayoglu (2018). For each step $S_{t}$ in a historical price series $S$ of a stock, the signal at time step $S_{t+1}$ is given by:

Considering a time window $W=11$, where $W_{min}$ represents the lowest price, $W_{max}$ the highest price, and $W_{median}$ the median price:

- If $W_{median} = W_{min}$:
  - Signal = Buy (1)
- If $W_{median} = W_{max}$:
  - Signal = Sell (2)
- Otherwise:
  - Signal = Hold (0)

## Reference

Sezer, O. B., & Ozbayoglu, A. M. (2018). Algorithmic financial trading with deep convolutional neural networks: Time series to image conversion approach. *Applied Soft Computing*, 70, 525–538.

## Pipeline Structure

1. Development dataset creation
2. Analysis of the development dataset
3. Strategy 1 models
4. Strategy 2 models

## Dataset Construction

The dataset is built using Yahoo Finance. In the first step, daily prices of 165 stocks listed on B3 are collected. In the second step, a group of stocks with similar correlations is selected using an unsupervised classification algorithm. In the third step, 177 technical analysis features are generated using `pandas_ta`. The parameters used in this step are the defaults from the package itself. Finally, the final dataset is defined by removing highly correlated features, resulting in 106 features for modeling.

## Modeling Strategies

Two strategies are tested:

1. **Direct Modeling**
   - The target is the signal, and the model features are the corresponding *features-ta*.

2. **Convolution**
   - The target is the signal, and the input is an image $W \times F$, where $W$ is a time window preceding the target step, and $F$ is the set of *features-ta*. The idea behind this strategy is to leverage the potential of convolutional networks for prediction.
