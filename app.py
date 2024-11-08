from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/genai/goods/prevention",methods=['POST'])
def test_send_post():
    json_string = request.get_json()
    if json_string == None:
        return 'false', 500
    try:
        json.loads(json_string)
        return 'true', 200
    except:
        return 'false', 500

if __name__ == '__main__':
    app.run()