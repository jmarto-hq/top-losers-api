import unittest
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from unittest.mock import patch
from api.data import DataError, universe_payload, chart_quote, history_payload

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

 def test_extended_percent_uses_previous_regular_bar(self):
  day=datetime.now(ZoneInfo("America/New_York")).replace(hour=9,minute=30,second=0,microsecond=0)
  start=int(day.timestamp());end=start+23400
  previous=int((day-timedelta(days=1)).replace(hour=15,minute=59).timestamp())
  meta={'currentTradingPeriod':{'regular':{'start':start,'end':end},'pre':{'start':start-19800},'post':{'end':end+14400}}}
  data={'chart':{'result':[{'meta':meta,'timestamp':[previous,start-1800,start+1800,end+1800],'indicators':{'quote':[{'close':[100,90,110,112],'volume':[1,1,1,1]}]}}]}}
  result=chart_quote('AAA',data)['sessions']
  self.assertEqual(result['PRE']['reference_price'],100)
  self.assertAlmostEqual(result['PRE']['change_percent'],-10)
  self.assertEqual(result['POST']['reference_price'],110)
 def test_unknown_timestamp_stays_unknown(self):
  result=universe_payload(self.payload([self.item()]),'date')
  self.assertIsNone(result['top_losers'][0]['quote_as_of'])
  self.assertEqual(result['quote_timestamp_coverage'],0)
 def test_nonfinite_price_is_not_accepted(self):
  item=self.item();item['regularMarketPrice']=float('nan')
  with self.assertRaises(DataError):universe_payload(self.payload([item]),'date')

if __name__=='__main__':unittest.main()

class HistoryTests(unittest.TestCase):
    def test_history_does_not_fabricate_missing_fields(self):
        data={"chart":{"result":[{"timestamp":[1788269400,1788355800],"indicators":{"quote":[{"close":[10,None],"volume":[5,6]}]}}]}}
        row=history_payload("ABC",data)
        self.assertEqual(len(row["bars"]),1)
        self.assertIsNone(row["bars"][0]["open"])
        self.assertIsNone(row["bars"][0]["adjusted_close"])
        self.assertEqual(row["bars"][0]["close"],10)
    def test_empty_history_is_explicit_failure(self):
        with self.assertRaises(ValueError):
            history_payload("ABC",{"chart":{"result":[]}})
