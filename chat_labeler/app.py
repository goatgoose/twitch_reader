from flask import Flask, render_template, request, redirect
import sys
import json

sys.path.append("../twitch_reader")
from chat_file import ChannelFile
hopped_messages = ChannelFile("../twitch_reader/hopped_messages.json", custom_json=True)
labeled_path = "../twitch_reader/hand_labeled.json"

for _ in range(5000):
    hopped_messages.next()

app = Flask(__name__)

messages = {}  # id : message


@app.route("/")
def index():
    next_message = hopped_messages.next()
    messages[next_message.id] = next_message
    return redirect(f"/label/{next_message.id}")


@app.route("/label/<id_>")
def label(id_):
    message = messages[id_]
    return render_template("index.html", message=message.content, id=message.id)


@app.route("/submit_label/<id_>", methods=["POST"])
def submit_label(id_):
    message = messages[id_]
    message.toxicity = request.form["label"]
    with open(labeled_path, "a+") as labeled_file:
        labeled_file.write(message.to_custom_json() + "\n")
    del messages[id_]
    return redirect("/")
