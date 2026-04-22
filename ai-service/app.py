from flask import Flask, request, jsonify
from sanitize import sanitize_input

app = Flask(__name__)

@app.before_request
def before():
    result = sanitize_input()
    if result:
        return result

@app.route("/test", methods=["POST"])
def test():
    return jsonify({
        "message": "Input accepted",
        "data": request.get_json()
    })

if __name__ == "__main__":
    app.run(debug=True)