#!/usr/bin/env python3

from flask import *
import requests
import traceback
import secret
import data_processing


app = Flask(__name__, static_url_path="")
app.secret_key = secret.SECRET_KEY


@app.template_filter()
def format_money(m):
    return "${:,.2f}".format(m)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def data():
    try:
        lat = float(request.args.get("latitude"))
        lng = float(request.args.get("longitude"))
        r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params = {
            "latlng": "{},{}".format(lat, lng),
            "key": secret.GMAPS_API_KEY,
        }).json()
        if r["results"]:
            place = r["results"][0]
        else:
            place = {"formatted_address": None, "place_id": None}

        context = {
            "gmaps_api_key": secret.GMAPS_API_KEY,
            "weekly_avg_income": data_processing.get_weekly_avg_income(lat, lng),
            "max_bookings_price": data_processing.get_max_bookings_price(lat, lng),
            "formatted_address": place["formatted_address"],
            "place_id": place["place_id"],
        }
        return render_template("data.html", **context)
    except:
        traceback.print_exc()
        flash("Oh no, something went wrong!")
        return redirect("/")


if __name__ == "__main__":
    import sys
    app.run(host="0.0.0.0", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, threaded=True)
