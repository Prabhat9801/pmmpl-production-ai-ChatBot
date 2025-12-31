# 🤖 PMMPL Production Management AI ChatBot

Enterprise-grade AI agent for production management. Query 16 Google Sheets using natural language with LangGraph. 82% accuracy on 56+ query types.

## Features
- 7 operation types: Retrieve, Aggregate, Compare, Rank, Trend, Predict, Feasibility
- Real-time Google Sheets integration
- Smart query routing with LangGraph
- Date intelligence ("last 30 days", "this month")
- Self-healing with retry mechanism

## Quick Start
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API keys and Google credentials to `.env` (do not commit secrets)
4. Run the notebook: `jupyter notebook Untitled50.ipynb`

## Security
- All secrets and credentials must be kept in `.env` and are ignored by git
- Never commit `.env` or `*.json` credential files

## License
MIT
