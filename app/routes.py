from flaskproject.forms import (RegistrationForm, LoginForm, CommentForm,
                                UpdateAccountForm, PostForm, ResetPasswordForm, RequestResetForm)
from flask import render_template, url_for, redirect, flash, request, abort
from flask_login import login_required, current_user, login_user, logout_user
from flaskproject.models import User, Post, Comment
from flaskproject import app, db, bcrypt, mail
from flask_mail import Message
from datetime import datetime
import secrets
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', _category='')


@app.route('/about')
def about():
    return render_template('about.html', title='About', _category='')


@app.route('/anime')
def anime():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='anime').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Anime', posts=posts, _category='anime')


@ app.route('/animals')
def animals():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='animals').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Animals', posts=posts, _category='animals')


@ app.route('/technology')
def technology():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='technology').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Technology', posts=posts, _category='technology')


@ app.route('/sns')
def sns():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='sns').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='SeriesNShows', posts=posts, _category='sns')


@ app.route('/movies')
def movies():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='movies').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Movies', posts=posts, _category='movies')


@ app.route('/programming')
def programming():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='programming').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Programming', posts=posts, _category='programming')


@ app.route('/funny')
def funny():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='funny').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Funny', posts=posts, _category='funny')


@ app.route('/gaming')
def gaming():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='gaming').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='Gaming', posts=posts, _category='gaming')


@app.route('/nsfw')
def nsfw():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='nsfw').order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('posts_page.html', title='NSFW', posts=posts, _category='nsfw')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user1 = User.query.filter_by(username=form.email.data).first()
        if user1:
            user = user1
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Log In unsuccessful. Check you email/username and password', 'danger')
    return render_template('login.html', title='Login', form=form, _category='')


@ app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you can login now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, _category='')


def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    new_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', new_fn)
    form_pic.save(pic_path)
    return new_fn


@ app.route('/account', methods=['POST', 'GET'])
@ login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            current_user.image = pic_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', image=image, form=form, _category='')


@app.route('/chatrooms', methods=['GET', 'POST'])
def chatrooms():
    return render_template('index.html', title="Chat Room")


@ app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            new_comment = Comment(author=current_user.username, user_id=current_user.id,
                                  post_id=post.id, comment=form.comment.data)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(request.referrer)
    else:
        comments = Comment.query.filter_by(post_id=post_id).all()
        return render_template('post.html', title='Post', post=post,
                               comments=comments, _category=post.category,
                               time=datetime.utcnow())
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', title='Post', post=post, form=form,
                           comments=comments, _category=post.category,
                           time=datetime.utcnow())


@app.route('/post/new/<string:_for>', methods=['POST', 'GET'])
@login_required
def new_post(_for):
    form = PostForm()
    if form.validate_on_submit():
        if form.image_post.data:
            post_pic = save_picture(form.image_post.data)
            post = Post(title=form.title.data, category=_for, content=form.content.data,
                        author=current_user, image_post=post_pic)
        else:
            post = Post(title=form.title.data, category=_for, content=form.content.data,
                        author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for(_for))
    return render_template('new_post.html', title='Post', form=form, legend='New Post', _category='')


@ app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@ login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.image_post.data = post.image_post
    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post')


@ app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    for comment in comments:
        db.session.delete(comment)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))


@ app.route('/post/<int:comment_id>/comment/delete', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment.author != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted', 'success')
    return redirect(request.referrer)


@app.route('/user/<string:username>')
def user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_dash.html', title='Dashboard', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='ayushverma01911@gmail.com', recipients=[user.email])
    msg.body = f'''
To reset your password click on the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, ignore this email and no changes will be made to your account.
    '''
    mail.send(msg)


@app.route('/reset_password/<int:change>', methods=['GET', 'POST'])
def reset_request(change):
    if change:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email for Password Reset has been sent.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form, _category='')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! You can login now.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form, _category='')


@app.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)


@ app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))