from flask import Flask,render_template
from flask_wtf import Form
from flask_bootstrap import Bootstrap 
from wtforms import StringField,SubmitField 
from wtforms.validators import Required

from tools import search

DB_PATH = 'db'

class IRForm(Form): 
	name = StringField('Please enter: ',validators=[Required()]) 
	submit = SubmitField('Submit') 

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'key' 
bootstrap = Bootstrap(app) 

@app.route('/',methods=['GET','POST']) 
def index(): 
	name = None 
	nameForm = IRForm()
	ret = ''

	if nameForm.validate_on_submit():
		name = nameForm.name.data
		nameForm.name.data = ''
		tmp = 'Retrive results: \n'+search(DB_PATH, name)
		ret = tmp.replace('\n','$')
	
	return render_template('index.html',form=nameForm,name=ret) 

if __name__ == '__main__': 
	app.run(debug=True)
