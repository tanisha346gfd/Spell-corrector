from flask import Flask, request, render_template
from src.spell_corrector import SpellCorrector

app = Flask(__name__)
corrector = SpellCorrector("data/big.txt")

@app.route("/", methods=["GET", "POST"])
def home():
    corrected = None
    if request.method == "POST":
        word = request.form["word"]
        corrected = corrector.correction(word)
    return render_template("index.html", corrected=corrected)

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)

