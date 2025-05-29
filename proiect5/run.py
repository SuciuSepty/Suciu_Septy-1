from flask import Flask
from app.routes.items import items_bp

app = Flask(__name__)
app.register_blueprint(items_bp)

if __name__ == '__main__':
    app.run(debug=True)
