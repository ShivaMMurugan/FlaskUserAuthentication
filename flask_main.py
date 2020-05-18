from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b87e6e3fd893f525f32af96dd8e284808aeb0aa24e5043d6f20a62d81c4503bb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'
mongo = PyMongo(app)


class FlaskAuth(FlaskForm):

	username = StringField('username')
	password = StringField('password')



@app.route('/register_page', methods=['GET', 'POST'])
def register_page():

	form = FlaskAuth()

	if request.method == 'POST':

		usr_nme = request.form.get('username')
		pwd = request.form.get('password')

		user_details = mongo.db.logindetails.insert({'username': usr_nme, 'password': pwd})

		if usr_nme and pwd:
			
			return redirect(url_for('success_page'))
			


	return render_template('register_page.html', form=form)


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():

	form = FlaskAuth()

	if request.method == 'POST':

		existing_username = request.form.get('username')
		existing_userpassword = request.form.get('password')

		
		db_users = mongo.db.logindetails.find()

		for data in db_users:

			if existing_username == data['username'] and existing_userpassword == data['password']:

				return redirect(url_for('success_page'))

		return redirect(url_for('register_page'))

	return render_template('login_page.html', form=form)



@app.route('/success_page')
def success_page():

	return render_template('success_page.html')


if __name__ == '__main__':

	app.run(debug=True)
