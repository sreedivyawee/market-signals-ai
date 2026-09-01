import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from models.schemas import AgentResult, AgentResultData, Source


# --------------------------------------------------
# Company name mapping
# --------------------------------------------------

company_names = {
    "TCS.NS": "TCS",
    "INFY.NS": "INFOSYS",
    "RELIANCE.NS": "RELIANCE",

    "AAPL": "APPLE",
    "TSLA": "TESLA",
    "NVDA": "NVIDIA",
    "MSFT": "MICROSOFT",
    "GOOGL": "GOOGLE",
    "AMZN": "AMAZON",
    "META": "META",
    "NFLX": "NETFLIX",
    "AMD": "AMD",
    "INTC": "INTEL"
}


# --------------------------------------------------
# Convert user ticker to Yahoo Finance ticker
# --------------------------------------------------

def yahoo_ticker(ticker: str) -> str:

    ticker = ticker.upper().strip()

    # Indian stocks
    if ticker in ["TCS", "INFY", "RELIANCE"]:
        return f"{ticker}.NS"

    # Already has exchange suffix
    if "." in ticker:
        return ticker

    # US stocks remain unchanged
    return ticker


# --------------------------------------------------
# Create sentiment analyzer
# --------------------------------------------------

analyzer = SentimentIntensityAnalyzer()


def news_agent(ticker: str) -> AgentResult:

    try:

        # --------------------------------------------------
        # 1. Convert ticker
        # --------------------------------------------------

        yf_ticker = yahoo_ticker(ticker)

        # --------------------------------------------------
        # 2. Get recent news
        # --------------------------------------------------

        stock = yf.Ticker(yf_ticker)

        news = stock.news

        if not news:

            raise ValueError(
                f"No recent news found for {ticker}"
            )

        # --------------------------------------------------
        # 3. Find company name
        # --------------------------------------------------

        ticker_upper = yf_ticker.upper()

        company_name = company_names.get(
            ticker_upper,
            ticker.upper()
        )

        # --------------------------------------------------
        # 4. Extract relevant headlines
        # --------------------------------------------------

        headlines = []

        for item in news:

            content = item.get(
                "content",
                {}
            )

            title = content.get(
                "title",
                ""
            )

            if not title:
                continue

            title_upper = title.upper()

            # Keep relevant company headlines
            if (
                ticker_upper in title_upper
                or company_name in title_upper
            ):

                headlines.append(title)

            if len(headlines) >= 10:
                break

        # --------------------------------------------------
        # 5. Check headlines
        # --------------------------------------------------

        if not headlines:

            raise ValueError(
                f"No relevant news headlines "
                f"found for {ticker}"
            )

        # --------------------------------------------------
        # 6. Analyze sentiment
        # --------------------------------------------------

        sentiment_scores = []

        for headline in headlines:

            sentiment = (
                analyzer.polarity_scores(
                    headline
                )
            )

            score = sentiment["compound"]

            sentiment_scores.append(score)

        # --------------------------------------------------
        # 7. Calculate average sentiment
        # --------------------------------------------------

        average_score = (
            sum(sentiment_scores)
            / len(sentiment_scores)
        )

        # --------------------------------------------------
        # 8. Classification
        # --------------------------------------------------

        if average_score >= 0.20:

            classification = "BULLISH"

        elif average_score <= -0.20:

            classification = "BEARISH"

        else:

            classification = "NEUTRAL"

        # --------------------------------------------------
        # 9. Confidence
        # --------------------------------------------------

        confidence = min(
            abs(average_score) + 0.2,
            1.0
        )

        # --------------------------------------------------
        # 10. Reasoning
        # --------------------------------------------------

        reasoning = [

            f"Analyzed {len(headlines)} "
            f"relevant news headlines.",

            f"Average news sentiment score "
            f"is {average_score:.2f}.",

            f"Overall news sentiment is "
            f"{classification}."
        ]

        # --------------------------------------------------
        # 11. Return standard AgentResult
        # --------------------------------------------------

        return AgentResult(

            agent_name="news_agent",

            status="success",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification=classification,

                confidence=confidence,

                score=average_score,

                summary=(
                    f"Recent news sentiment is "
                    f"{classification.lower()} "
                    f"with a score of "
                    f"{average_score:.2f}."
                ),

                reasoning=reasoning
            ),

            sources=[

                Source(

                    type="news",

                    name="Yahoo Finance",

                    reference=headline

                )

                for headline in headlines

            ],

            metadata={

                "headlines_analyzed":
                    len(headlines),

                "headlines":
                    headlines,

                "sentiment_scores":
                    sentiment_scores,

                "yahoo_ticker":
                    yf_ticker
            }
        )

    # --------------------------------------------------
    # Error handling
    # --------------------------------------------------

    except Exception as e:

        return AgentResult(

            agent_name="news_agent",

            status="error",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification="UNKNOWN",

                confidence=0.0,

                score=0.0,

                summary="Unable to analyze news.",

                reasoning=[
                    str(e)
                ]
            ),

            sources=[],

            metadata={}
        )