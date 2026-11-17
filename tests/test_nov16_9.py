import pandas as pd
import pytest
from natgas_analytics.curve import curve_matrix
def test_duplicate_quote_cannot_depend_on_input_order():
    df=pd.DataFrame({"date":pd.to_datetime(["2020-01-01"]*2),"contract":["2020-02"]*2,"price":[2,3]})
    for rows in (df,df.iloc[::-1]):
        with pytest.raises(ValueError,match="one quote"):
            curve_matrix(rows)
