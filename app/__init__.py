from flask import Flask

def create_app():
    """
    Application Factory pattern to initialize and configure the Flask app.
    """
    app = Flask(__name__)
    
    # Configure application settings
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    # Using app context to cleanly import and link modules
    with app.app_context():
        from app import routes
        # Register the blueprint we defined in routes.py
        app.register_blueprint(routes.bp)
        
    return app