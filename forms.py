from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PessoaForm(FlaskForm):


    nome = StringField('Nome', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired(), NumberRange(min=0, max=120)])
    submit = SubmitField('Cadastrar')
