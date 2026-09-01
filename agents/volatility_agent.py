import yfinance as yf
import numpy as np

from models.schemas import AgentResult, AgentResultData, Source


def volatility_agent(ticker: str) -> AgentResult:

    try:
        # Get 6 months of historical price data
        stock = yf.Ticker(ticker)
        df = stock.history(period="6mo")

        if df.empty:
            raise ValueError(f"No market data found for {ticker}")

        # Calculate daily returns
        returns = df["Close"].pct_change().dropna()

        # Calculate 30-day rolling volatility
        daily_volatility = returns.rolling(30).std().iloc[-1]

        # Annualize volatility
        annualized_volatility = (
            daily_volatility * np.sqrt(252)
        )

        volatility = float(annualized_volatility)

        # Classify volatility
        if volatility >= 0.50:

            classification = "HIGH_RISK"

        elif volatility >= 0.30:

            classification = "ELEVATED_RISK"

        else:

            classification = "LOW_RISK"

        # Convert volatility into a score
        #
        # Higher volatility = more risk
        # Therefore higher volatility gives a more negative score.

        score = -min(
            volatility / 0.8,
            1.0
        )

        # Confidence
        confidence = min(
            abs(score) + 0.2,
            1.0
        )

        reasoning = [

            f"30-day annualized volatility is "
            f"{volatility * 100:.2f}%.",

            f"Volatility level is classified as "
            f"{classification}.",

            "Higher volatility indicates greater "
            "short-term price uncertainty."

        ]

        return AgentResult(

            agent_name="volatility_agent",

            status="success",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification=classification,

                confidence=confidence,

                score=score,

                summary=(
                    f"30-day annualized volatility is "
                    f"{volatility * 100:.2f}%."
                ),

                reasoning=reasoning,

            ),

            sources=[

                Source(

                    type="market_data",

                    name="Yahoo Finance",

                    reference=(
                        f"{ticker} historical price data"
                    ),

                )

            ],

            metadata={

                "annualized_volatility": volatility,

                "daily_volatility": float(
                    daily_volatility
                ),

                "window_days": 30,

            },

        )

    except Exception as e:

        return AgentResult(

            agent_name="volatility_agent",

            status="error",

            input={
                "ticker": ticker
            },

            result=AgentResultData(

                classification="UNKNOWN",

                confidence=0.0,

                score=0.0,

                summary="Unable to analyze volatility.",

                reasoning=[
                    str(e)
                ],

            ),

            sources=[],

            metadata={},

        )