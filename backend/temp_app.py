from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated project stages
PROJECT_STAGES = {
    "P123": "selectSources",
    "P124": "script",
    "P125": "videoTitle",
    # Add more projects and their stages as needed
}

@app.route('/api/getNextStage/<project_id>', methods=['GET'])
def get_next_stage(project_id):
    next_stage = PROJECT_STAGES.get(project_id, None)
    if next_stage:
        return jsonify({"next_stage": next_stage}), 200
    return jsonify({"error": "Project not found"}), 404

@app.route('/api/checkProject/<project_id>', methods=['GET'])
def check_project(project_id):
    # Check if the project ID exists in the database
    if project_id in PROJECT_STAGES:
        return jsonify({"exists": True, "project_id": project_id}), 200
    return jsonify({"exists": False, "error": "Project not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
