from flask import *
from nlp import Model
m = Model()
app = Flask(__name__)
data = list()

@app.route('/')
def home():
    return "hello"


@app.route('/result',methods=["POST"])
def result():
    if request.method=="POST":
        res = request.get_json()
        blogs = res["blogs"]
        result = m.predict(blogs)
        d = dict()
        d["result"] = result
        return jsonify(d)
    else:
        return "Bad request",400

def run(port):
    if __name__ =="__main__":
        app.run(debug = False, port=port)

run(5000)