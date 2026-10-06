import unittest
from unittest.mock import patch
from api.data import DataError, universe_payload, chart_quote

class DataTests(unittest.TestCase):
 def item(self, symbol='AAA', **kw):
  return dict(symbol=symbol, regularMarketPrice=20, regularMarketChangePercent=-4, marketCap=3e9, **kw)
 def payload(self, quotes):return {'finance':{'result':[{'quotes':quotes}]}}
 def test_max_250_order(self):
  result=universe_payload(self.payload([self.item(str(i)) for i in range(260)]),'date')
  self.assertEqual(len(result['top_losers']),250)
  self.assertEqual(result['top_losers'][0]['ticker'],'0')
  self.assertEqual(result['top_losers'][-1]['ticker'],'249')
 def test_gate_and_timestamp(self):
  items=[self.item('AAA',regularMarketTime=1700000000), self.item('BBB')]
  items[1]['marketCap']=1e9
  result=universe_payload(self.payload(items),'date')
  self.assertEqual(result['total_encontrados'],1)
  self.assertEqual(result['quote_timestamp_coverage'],1)
  self.assertEqual(result['price_session'],'REGULAR')
  self.assertIsNone(result['delay_minutes'])
 def test_bad_price_not_zero(self):
  item=self.item();item['regularMarketPrice']=None
  with self.assertRaises(DataError):universe_payload(self.payload([item]),'date')
 def test_upstream_error_not_empty_success(self):
  with self.assertRaises(DataError):universe_payload({'finance':{'error':{'code':'x'},'result':[]}},'date')
 def test_no_extended_data_is_explicit(self):
  start=1791293400;end=start+23400
  data={'chart':{'result':[{'meta':{'currentTradingPeriod':{'regular':{'start':start,'end':end}}},'timestamp':[start], 'indicators':{'quote':[{'close':[20],'volume':[100]}]}}]}}
  result=chart_quote('AAA',data)
  self.assertIsNone(result['sessions']['PRE'])
  self.assertIsNone(result['sessions']['POST'])
  self.assertEqual(result['sessions']['REGULAR']['kind'],'ONE_MINUTE_BAR')

if __name__=='__main__':unittest.main()
