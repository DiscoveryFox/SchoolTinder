import flask
from flask import request, jsonify
from flask_login import current_user

app = flask.Flask(__name__)

@app.route("/")
def index():
    return flask.render_template("index.html", name="Flinn")

@app.route("/match", methods=["GET"])
def get_next_match():
    match = {
        "pictures": [
            "url1",
            "url2",
            "url3",
        ],
        "name": "Marc",
        "link_to_profile": "url_to_profile",
        # TODO: Alle Daten die angezeigt werden sollen.
    }
    return jsonify(match)

@app.route("/match", methods=["POST"])
def update_match():
    data = request.get_json()
    
    # profile_id: str = current_user.profileId TODO: Implement user login and management
    profile_id: str = "dajkdanwhjkdnijd2i3j1jkn"
    otherProfileId: str = str(data.get("otherProfileId"))
    result: str = str(data.get("result"))
    
    
    if result not in ["success", "denial"]:
        return jsonify({"error": "Invalid result"}), 400

    print(f"Match {profile_id}(You) matched with -> {otherProfileId}(From your profile) updated as {result}")
    
    return jsonify({"message": f"Match {profile_id}-{otherProfileId} updated successfully", "result": result})

if __name__ == "__main__":
    app.run(debug=True)
