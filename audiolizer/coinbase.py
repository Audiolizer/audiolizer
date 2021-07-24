# ## Experimental coinbase api
#


import cbpro
public_client = cbpro.PublicClient()

# How to get trading pairs

import pandas as pd

# ## Ticker symbols

products = public_client.get_products()

pd.DataFrame(products)

# ## Order book

# Best current order: each entry is in `price`, `size`, `num-orders`

best = public_client.get_product_order_book('BTC-USD')
pd.DataFrame(best)

# Top 50

best50 = public_client.get_product_order_book('BTC-USD', level=2)
pd.DataFrame(best50).head()

btc_tick = public_client.get_product_ticker('BTC-USD')
pd.Series(btc_tick)

# ## Historic rates

btc_hist = public_client.get_product_historic_rates('BTC-USD')

df = pd.DataFrame(btc_hist, columns = ['time', 'low', 'high', 'open', 'close', 'volume']).set_index('time')

df.index = pd.to_datetime(df.index, unit='s')
df.sort_index(inplace=True)

df

# +
# public_client.get_product_historic_rates?
# -

btc_hist

# ## websocket feed
#
# https://docs.pro.coinbase.com//#websocket-feed
