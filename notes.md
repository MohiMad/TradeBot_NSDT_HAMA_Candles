/* conditions for a "buy" text sign */
### high = current high price in the candlestick

### ma1 = ma(high, 200, SMA)
### ma2 = ma(low, 200, SMA)

### SMA = sum_of_all_prices_(high or low)/200

## Hlv1 = float(na)
## Hlv1 := (close > ma1) ? 1 : (close < ma2) ? -1 : Hlv1[1]

# if
# Hlv1 == 1 and Hlv1[1] == -1
# then show buy signal


--- Some markets do give a "buy" signal although they're false --- 
To work around it, the NSDT indicator must have no flaws


----------------------------------------------------------------------------------

OpenType = HighType = LowType = CloseType = MAType = "EMA"
OpenLength = 25
HighLength = 20
LowLength = 20
CloseLength = 20
LengthMA = 100

MASource = close

TypeOpen = OpenType
SourceOpen = (open[1] + close[1])/2
LengthOpen = OpenLength

TypeHigh = HighType
SourceHigh = max(high, close)
LengthHigh = HighLength

TypeLow = LowType
SourceLow = min(low, close)
LengthLow = LowLength

TypeClose = CloseType
SourceClose = (open + high + low + close)/4
LengthClose = CloseLength

