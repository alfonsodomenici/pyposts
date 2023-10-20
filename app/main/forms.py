from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    usr = StringField('usr',validators=[DataRequired()])
    pwd=PasswordField('pwd',validators=[DataRequired()])
    submit=SubmitField('Login')
