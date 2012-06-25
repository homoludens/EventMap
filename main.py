from hello import app, db
from flask import json

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    #app.run(host='0.0.0.0')