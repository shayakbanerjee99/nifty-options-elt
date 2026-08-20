CREATE_NIFTY_OPTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS nifty_options (
    date DATE,
    segment VARCHAR,
    exchange VARCHAR,
    symbol VARCHAR,
    expiry_date DATE,
    strike_price DOUBLE,
    option_type VARCHAR,
    instrument_name VARCHAR,
    open_price DOUBLE,
    high_price DOUBLE,
    low_price DOUBLE,
    close_price DOUBLE,
    last_traded_price DOUBLE,
    previous_closing_price DOUBLE,
    underlying_price DOUBLE,
    settlement_price DOUBLE,
    open_interest BIGINT,
    change_in_open_interest BIGINT,
    total_traded_volume BIGINT,
    total_traded_value DOUBLE,
    number_of_trades BIGINT,
    PRIMARY KEY (date, symbol, expiry_date, instrument_name)
)
"""

def create_schema(con):
    con.execute(CREATE_NIFTY_OPTIONS_TABLE)