from application import app, db
from application.models import *
from datetime import date, timedelta
from flask import request, redirect, url_for, render_template
from application.forms import *

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/view-reviews')  #
def view_all_reviews():
    reviews = Review.query.all()
    return render_template('view_all.html', entity='Review', reviews=reviews)

@app.route('/add-review', methods=['GET', 'POST'])
def create_new_review():
    form = ReviewForm()
    users = User.query.all()
    form.review_by.choices = [(user.uid, f"{user.first_name} {user.last_name}") for user in users]
    if form.validate_on_submit():
        b_name = form.book.data
        b_review = form.book_review.data
        review_date = form.review_date.data
        uid = form.review_by.data
        new_review = Review(book=b_name, book_review=b_review, review_date=review_date, review_by=uid)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('view_all_reviews'))
    form.review_date.data = date.today()
    errors = form.review_date.errors
    errors += form.book.errors
    return render_template('review_form.html', form = form, errors = errors)

@app.route('/update-review/<int:id>', methods=['GET', 'POST'])
def update_review(id):
    review_to_update = Review.query.get(id)
    form = ReviewForm()
    users = User.query.all()
    form.review_by.choices = [(user.uid, f"{user.first_name} {user.last_name}") for user in users]
    if form.validate_on_submit():
        review_to_update.book = form.book.data
        review_to_update.book_review = form.book_review.data
        review_to_update.review_date = form.review_date.data
        review_to_update.review_by = form.review_by.data
        db.session.commit()
        return redirect(url_for('view_all_reviews'))
    form.book.data = review_to_update.book
    form.book_review.data = review_to_update.book_review
    form.review_date.data = review_to_update.review_date
    return render_template('review_form.html', form=form)

@app.route('/delete-review/<int:id>')
def delete_review(id):
    review_to_delete = Review.query.get(id)
    db.session.delete(review_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_reviews'))

@app.route('/view-users')
def view_all_users():
    users = User.query.all()
    return render_template('view_all.html', entity='User', reviews=users)

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User(first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('view_all_users'))
    return render_template('user_form.html', form=form)

@app.route('/update-user/<int:id>', methods = ['GET', 'POST'])
def update_user(id):
    user_to_update = User.query.get(id)
    form = UserForm()
    if form.validate_on_submit():
        first_name, last_name = form.first_name.data, form.last_name.data
        user_to_update.first_name = first_name
        user_to_update.last_name = last_name
        db.session.commit()
        return redirect(url_for('view_all_users'))
    form.first_name.data = user_to_update.first_name
    form.last_name.data = user_to_update.last_name
    return render_template('user_form.html', form=form)

@app.route('/delete-user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get(id)
    for review in user_to_delete.reviews:
        db.session.delete(review)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_users'))