from datetime import timedelta
from unittest.mock import Mock
import time
import pandas as pd
import pytest
from natgas_analytics import weather

def test_multiyear_requests_use_bounded_contiguous_daily_ranges(monkeypatch):
    calls=[]
    def get(*args,params,**kwargs):
        first,last=pd.Timestamp(params['startdate']),pd.Timestamp(params['enddate'])
        assert (last-first).days <= 364
        calls.append((first,last))
        response=Mock();response.json.return_value={'results':[{'date':first.isoformat(),'value':50},{'date':last.isoformat(),'value':60}]}
        return response
    monkeypatch.setattr(weather.requests,'get',get);monkeypatch.setattr(time,'sleep',lambda _:None)
    out=weather.download_noaa_daily('token','station','2023-01-01','2025-01-02')
    assert len(calls)==3
    assert all(calls[i][0]==calls[i-1][1]+timedelta(days=1) for i in range(1,len(calls)))
    assert out['date'].min()==pd.Timestamp('2023-01-01') and out['date'].max()==pd.Timestamp('2025-01-02')

def test_metadata_pages_are_not_silently_truncated(monkeypatch):
    offsets=[]
    def get(*args,params,**kwargs):
        offset=params.get('offset',1);offsets.append(offset)
        response=Mock();response.json.return_value={'results':[{'date':f'2025-01-0{offset}','value':50}], 'metadata':{'resultset':{'count':2}}}
        return response
    monkeypatch.setattr(weather.requests,'get',get);monkeypatch.setattr(time,'sleep',lambda _:None)
    assert len(weather.download_noaa_daily('token','station','2025-01-01','2025-01-02'))==2
    assert offsets==[1,2]

def test_reversed_dates_are_rejected_before_download(monkeypatch):
    request=Mock();monkeypatch.setattr(weather.requests,'get',request)
    with pytest.raises(ValueError,match='date range'):
        weather.download_noaa_daily('token','station','2025-02-01','2025-01-01')
    request.assert_not_called()
