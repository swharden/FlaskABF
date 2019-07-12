import flask
from flask import request

app = flask.Flask(__name__)

@app.route('/testPost', methods=['POST', 'GET'])
def testPost():
    html = ""
    
    if request.method == 'POST':
        html += "<div>POST</div>"
        html += f"<div>abfID: {request.form['abfID']}</div>"
        html += f"<div>comment: {request.form['comment']}</div>"
        html += f"<div>colorCode: {request.form['colorCode']}</div>"
    else:
        html += "<div>GET</div>"

    html += """
    <hr>
    <form action="/testPost" method="post">
        ABFID: <input type="text" name="abfID" value="123456"><br>
        comment: <input type="text" name="comment" value="awesome stuff"><br>
        color: <input type="text" name="colorCode" value="g1"><br>
        <input type="submit" value="Submit">
    </form>
    """
    return html


if __name__ == '__main__':
    app.run(host="192.168.1.225", port="8080")
