from flask import Flask, render_template, request, redirect, url_for, session, flash, logging
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from recommendation import get_user_recommendations, update_user_ratings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dhruv1;s2secret#key$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

movies_df = pd.read_csv('./movie-dataset/movies.csv')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False, unique=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate:
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            name=form.name.data,
            email=form.email.data,
            password=hashed_password )
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    else: # method is GET
        return render_template('register.html',form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash('You have successfully logged in.',"success")
            session['logged_in'] = True
            session['use_id'] = user.id
            session['username'] = user.username
            return redirect(url_for("search"))
        else:
            flash("Invalid credentials. Please try again.","Danger")
            return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route('/logout/')
def logout():
    session['logged_in'] = False
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'user_id' not in session:
        flash("You need to login first.")
        return redirect(url_for('login'))
    
    user_id = session['use_id']
    
    user = User.query.get(user_id)
    if user:
        Rating.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        
        delete_user(user_id)
        
        session.pop('user_id', None)
        flash('User deleted successfully.', 'success')
        return redirect(url_for('index'))
    else:
        flash('User not found.', 'error')
        return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if session['logged_in']==False:
        flash("You need to login first.")
        return redirect(url_for('login'))
    
    u_id = session['use_id']
    user_ratings = Rating.query.filter_by(user_id=u_id).all()
    
    movies_df = pd.read_csv('./movie-dataset/movies.csv')  

    if request.method == 'POST':
        query = request.form['query']
        movies = movies_df[movies_df['title'].str.contains(query, case=False, regex=False)]
        return render_template('search.html', movies=movies.to_dict('records'),user_ratings=user_ratings,movies_df=movies_df)
    return render_template('search.html', movies=[],user_ratings=user_ratings,movies_df=movies_df)


@app.route('/rate', methods=['POST'])
def rate_movie():
    if session['logged_in']==False:
        flash("You need to login first.")
        return redirect(url_for('login'))

    user_id = session['use_id']
    movie_id = int(request.form['movie_id'])
    rating_value = float(request.form['rating'])
    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    
    if rating:
        rating.rating = rating_value
    else:
        new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating_value)
        db.session.add(new_rating)
    
    db.session.commit()
    
    movie_ratings = {rating.movie_id: rating.rating for rating in Rating.query.filter_by(user_id=user_id).all()}
    update_user_ratings(user_id, movie_ratings)
    
    return redirect(url_for('search'))


@app.route('/recommendations')
def recommendations():
    if session['logged_in']==False:
        flash("You need to login first.")
        return redirect(url_for('login'))

    user_id = session['use_id']
    
    user_ratings = {rating.movie_id: rating.rating for rating in Rating.query.filter_by(user_id=user_id).all()}
    # print(user_ratings)
    update_user_ratings(user_id, user_ratings)
    
    recommendations = get_user_recommendations(user_id)
    
    if recommendations is None:
        recommended_movies = []
    else:
        recommended_movies = [
            {'id': movie_id, 'title': movies_df[movies_df['movieId'] == movie_id]['title'].values[0]}
            for movie_id in recommendations.index
        ]
    
    return render_template('recommendations.html', recommendations=recommended_movies)

# to run initially: set Flask_APPP=app.py
# to run initially(macOS or Linux): export Flask_APPP=app.py

# after that , use : flask run