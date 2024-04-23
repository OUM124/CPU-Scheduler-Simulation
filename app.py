from flask import Flask

# Create a Flask app instance
app = Flask(__name__)

# Define a route and its associated function
@app.route('/')
def hello():
    return 'Hello, World!'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
