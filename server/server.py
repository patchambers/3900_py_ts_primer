from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


# Add a student to students.json
# Returns the id of the added student
def add_student(name):
    with open("students.json", "r") as file:
        students = json.load(file)
    students.append(name)
    count = len(students)
    with open("students.json", "w") as file:
        json.dump(students, file)
    return count

# Add a group to groups.json
# Returns the group details, or None if the given group name already exists
def add_group(group_name, student_names):
    with open("groups.json", "r") as file:
        group_json = json.load(file)

    # If group name already exists, return None
    for g in group_json["groups"]:
        if g["groupName"] == group_name:
            return None
    
    group_json["counter"] = int(group_json["counter"]) + 1

    group = {
        "id": group_json["counter"],
        "groupName": group_name,
        "members": [],
    }

    for student_name in student_names:
        group["members"].append(add_student(student_name))
    group_json["groups"].append(group)

    with open("groups.json", "w") as file:
        json.dump(group_json, file)

    return group


@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    with open("groups.json", "r") as file:
        group_json = json.load(file)
    groups = group_json["groups"]
    return jsonify([_ for _ in groups])


@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    
    with open("students.json", "r") as file:
        students = json.load(file)
    return jsonify([{"id": i + 1, "name": students[i]} for i in range(len(students))])


@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """
    
    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")
    
    new_group = add_group(group_name, group_members)
    
    if new_group:
        return jsonify(new_group), 201
    
    # If user enters a group name that already exists, no group created and 400 
    # code returned
    return '', 400



@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    # TODO: (delete the group with the specified id)

    with open("groups.json", "r") as file:
        group_json = json.load(file)

    for group in group_json["groups"]:
        if group["id"] == group_id:
            group_json["groups"].remove(group)

    with open("groups.json", "w") as file:
        json.dump(group_json, file)

    return '', 204  # Return 204 (do not modify this line)


@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """

    with open("groups.json", "r") as file:
        groups = json.load(file)["groups"]

    with open("students.json", "r") as file:
        students = json.load(file)

    for group in groups:
        if group["id"] == group_id:
            return jsonify({
                "id": group_id, 
                "groupName": group["groupName"], 
                "members": [{"id": i, "name": students[i - 1]} for i in group["members"]]
            })

    abort(404, "Group not found")


if __name__ == '__main__':
    
    with open("students.json", "w") as file:
        json.dump([], file)
    with open("groups.json", "w") as file:
        json.dump({"counter": 0, "groups": []}, file)
    app.run(port=3902, debug=True)
