from duckdb import DuckDBPyConnection

import logging
logger = logging.getLogger(__name__)

def load_bhavcopy(con: DuckDBPyConnection, file_path: str, symbol: str):
    query = build_load_query(file_path, symbol)
    con.execute(query)
    logger.info("Executed load query")

def build_load_query(csv_path: str, symbol: str) -> str:
    query = f"""
    INSERT INTO nifty_options
    SELECT
        TradDt AS date,
        Sgmt AS segment,
        Src AS exchange,
        TckrSymb AS symbol,
        XpryDt AS expiry_date,
        StrkPric AS strike_price,
        OptnTp AS option_type,
        FinInstrmNm AS instrument_name,
        OpnPric AS open_price,
        HghPric AS high_price,
        LwPric AS low_price,
        ClsPric AS close_price,
        LastPric AS last_traded_price,
        PrvsClsgPric AS previous_closing_price,
        UndrlygPric AS underlying_price,
        SttlmPric AS settlement_price,
        OpnIntrst AS open_interest,
        ChngInOpnIntrst AS change_in_open_interest,
        TtlTradgVol AS total_traded_volume,
        TtlTrfVal AS total_traded_value,
        TtlNbOfTxsExctd AS number_of_trades
    FROM read_csv_auto('{csv_path}')
    WHERE TckrSymb = '{symbol}'
    ON CONFLICT DO NOTHING
    """

    logger.debug("Load Query: %s", query)
    logger.info("Constructed load query with csv_path: '%s' and symbol: '%s'", csv_path, symbol)

    return query