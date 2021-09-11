from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,MultipleFileField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileAllowed,FileRequired


class LoginForm(FlaskForm):
    user = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    submit = SubmitField("Login")
    
    
class AddPersonForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    image = MultipleFileField("Image",render_kw={'multiple': True})
    submit = SubmitField("Add Person")