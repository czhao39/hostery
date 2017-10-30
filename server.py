#!/usr/bin/env python3

from flask import *
import secret
import data_processing
import traceback


app = Flask(__name__, static_url_path="")
app.secret_key = secret.SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    try:
        lat = float(request.args.get("latitude"))
        lng = float(request.args.get("longitude"))
        context = {
            "weekly_avg_income": data_processing.get_weekly_avg_income(lat, lng),
            "max_bookings_price": data_processing.get_max_bookings_price(lat, lng),
        }
        return render_template("data.html", **context)
    except:
        traceback.print_exc()
        flash("Oh no, something went wrong!")
        return redirect("/")


if __name__ == "__main__":
    import sys
    app.run(host="0.0.0.0", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, threaded=True)
