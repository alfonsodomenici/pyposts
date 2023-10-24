import os
from app import create_app, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models.user import User
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)


from app import models

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)