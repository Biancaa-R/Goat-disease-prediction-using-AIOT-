import os
import secrets
from flask import render_template,flash,redirect,url_for, flash, request, abort
from flask_1.models import User,Post
from flask_1 import app,db,bcrypt
from flask_1.forms import RegistrationForm,LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user,current_user, logout_user, login_required

posts1=[
    {
        'author':"cory", 'title':'blog_post_1',"content":"The first post","date":"january 2020"
    },
    {
        "author":"harry","title":"Issues in indian farming","content":'''One of the major challenges faced by Indian agriculture is the problem of soil degradation and nutrient depletion. Soil degradation occurs due to several factors such as erosion, loss of organic matter, and chemical pollution, amongst others. As a result, Indian soil is losing its fertility at an alarming rate, leading to decreased crop yields and reduced productivity.

Farmers often resort to using chemical fertilizers to compensate for the loss of soil fertility, which only exacerbates the problem. The overuse of chemical fertilizers damages the soil microbiome and reduces its ability to retain moisture and essential nutrients.

Furthermore, soil degradation also contributes to environmental issues like air and water pollution. When soil loses its fertility, it affects the quality of crops, which in turn affects human health and well-being.

To address this issue, farmers need to adopt sustainable practices like crop rotation, intercropping, and agroforestry. These practices help to restore soil fertility and reduce soil erosion. For example, crop rotation involves planting different crops on the same land in successive seasons. This helps to replenish soil nutrients and reduce pest and disease buildup.''',"date":"nov 2023"
    }
]
       

import requests
import json

posts = []
r = requests.get("https://api.thingspeak.com/channels/2567333/feeds.json?api_key=T1YTUYGYW4TUOLM4&results=2")
n = json.loads(r.text)

num = 0
for i in range(len(n["feeds"])):
    disease = []
    list1 = [n["feeds"][i]["entry_id"], n['feeds'][i]['field1'], n['feeds'][i]['field2'], n['feeds'][i]['field3'], n['feeds'][i]['created_at']]
    num += 1
    if num != 1:  # If it's not the first iteration
        if list1[1] == "1":
            disease.append("ppr")
        if list1[2] == "1":
            disease.append("anthrax")
        if list1[3] == "1":
            disease.append("tetanus")
        disease_str = ", ".join(disease) if disease else "none"
        dict1 = {
            "author": list1[0],
            "title": "disease detected on " + list1[4],
            "content": "The diseases detected is/are " + disease_str,
            "date": list1[4]
        }
        posts.append(dict1)


print(posts)
@app.route("/")
def home():
    return render_template('home.html',posts=posts,title="home sweet home") #we will have access to this variable in the template

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register",methods=['POST','GET']) #list of allowed methods in our route
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    #creating instance of the registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}','success') #easy to send ot alert , category
        return redirect(url_for('home'));
    return render_template("register_1.html",title='Register',form=form)
# just like how we set posts , we have access to this instance form in the register template for showing the data

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        #if form.email.data=="admin@gmail.com" and form.password.data=="hello":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
                '''flash("You have successfully logged in","success")
                return redirect(url_for('home'))'''
        else:
            flash("Login unsuccessful please check your password")
    return render_template("login.html",title='Login',form=form)
@app.route("/post/new", methods=['GET', 'POST'])
#@login_required

def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

'''def new_post():
    return render_template('create_post.html',title='New Post')'''