from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import random
import string

app = Flask(__name__)
CORS(app)

projects = [
    {
        "id": "PROJ001",
        "dateCreated": "2024-12-18 13:31:10",
        "ideaDescription": "Redesign the mobile app UI/UX for better user engagement.",
        "ideaTitle": "Mobile app redesign abcdefadgasoi"
    },
    {
        "id": "PROJ002",
        "dateCreated": "2024-12-18 09:31:10",
        "ideaDescription": "Integrate blockchain technology for secure transactions.",
        "ideaTitle": "Blockchain integration"
    },
    {
        "id": "PROJ003",
        "dateCreated": "2024-12-18 13:31:10",
        "ideaDescription": "Create a system for managing IoT devices in smart homes.",
        "ideaTitle": "IoT device management"
    },
    {
        "id": "PROJ004",
        "dateCreated": "2024-12-17 10:15:30",
        "ideaDescription": "Develop an AI-powered recommendation engine for e-commerce.",
        "ideaTitle": "AI recommendation engine"
    },
    {
        "id": "PROJ005",
        "dateCreated": "2024-12-16 16:45:20",
        "ideaDescription": "Create a virtual reality training platform for industrial workers.",
        "ideaTitle": "VR training platform"
    },
    {
        "id": "PROJ006",
        "dateCreated": "2024-12-15 11:20:45",
        "ideaDescription": "Build a decentralized file storage system using blockchain.",
        "ideaTitle": "Decentralized storage"
    }]

# Simulated project stages
PROJECT_STAGES = {
    "PROJ001": "selectSources",
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

@app.route('/getUserProjects', methods=['POST'])
def get_user_projects():
    try:
        return jsonify({
            "success": True,
            "allUserProjects": projects
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An error occurred"
        }), 500

@app.route('/deleteProject', methods=['DELETE'])
def delete_project():
    project_id = request.json.get('id')
    if not project_id:
        return jsonify({
            "success": False,
            "error": "Project ID is required"
        }), 400
    
    print(f"Deleting project with ID: {project_id}")
    
    global projects
    projects = [p for p in projects if p['id'] != project_id]
    
    return jsonify({
        "success": True,
        "message": f"Project {project_id} deleted successfully"
    })

@app.route('/createProject', methods=['POST'])
def create_project():
    idea_title = request.json.get('ideaTitle')
    idea_description = request.json.get('ideaDescription')

    if not idea_title or not idea_description:
        return jsonify({
            "success": False,
            "error": "Idea title and description are required"
        }), 400

    print(f"Creating new project: {idea_title}")
    print(f"Description: {idea_description}")

    new_project = {
        "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
        "dateCreated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ideaTitle": idea_title,
        "ideaDescription": idea_description
    }

    projects.append(new_project)

    return jsonify({
        "success": True,
        "message": "Project created successfully",
        "project": new_project
    })
    
@app.route('/getProjectDetails', methods=['POST'])
def get_project_details():
    try:
        project_id = request.json.get('id')
        if not project_id:
            return jsonify({
                "success": False,
                "error": "Project ID is required"
            }), 400

        project = next((p for p in projects if p['id'] == project_id), None)
        if not project:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404

        return jsonify({
            "success": True,
            "project": project
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/last-completed-stage/<project_id>', methods=['GET'])
def get_last_completed_stage(project_id):
    print("project_stages1", project_stages)
    last_completed_stage = project_stages.get(project_id, -1)
    return jsonify({'lastCompletedStage': last_completed_stage})

@app.route('/api/complete-stage/<project_id>/<int:stage>', methods=['POST'])
def complete_stage(project_id, stage):
    print("project_stages2", project_stages)
    project_stages[project_id] = stage
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)

print("Flask server is running. Try making requests to the API endpoints.")
