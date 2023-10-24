import os
from app import create_app, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import User
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)
jwt = JWTManager(app)

from app import models

@jwt.user_lookup_loader
def load_current_user(_jwt_header, jwt_data):
    sub = jwt_data["sub"]
    return User.find_by_username(sub)

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)