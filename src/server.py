import indexer

import os
from flask import Flask
app = Flask(__name__)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    
    abs_path = os.path.join('C:/', req_path)

    if not os.path.exists(abs_path):
        return f"NOT EXIST: {abs_path}"

    if os.path.isfile(abs_path):
        return f"FILE CONTENTS FOR: {abs_path}"

    return indexer.folder(abs_path)


if __name__ == '__main__':
    app.run()
