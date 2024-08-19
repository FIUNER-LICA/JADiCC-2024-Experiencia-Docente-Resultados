from flask_wtf import FlaskForm # pip install flask-wtf
from wtforms import StringField, PasswordField, FileField, SelectField, SubmitField # https://wtforms.readthedocs.io/en/2.3.x/
from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf.file import FileAllowed, FileRequired, FileSize

class RegisterForm(FlaskForm):
    nombre = StringField(label='Nombre', validators=[DataRequired()])
    apellido = StringField(label='Apellido', validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=5), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField(label='Repeat Password', validators=[DataRequired()])
    submit = SubmitField(label='Register')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField(label='Log In')


class ReclamoForm(FlaskForm):
    asunto = StringField(label='Asunto', validators=[DataRequired()])
    imagen = FileField('File', validators=[
        FileAllowed(['jpg', 'jpeg' , 'png', 'bmp', 'gif'], 'Solo se permiten archivos de tipo jpg, png, bmp y gif'),
        FileSize(max_size=5 * 1024 * 1024, message='El archivo no debe superar los 5MB de tamaño.')
    ])
    contenido = StringField(label='Contenido', validators=[DataRequired()], render_kw={'width': '200', 'height': '100'})
    submit = SubmitField(label='Crear')
