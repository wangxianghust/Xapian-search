from flask import Flask,render_template,request
from flask_wtf import Form
from flask_bootstrap import Bootstrap 
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,InputRequired

from tools import search

DB_PATH = 'db'

class IRForm(Form): 
	statement = StringField('Please enter the statement you want to check: ',validators=[DataRequired()])
	scheme = SelectField('Please choose the weighting scheme you want to use: ', choices=[
		(0, 'BB2Weight'),
		(1, 'BM25PlusWeight'),
		(2, 'BM25Weight'),
		(3, 'BoolWeight'),
		(4, 'CoordWeight'),
		(5, 'DLHWeight'),
		(6, 'DPHWeight'),
		(7, 'IfB2Weight'),
		(8, 'IneB2Weight'),
		(9, 'InL2Weight'),
		(10, 'LMWeight'),
		(11, 'PL2PlusWeight'),
		(12, 'PL2Weight'),
		(13, 'TfIdfWeight'),
		(14, 'TradWeight')], validators=[InputRequired()], default=2, coerce=int)
	submit = SubmitField('Submit')

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'key' 
bootstrap = Bootstrap(app) 

@app.route('/',methods=['GET','POST']) 
def index(): 
	statement = None
	weightOption = 2
	InformationForm = IRForm(request.form)
	ret = []

	if request.method == 'POST':
		if InformationForm.validate_on_submit():
			statement = InformationForm.statement.data
			weightOption = InformationForm.scheme.data
			InformationForm.statement.data = ''
			tmp = 'Retrive results: \n'+search(DB_PATH, statement, weightOption)
			ret = tmp.split("\n")

	return render_template('index.html',form=InformationForm,statement=ret) 

if __name__ == '__main__': 
	app.run(debug=True)
