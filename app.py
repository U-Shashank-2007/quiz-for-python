from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ------------------ QUIZ DATA (same as your Pygame backend) ------------------ #
questions = [
    {
        "id": 0,
        "q": "Who invented Python?",
        "options": ["Dennis Ritchie", "Guido van Rossum", "Bjarne Stroustrup", "Linus Torvalds"],
        "answer": 1  # index of correct option
    },
    {
        "id": 1,
        "q": "Which keyword is used to define a function in Python?",
        "options": ["func", "function", "def", "lambda"],
        "answer": 2
    },
    {
        "id": 2,
        "q": "What is the output of: len([1,2,3])?",
        "options": ["2", "3", "4", "None"],
        "answer": 1
    }
]


@app.route("/")
def home():
    # Serve the frontend page
    return render_template("index.html")


@app.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Return the list of questions WITHOUT answers
    so students don’t see the correct options in the JSON.
    """
    public_questions = []
    for q in questions:
        public_questions.append({
            "id": q["id"],
            "q": q["q"],
            "options": q["options"]
        })
    return jsonify(public_questions)


@app.route("/api/submit", methods=["POST"])
def submit_answers():
    """
    Receive student's answers and calculate score.
    Expected JSON:
    {
        "answers": [selectedIndexForQ0, selectedIndexForQ1, ...]
    }
    """
    data = request.get_json()
    user_answers = data.get("answers", [])

    score = 0
    for i, q in enumerate(questions):
        if i < len(user_answers) and user_answers[i] == q["answer"]:
            score += 1

    result = {
        "score": score,
        "total": len(questions)
    }
    return jsonify(result)


if __name__ == "__main__":
    # Debug mode on for development
    app.run(debug=True)
