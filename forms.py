from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length

class LoginForm(FlaskForm):
    user = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")