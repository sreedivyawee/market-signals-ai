import yfinance as yf

from models.schemas import AgentResult, AgentResultData, Source


def yahoo_ticker(ticker: str) -> str:
    """
    Convert a user-facing Indian stock ticker such as TCS
    into the Yahoo Finance ticker TCS.NS.
    """
    if "." not in ticker:
        return f"{ticker}.NS"

    return ticker


def volume_agent(ticker: str) -> AgentResult:

    try:
        # Convert TCS -> TCS.NS for Yahoo Finance
        yf_ticker = yahoo_ticker(ticker)

        # Get 3 months of historical market data
        stock = yf.Ticker(yf_ticker)
        df = stock.history(period="3mo")

        if df.empty:
            raise ValueError(
                f"No market data found for {ticker}"
            )

        # Current values
        current_volume = float(
            df["Volume"].iloc[-1]
        )

        current_price = float(
            df["Close"].iloc[-1]
        )

        previous_price = float(
            df["Close"].iloc[-2]
        )

        # 20-day average volume
        average_volume = float(
            df["Volume"].rolling(20).mean().iloc[-1]
        )

        # Prevent division by zero
        if average_volume == 0:
            raise ValueError(
                f"Average volume is zero for {ticker}"
            )

        # Volume ratio
        volume_ratio = (
            current_volume / average_volume
        )

        # Recent price movement
        price_change = (
            (current_price - previous_price)
            / previous_price
        )

        # Classify volume activity
        if volume_ratio >= 2.0:

            anomaly = "EXTREME"

        elif volume_ratio >= 1.5:

            anomaly = "HIGH"

        elif volume_ratio >= 1.2:

            anomaly = "ELEVATED"

        else:

            anomaly = "NORMAL"

        # Determine market signal
        #
        # High volume + rising price = bullish
        # High volume + falling price = bearish
        # Normal volume = neutral

        if volume_ratio < 1.2:

            classification = "NEUTRAL"
            score = 0.0

        elif price_change > 0:

            classification = "BULLISH"

            score = min(
                (volume_ratio - 1.0) / 2.0,
                1.0
            )

        else:

            classification = "BEARISH"

            score = -min(
                (volume_ratio - 1.0) / 2.0,
                1.0
            )

        # Confidence
        confidence = min(
            abs(score) + 0.2,
            1.0
        )

        # Human-readable reasoning
        reasoning = [

            f"Current volume is "
            f"{volume_ratio:.2f}x "
            f"the 20-day average.",

            f"Volume activity is classified "
            f"as {anomaly}.",

            f"Recent price movement is "
            f"{price_change * 100:.2f}%."
        ]

        # Return the common AgentResult structure
        return AgentResult(

            agent_name="volume_agent",

            status="success",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification=classification,

                confidence=confidence,

                score=score,

                summary=(
                    f"{anomaly.capitalize()} volume detected: "
                    f"{volume_ratio:.2f}x "
                    f"the 20-day average."
                ),

                reasoning=reasoning,
            ),

            sources=[

                Source(

                    type="market_data",

                    name="Yahoo Finance",

                    reference=(
                        f"{ticker} historical volume "
                        f"and price data"
                    ),
                )
            ],

            metadata={

                "current_volume":
                    current_volume,

                "average_volume":
                    average_volume,

                "volume_ratio":
                    volume_ratio,

                "current_price":
                    current_price,

                "price_change":
                    price_change,

                "yahoo_ticker":
                    yf_ticker,
            },
        )

    except Exception as e:

        return AgentResult(

            agent_name="volume_agent",

            status="error",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification="UNKNOWN",

                confidence=0.0,

                score=0.0,

                summary="Unable to analyze volume.",

                reasoning=[
                    str(e)
                ],
            ),

            sources=[],

            metadata={},
        )