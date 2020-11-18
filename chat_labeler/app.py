from flask import Flask, render_template, request, redirect
import sys
import json

sys.path.append("..")
from chat_file import ChannelFile
hopped_messages = ChannelFile("../hopped_messages.json", custom_json=True)

labeled_path = "../hand_labeled.json"
labeled_file = ChannelFile(labeled_path, custom_json=True)

last_labeled = None
while True:
    next_message = labeled_file.next()
    if not next_message:
        break
    last_labeled = next_message

while True:
    next_message = hopped_messages.next()
    if not next_message:
        break
    if next_message.timestamp >= last_labeled.timestamp:
        break

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
