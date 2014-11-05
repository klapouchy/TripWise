from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import jinja2
import os
import model
import map_data

app = Flask(__name__)
app.secret_key = 'kbegw*^6^Fhjkh'

@app.route("/")
def index():
    """This is the 'cover' page of the site"""
    return render_template("index.html")

@app.route("/javascript")
def js_index():
    return render_template("test_js_directions.html")

@app.route("/directions")
def list_directions():
    """Prints out directions from user input"""
    origin = request.args.get("origin")
    destination = request.args.get("destination")

    route = model.Route(origin, destination)
    route.get_directions()


    # Checks that valid results were returned from Google Directions API
    if route.directions['status'] == 'OK':
        direction_steps = []
        for step in route.directions['routes'][0]['legs'][0]['steps']:
            direction_steps.append(step['html_instructions'])
        
        return render_template("test.html", direction_steps=direction_steps, distance=route.distance, duration=route.duration, polyline=route.polyline)

    else:
        direction_steps = ["It didn't work"]
        return render_template("test.html", direction_steps=direction_steps)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
