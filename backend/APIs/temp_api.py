from flask import Blueprint, jsonify
from PseudoAgents import ResearcherAgent

temp_blueprint = Blueprint('temp', __name__)

@temp_blueprint.route('/temp', methods=['POST'])
def temp():
    researcher = ResearcherAgent(projectID=1234)
    # Set an idea title and generate a search query
    researcher.setIdeaTitle("Quantum Computing in Cryptography")
    researcher.generateSearchQuery()

    # Retrieve and print the generated search query
    search_query = researcher.getSearchQuery()
    print(f"Search Query: {search_query}")

    return jsonify({"message": "temp endpoint" +search_query})
