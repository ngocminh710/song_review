from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,TextAreaField,validators,PasswordField
from wtforms.validators import DataRequired, Length, ValidationError,Email,EqualTo
from password_validator import PasswordValidator
from app.Model.models import User


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class MusicsearchForm(FlaskForm):
    field = SelectField('',choices = [('songname', 'Song'), ('artist', 'Artist'), ('album','Album')])
    matching = StringField('')
    submit = SubmitField('Search')

class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])

    confirmpassword = PasswordField('Confirm Password', [
        DataRequired(message='Your confirmpassword is required'),
        PasswordValid(),
        EqualTo('password')])

    FirstName = StringField('First Name', [
        DataRequired(message='Your First Name is required'),
        Length(min=1, message='Your First Name is too short')])

    LastName = StringField('Last Name', [
        DataRequired(message='Your Last Name is required'),
        Length(min=1, message='Your Last Name is too short')])
    
    email = StringField(label='E-mail', validators=[DataRequired(), Email()],
                        render_kw={ "class": "form-control"})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')

class ChangeUserForm(FlaskForm):
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    confirmpassword = PasswordField('Confirm Password', [
        DataRequired(message='Your confirmpassword is required'),
        PasswordValid(),
        EqualTo('password')])
    email = StringField(label='E-mail', validators=[DataRequired(), Email()],
                        render_kw={ "class": "form-control"})
    submit = SubmitField('UPDATE')

class CommentForm(FlaskForm):
    comment = StringField('Comments:', [
        DataRequired(),validators.Length(min=1, max=500,message="Word count mismatch")])
    rating = SelectField('Your Rating',choices = [(5, 'Five Stars'), (4, 'Four Stars'), (3, 'Three Stars'), 
    (2, 'Two Stars'), (1,'One Star'), (0,'Zreo')])
    submit = SubmitField('Submit')