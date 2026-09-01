# Sample portfolios for the 6 HackVerse users

portfolios = {
    "U001": {
        "TCS": 5,
        "INFY": 5
    },

    "U002": {
        "RELIANCE": 4,
        "INFY": 8
    },

    "U003": {
        "TCS": 3,
        "RELIANCE": 3
    },

    "U004": {
        "TCS": 10,
        "RELIANCE": 8
    },

    "U005": {
        "INFY": 15,
        "TCS": 8
    },

    "U006": {
        "TCS": 15,
        "RELIANCE": 10
    }
}


def get_user_portfolio(user_id):
    return portfolios.get(user_id)


def calculate_portfolio_allocation(user_id, current_prices):

    portfolio = get_user_portfolio(user_id)

    if portfolio is None:
        return None

    stock_values = {}

    for stock, quantity in portfolio.items():

        if stock in current_prices:
            stock_values[stock] = quantity * current_prices[stock]

    total_value = sum(stock_values.values())

    if total_value == 0:
        return {}

    allocation = {}

    for stock, value in stock_values.items():

        allocation[stock] = round(
            (value / total_value) * 100,
            2
        )

    return allocation


# Testing with sample current prices
if __name__ == "__main__":

    current_prices = {
        "TCS": 3500,
        "INFY": 1500,
        "RELIANCE": 2500
    }

    result = calculate_portfolio_allocation(
        "U001",
        current_prices
    )

    print("U001 Portfolio Allocation:")
    print(result)