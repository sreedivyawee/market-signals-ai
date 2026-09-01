from p3.profile import get_user_profile
from p3.portfolio import calculate_portfolio_allocation


def get_result_data(agent_output):
    """
    Extract the result from an agent response.

    Supports both dictionaries and Pydantic objects.
    """

    if agent_output is None:
        return {}

    if isinstance(agent_output, dict):
        return agent_output.get("result", {})

    return getattr(agent_output, "result", {})


def get_value(obj, key, default=None):
    """
    Read a value from either a dictionary or Pydantic object.
    """

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def personalize_user(
    user_id,
    ticker,
    agent_results,
    current_prices,
    synthesis_result=None
):
    """
    Personalize the market analysis for a specific user.
    """

    # ==================================================
    # 1. GET USER PROFILE
    # ==================================================

    profile = get_user_profile(user_id)

    if profile is None:
        return {
            "error": "User not found"
        }

    # ==================================================
    # 2. GET SYNTHESIS RESULT
    # ==================================================

    market_signal = "HOLD"
    market_confidence = 0.0

    if synthesis_result:

        market_signal = synthesis_result.get(
            "signal",
            "HOLD"
        )

        market_confidence = synthesis_result.get(
            "confidence",
            0.0
        )

    # ==================================================
    # 3. CALCULATE PORTFOLIO ALLOCATION
    # ==================================================

    allocation = calculate_portfolio_allocation(
        user_id,
        current_prices
    )

    if allocation is None:
        return {
            "error": "Portfolio not found"
        }

    current_exposure = allocation.get(
        ticker,
        0
    )

    # ==================================================
    # 4. READ P1 AGENT RESULTS
    # ==================================================

    volatility_output = agent_results.get(
        "volatility_agent"
    )

    volume_output = agent_results.get(
        "volume_agent"
    )

    news_output = agent_results.get(
        "news_agent"
    )

    # Extract actual result objects

    volatility_result = get_result_data(
        volatility_output
    )

    volume_result = get_result_data(
        volume_output
    )

    news_result = get_result_data(
        news_output
    )

    # ==================================================
    # 5. EXTRACT AGENT VALUES
    # ==================================================

    volatility_classification = get_value(
        volatility_result,
        "classification",
        "UNKNOWN"
    )

    volatility_confidence = get_value(
        volatility_result,
        "confidence",
        0.0
    )

    volatility_score = get_value(
        volatility_result,
        "score",
        0.0
    )

    volume_classification = get_value(
        volume_result,
        "classification",
        "UNKNOWN"
    )

    volume_confidence = get_value(
        volume_result,
        "confidence",
        0.0
    )

    volume_score = get_value(
        volume_result,
        "score",
        0.0
    )

    sentiment_classification = get_value(
        news_result,
        "classification",
        "UNKNOWN"
    )

    sentiment_confidence = get_value(
        news_result,
        "confidence",
        0.0
    )

    sentiment_score = get_value(
        news_result,
        "score",
        0.0
    )

    # ==================================================
    # 6. DETERMINE CONCENTRATION
    # ==================================================

    if current_exposure > 40:

        concentration = "HIGH"

    elif current_exposure >= 20:

        concentration = "MEDIUM"

    else:

        concentration = "LOW"

    # ==================================================
    # 7. DETERMINE CAUTION LEVEL
    # ==================================================

    caution_level = "LOW"

    if profile["risk_level"] == "low":

        if volatility_classification == "HIGH_RISK":
            caution_level = "HIGH"

        if concentration == "HIGH":
            caution_level = "HIGH"

    elif profile["risk_level"] == "high":

        if volatility_classification == "HIGH_RISK":
            caution_level = "MEDIUM"

    # ==================================================
    # 8. PERSONALIZED MESSAGE
    # ==================================================

    if caution_level == "HIGH":

        message = (
            "High caution is advised because the user "
            "has a low risk tolerance, high existing "
            "exposure, or elevated stock volatility."
        )

    elif caution_level == "MEDIUM":

        message = (
            "Moderate caution is advised because the "
            "stock shows elevated risk."
        )

    else:

        message = (
            "The current market signals appear relatively "
            "suitable for the user's risk profile."
        )

    # ==================================================
    # 9. PERSONALIZED RECOMMENDATION
    # ==================================================

    personalized_signal = market_signal

    if caution_level == "HIGH":

        if market_signal == "BULLISH":
            personalized_signal = "HOLD"

        elif market_signal == "BEARISH":
            personalized_signal = "SELL"

    elif caution_level == "MEDIUM":

        if market_signal == "BULLISH":
            personalized_signal = "HOLD"

    # ==================================================
    # 10. FINAL PERSONALIZATION RESULT
    # ==================================================

    return {

        "user_id": user_id,

        "ticker": ticker,

        "user_profile": {

            "risk_level":
                profile["risk_level"],

            "investment_horizon":
                profile["investment_horizon"],

            "investment_amount":
                profile["investment_amount"]
        },

        "portfolio": {

            "current_exposure_percent":
                current_exposure,

            "concentration":
                concentration,

            "allocation":
                allocation
        },

        "market_signals": {

            "volatility": {

                "classification":
                    volatility_classification,

                "confidence":
                    volatility_confidence,

                "score":
                    volatility_score
            },

            "volume": {

                "classification":
                    volume_classification,

                "confidence":
                    volume_confidence,

                "score":
                    volume_score
            },

            "sentiment": {

                "classification":
                    sentiment_classification,

                "confidence":
                    sentiment_confidence,

                "score":
                    sentiment_score
            }
        },

        "personalization": {

            "caution_level":
                caution_level,

            "message":
                message
        },

        "recommendation": {

            "market_signal":
                market_signal,

            "market_confidence":
                market_confidence,

            "personalized_signal":
                personalized_signal
        }
    }


# ======================================================
# SIMPLE TEST
# ======================================================

if __name__ == "__main__":

    current_prices = {

        "TCS": 3500,

        "INFY": 1500,

        "RELIANCE": 2500
    }

    test_agent_results = {

        "volatility_agent": {

            "status": "success",

            "result": {

                "classification":
                    "LOW_RISK",

                "confidence":
                    0.57,

                "score":
                    -0.37
            }
        },

        "volume_agent": {

            "status": "success",

            "result": {

                "classification":
                    "NEUTRAL",

                "confidence":
                    0.20,

                "score":
                    0.0
            }
        },

        "news_agent": {

            "status": "success",

            "result": {

                "classification":
                    "NEUTRAL",

                "confidence":
                    0.24,

                "score":
                    -0.04
            }
        }
    }

    test_synthesis = {

        "signal": "HOLD",

        "confidence": 0.50
    }

    result = personalize_user(

        user_id="U001",

        ticker="TCS",

        agent_results=test_agent_results,

        current_prices=current_prices,

        synthesis_result=test_synthesis
    )

    print(result)