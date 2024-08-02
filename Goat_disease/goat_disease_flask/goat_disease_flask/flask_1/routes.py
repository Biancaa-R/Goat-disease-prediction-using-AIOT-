import os
import secrets
from flask import render_template,flash,redirect,url_for, flash, request, abort
from flask_1.models import User,Post
from flask_1 import app,db,bcrypt
from flask_1.forms import RegistrationForm,LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user,current_user, logout_user, login_required


data=[{"content":'''Goat farming is a vital agricultural enterprise that supports the livelihoods of millions of farmers around the globe. Goats provide a wide array of products, including meat, milk, fiber, and hides, which are integral to the economies of many rural communities. However, the productivity and health of goats are often compromised by various infectious and non-infectious diseases. These diseases not only affect the well-being of the animals but also have substantial economic ramifications for the farmers and the broader agricultural economy.

The economic impact of goat diseases is multifaceted. Infected animals often exhibit reduced growth rates, lower milk yields, and poor reproductive performance, which directly diminishes the overall productivity of the herd. Increased mortality rates and the need for frequent veterinary interventions further escalate the costs for goat farmers. Additionally, outbreaks of contagious diseases can lead to trade restrictions and loss of market access, further exacerbating the economic burden.

Diseases such as Blue Tongue, Anthrax, Tetanus, and Orf Scab are particularly concerning due to their severe symptoms and high morbidity and mortality rates. These diseases can spread rapidly within herds and, in some cases, to other livestock or even humans, posing significant public health risks. The management and control of these diseases require substantial investments in veterinary care, biosecurity measures, and farmer education, which can strain the financial resources of small-scale farmers.

Understanding the epidemiology and impact of these diseases is crucial for developing effective prevention and control strategies. By mitigating the incidence and spread of diseases in goats, farmers can enhance animal welfare, improve productivity, and ensure the sustainability of their farming operations. Consequently, addressing goat diseases is not only essential for animal health but also for the economic stability and growth of rural communities that depend on goat farming as a primary source of income.'''},
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
    if num :  # If it's not the first iteration
        if list1[1] == "1":
            disease.append("ppr")
        if list1[2] == "1":
            disease.append("anthrax")
        if list1[3] == "1":
            disease.append("tetanus")
        disease_str = ", ".join(disease) if disease else "none"
        dict1 = {
            "author": list1[0]-1,
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
    return render_template("about.html",posts=data)

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