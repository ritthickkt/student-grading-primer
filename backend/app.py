from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
    mark = student_data.get("mark", 0)
    new_student = db.insert_student(student_data["name"], student_data["course"], mark)
    return jsonify(new_student), 200

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    updated_student = db.update_student(student_id, student_data["name"], student_data["course"], student_data["mark"])
    if updated_student is None:
      return jsonify(updated_student), 404
    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted_student = db.delete_student(student_id)
    if deleted_student is None:
      return jsonify(deleted_student), 404
    return jsonify(deleted_student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    if len(students) == 0:
      return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200
    count = 0
    min = students[0]["mark"]
    max = students[0]["mark"]
    total_mark = 0
    for student in students:
        total_mark = total_mark + student["mark"]
        count = count + 1
        if student["mark"] < min:
            min = student["mark"]
        if student["mark"] > max:
            max = student["mark"]
    avg = total_mark/count
    return jsonify({"count": count, "average": avg, "min": min, "max": max}), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
