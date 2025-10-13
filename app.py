from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Seema,, I love you My Love, I miss you so much, Please come back to me soon, I can't live without you."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
