# User profiles for the HackVerse project

users = {
    "U001": {
        "risk_level": "low",
        "investment_horizon": "long_term",
        "investment_amount": 50000
    },

    "U002": {
        "risk_level": "low",
        "investment_horizon": "medium_term",
        "investment_amount": 75000
    },

    "U003": {
        "risk_level": "low",
        "investment_horizon": "short_term",
        "investment_amount": 30000
    },

    "U004": {
        "risk_level": "high",
        "investment_horizon": "short_term",
        "investment_amount": 50000
    },

    "U005": {
        "risk_level": "high",
        "investment_horizon": "medium_term",
        "investment_amount": 100000
    },

    "U006": {
        "risk_level": "high",
        "investment_horizon": "long_term",
        "investment_amount": 150000
    }
}


def get_user_profile(user_id):
    return users.get(user_id)