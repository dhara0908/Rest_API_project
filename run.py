from app import create_app

# Instantiate the Flask application via the factory function
app = create_app()

if __name__ == '__main__':
    # Running the application locally in debug mode for development.
    # Debug mode provides interactive error messages and auto-reloads on file changes.
    app.run(host='127.0.0.1', port=5000, debug=True)