from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    cwd = os.getcwd()
    print("Current directory:", cwd)

    with open("C:\BrightCom\GitHub\mstjernfelt\m3u_to_strm\.local\Monsteriptv\logfile.log", "r") as f:
        contents = f.read()

    return render_template("index.html", contents=contents)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
