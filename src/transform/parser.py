import pandas as pd

def transform_bhavcopy_csv(file_path: str, symbol: str) -> pd.DataFrame:
    # Below columns are required from the CSV
    columns = ['TradDt', 'Sgmt', 'Src',
               'TckrSymb', 'XpryDt', 'StrkPric',
               'OptnTp', 'FinInstrmNm', 'OpnPric', 'HghPric', 'LwPric', 'ClsPric',
               'LastPric', 'PrvsClsgPric', 'UndrlygPric', 'SttlmPric', 'OpnIntrst',
               'ChngInOpnIntrst', 'TtlTradgVol', 'TtlTrfVal', 'TtlNbOfTxsExctd']

    df = pd.read_csv(file_path, usecols=columns)

    # Filter using the symbol, e.g., NIFTY, BANKNIFTY, etc.
    df = df[df['TckrSymb'] == symbol]

    # Rename columns to prepare data for ingestion into the DB
    df.rename(
        columns={
            'TradDt': 'date',
            'Sgmt': 'segment',
            'src': 'exchange',
            'TckrSymb': 'symbol',
            'XpryDt': 'expiry_date',
            'StrkPric': 'strike_price',
            'OptnTp': 'option_type',
            'FinInstrmNm': 'instrument_name',
            'OpnPric': 'open_price',
            'HghPric': 'high_price',
            'LwPric': 'low_price',
            'ClsPric': 'close_price',
            'LastPric': 'last_traded_price',
            'PrevClsgPric': 'previous_closing_price',
            'UndrlygPric': 'underlying_price',
            'SttlmPric': 'settlement_price',
            'OpnIntrst': 'open_interest',
            'ChngInOpnIntrst': 'change_in_open_interest',
            'TtlTradgVol': 'total_traded_volume',
            'TtlTrfVal': 'total_traded_value',
            'TtlNbOfTxsExctd': 'number_of_trades'
        },
        inplace=True
    )
    df.reset_index(inplace=True)

    return df
