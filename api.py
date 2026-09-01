from flask import Flask, jsonify, request
from flask_cors import CORS

from orchestration.parallel_runner import run_all_agents
from orchestration.synthesis_agent import synthesize
from p3.personalization import personalize_user
from rag.retriever import retrieve_documents

app = Flask(__name__)
CORS(app)


@app.route("/analyze")
def analyze():

    ticker = request.args.get("ticker", "TCS")
    user_id = request.args.get("user_id", "U001")

    # P1 - market agents
    agents = run_all_agents(ticker)

    # RAG
    documents = retrieve_documents(
        f"{ticker} financial performance investment risk",
        top_k=3
    )

    # P2 - synthesis
    synthesis = synthesize(
        agents,
        documents
    )

    # Sample prices for portfolio calculation
    prices = {
        "TCS": 2369,
        "INFY": 1500,
        "RELIANCE": 2500
    }

    # P3 - personalization
    personalization = personalize_user(
        user_id,
        ticker,
        agents,
        prices,
        synthesis
    )

    return jsonify({
        "ticker": ticker,
        "agents": agents,
        "synthesis": synthesis,
        "personalization": personalization
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )