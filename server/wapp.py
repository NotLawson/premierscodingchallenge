## WEB APP ##
from flask import Flask

if __name__=="__main__":
    app = Flask(__name__)
else:
    from __main__ import app 


@app.route("/")
def index():
    return "Hello world"

if __name__ == "__main__":
    app.run(port=5001, debug=True)
