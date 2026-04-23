from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=330)

trends = pytrends.trending_searches(pn='india')

print(trends.head(10))