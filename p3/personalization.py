from profile import get_user_profile
from portfolio import calculate_portfolio_allocation


def personalize_user(user_id, ticker, agent_results, current_prices):

    # -----------------------------
    # 1. Get user profile
    # -----------------------------
    profile = get_user_profile(user_id)

    if profile is None:
        return {"error": "User not found"}

    # -----------------------------
    # 2. Calculate portfolio allocation
    # -----------------------------
    allocation = calculate_portfolio_allocation(
        user_id,
        current_prices
    )

    if allocation is None:
        return {"error": "Portfolio not found"}

    # Percentage of the selected stock
    current_exposure = allocation.get(ticker, 0)

    # -----------------------------
    # 3. Read P1 agent results
    # -----------------------------

    volatility_agent = agent_results.get(
        "volatility_agent", {}
    )

    volume_agent = agent_results.get(
        "volume_agent", {}
    )

    news_agent = agent_results.get(
        "news_agent", {}
    )

    # P1 stores the useful information inside:
    # agent → result → classification/confidence/score

    volatility_result = volatility_agent.get(
        "result", {}
    )

    volume_result = volume_agent.get(
        "result", {}
    )

    news_result = news_agent.get(
        "result", {}
    )

    volatility_classification = volatility_result.get(
        "classification", "UNKNOWN"
    )

    volatility_confidence = volatility_result.get(
        "confidence", 0
    )

    volatility_score = volatility_result.get(
        "score", 0
    )

    volume_classification = volume_result.get(
        "classification", "UNKNOWN"
    )

    volume_confidence = volume_result.get(
        "confidence", 0
    )

    volume_score = volume_result.get(
        "score", 0
    )

    sentiment_classification = news_result.get(
        "classification", "UNKNOWN"
    )

    sentiment_confidence = news_result.get(
        "confidence", 0
    )

    sentiment_score = news_result.get(
        "score", 0
    )

    # -----------------------------
    # 4. Determine concentration
    # -----------------------------

    if current_exposure > 40:
        concentration = "HIGH"

    elif current_exposure >= 20:
        concentration = "MEDIUM"

    else:
        concentration = "LOW"

    # -----------------------------
    # 5. Determine caution level
    # -----------------------------

    caution_level = "LOW"

    if profile["risk_level"] == "low":

        if volatility_classification == "HIGH_RISK":
            caution_level = "HIGH"

        if concentration == "HIGH":
            caution_level = "HIGH"

    elif profile["risk_level"] == "high":

        if volatility_classification == "HIGH_RISK":
            caution_level = "MEDIUM"

    # -----------------------------
    # 6. Generate explanation
    # -----------------------------

    if caution_level == "HIGH":

        message = (
            "High caution is advised because the user "
            "has a low risk tolerance, high existing exposure, "
            "or elevated stock volatility."
        )

    elif caution_level == "MEDIUM":

        message = (
            "Moderate caution is advised because the stock "
            "shows elevated risk."
        )

    else:

        message = (
            "The current market signals appear relatively "
            "suitable for the user's risk profile."
        )

    # -----------------------------
    # 7. Return information for P2
    # -----------------------------

    return {

        "user_id": user_id,

        "ticker": ticker,

        "user_profile": {
            "risk_level": profile["risk_level"],
            "investment_horizon": profile["investment_horizon"],
            "investment_amount": profile["investment_amount"]
        },

        "portfolio": {
            "current_exposure_percent": current_exposure,
            "concentration": concentration
        },

        "market_signals": {

            "volatility": {
                "classification": volatility_classification,
                "confidence": volatility_confidence,
                "score": volatility_score
            },

            "volume": {
                "classification": volume_classification,
                "confidence": volume_confidence,
                "score": volume_score
            },

            "sentiment": {
                "classification": sentiment_classification,
                "confidence": sentiment_confidence,
                "score": sentiment_score
            }
        },

        "personalization": {
            "caution_level": caution_level,
            "message": message
        }
    }
if __name__ == "__main__":

    # Sample current market prices
    test_prices = {
        "TCS": 3500,
        "INFY": 1500,
        "RELIANCE": 2500
    }

    # Sample P1 output using the same structure P1 gave us
    test_agent_results = {

        "volatility_agent": {
            "status": "success",
            "result": {
                "classification": "LOW_RISK",
                "confidence": 0.57,
                "score": -0.37
            }
        },

        "volume_agent": {
            "status": "success",
            "result": {
                "classification": "NEUTRAL",
                "confidence": 0.20,
                "score": 0.0
            }
        },

        "news_agent": {
            "status": "success",
            "result": {
                "classification": "NEUTRAL",
                "confidence": 0.24,
                "score": -0.04
            }
        }
    }

    result = personalize_user(
        "U001",
        "TCS",
        test_agent_results,
        test_prices
    )

    print(result)

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
                "classification": "LOW_RISK",
                "confidence": 0.57,
                "score": -0.37
            }
        },

        "volume_agent": {
            "status": "success",
            "result": {
                "classification": "NEUTRAL",
                "confidence": 0.20,
                "score": 0.0
            }
        },

        "news_agent": {
            "status": "success",
            "result": {
                "classification": "NEUTRAL",
                "confidence": 0.24,
                "score": -0.04
            }
        }
    }

    result = personalize_user(
        "U001",
        "TCS",
        test_agent_results,
        current_prices
    )

    print(result)