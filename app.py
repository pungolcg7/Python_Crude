from flask import Flask
from routes import init_routes  # Import the init_routes function from routes

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize routes
init_routes(app)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
