import os
from app import create_app, db
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade
from app.models.role import Role

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app,db)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    upgrade()
    default_rules = ['ADMIN','USER']
    for r in default_rules:
        if Role.query.filter_by(name=r).first() is None:
            db.session.add(Role(name=r))
    db.session.commit()

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

from app.models import role, user, post