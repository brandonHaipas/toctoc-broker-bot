from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return render_template("base.html")

@app.route('/message/<message>', methods=["POST"])
def receive_message(message):
    print(message)

if __name__ == '__main__':
    app.run()
