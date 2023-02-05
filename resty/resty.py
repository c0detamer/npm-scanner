from flask import Flask, request

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    if request.method=='POST':
        data=request.get_json()
        if 'packages' not in data.keys() or not isinstance(data['packages'], list):
            return "invalid payload\n"
        return f"Got a request to scan the following pacakges: {data['packages']}\n"
    

if __name__ == '__main__':
    app.run(port=5000)