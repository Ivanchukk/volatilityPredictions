from flask import Flask
import os
print(os.getcwd())
from handlers.dataroutes import configure

app = Flask(__name__)

configure(app)


if __name__ == '__main__':
    app.run()


