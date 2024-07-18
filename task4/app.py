from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from recommendation import get_user_recommendations, update_user_ratings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'super_secret_key'
db = SQLAlchemy(app)

movies_df = pd.read_csv('./movie-dataset/movies.csv')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('search'))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'user_id' not in session:
        flash("You need to login first.")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
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
    if 'user_id' not in session:
        flash("You need to login first.")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    user_ratings = Rating.query.filter_by(user_id=user_id).all()
    
    movies_df = pd.read_csv('./movie-dataset/movies.csv')  

    if request.method == 'POST':
        query = request.form['query']
        movies = movies_df[movies_df['title'].str.contains(query, case=False, regex=False)]
        return render_template('search.html', movies=movies.to_dict('records'),user_ratings=user_ratings,movies_df=movies_df)
    return render_template('search.html', movies=[],user_ratings=user_ratings,movies_df=movies_df)


@app.route('/rate', methods=['POST'])
def rate_movie():
    if 'user_id' not in session:
        flash("You need to login first.")
        return redirect(url_for('login'))

    user_id = session['user_id']
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
    if 'user_id' not in session:
        flash("You need to login first.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    
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
