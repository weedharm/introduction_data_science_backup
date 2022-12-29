from flask import Flask, render_template, request
from laptop_prices import LaptopPrices

model = LaptopPrices()


app = Flask(__name__)

RAM = [2, 4, 8, 16]

V_RAM = [0.0, 4.0, 8.0]

DISPLAY = [13.3, 14, 15.6]

RESOLUTION = [
    "1920x1080",
    "2560x1600"
]

SSD = [
    256, 512, 1024
]

HDD = [
    0, 512, 1024
]


@app.route("/")
def index():
    return render_template("index.html",
                           RAM=RAM, V_RAM=V_RAM, DISPLAY=DISPLAY, RESOLUTION=RESOLUTION, SSD=SSD, HDD=HDD)


@app.route("/predict", methods=["POST"])
def predict():
    name = request.form.get("name", "undefined")
    if name == "":
        name = "Brown Fox"

    app.logger.warning(request.form.get("ram"))
    ram = request.form.get("ram", "undefined")

    app.logger.warning(request.form.get("v_ram"))
    v_ram = request.form.get("v_ram", "undefined")

    app.logger.warning(request.form.get("display"))
    display = request.form.get("display", "undefined")

    app.logger.warning(request.form.get("resolution"))
    resolution = request.form.get("resolution", "undefined")

    app.logger.warning(request.form.get("ssd"))
    ssd = request.form.get("ssd", "undefined")

    app.logger.warning(request.form.get("hdd"))
    hdd = request.form.get("hdd", "undefined")

    price = model.predict(ram, v_ram, display, resolution, ssd, hdd)
    return render_template("predictions.html", name=name, ram=ram, v_ram=v_ram, display=display, resolution=resolution, ssd=ssd,
                           hdd=hdd, price=price)

