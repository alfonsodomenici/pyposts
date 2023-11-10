import os
from app import create_app, db
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app,db)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

from app.models import role, user, post