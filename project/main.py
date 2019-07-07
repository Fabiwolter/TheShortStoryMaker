# main.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Post
from .forms import EditProfileForm, PostForm, StoryForm, SelectStoryForm
from datetime import datetime
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile/<name>')
# protect the page + lets us use the current_user obj inside the fnct
@login_required
def profile(name):
    # user = current_user
    user = User.query.filter_by(name=name).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('profile.html', name=name, user=user, posts=posts)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.name)
    if form.validate_on_submit():
        current_user.name = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@main.route('/follow/<name>')
@login_required
def follow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('User {} not found.'.format(name))
        return redirect(url_for('index'))
    #if user == current_user:
    #    flash('You cannot follow yourself!')
    #    return redirect(url_for('user', name=name))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(name))
    return redirect(url_for('main.profile', name=name))

@main.route('/unfollow/<name>')
@login_required
def unfollow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('User {} not found.'.format(name))
        return redirect(url_for('index'))
    #if user == current_user:
    #    flash('You cannot unfollow yourself!')
    #    return redirect(url_for('user', name=name))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(name))
    return redirect(url_for('main.profile', name=name))

#logik für "last_seen" bzw letzte Aktivität
@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main.route('/followed_stories', methods=['GET', 'POST'])
@login_required
def followed_stories():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.followed_stories'))
    posts = current_user.followed_posts().all()
    return render_template("followed_stories.html", title='Followed Stories', form=form,
                           posts=posts)
                        
@main.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    selectform = SelectStoryForm()
    selectform.story.choices = [(story.storyname, story.storyname) for story in Post.query.group_by(Post.storyname).distinct()]
    posts = Post.query.filter_by(storyname = selectform.story.data).all()
    if request.method == 'POST':
        return redirect('/explore/' + selectform.story.data)
    return render_template('explore.html', title='Explore', posts=posts, selectform=selectform)

@main.route('/explore/<storyname>', methods=['GET', 'POST'])
def story(storyname):
    selectform = SelectStoryForm()
    selectform.story.choices = [(story.storyname, story.storyname) for story in Post.query.group_by(Post.storyname).distinct()]
    posts = Post.query.order_by(Post.timestamp.asc()).filter_by(storyname = storyname).all()
    if request.method == 'POST':
        return redirect('/explore/' + selectform.story.data)
    return render_template('explore.html', title='Explore', posts=posts, selectform=selectform, storyname=storyname)

@main.route('/writeastory')
@login_required
def writeastory():
    return redirect('/writer/Story Name')

@main.route('/writer/<storyname>', methods=['GET', 'POST'])
@login_required
def writer(storyname):
    postform = PostForm()
    storyform = StoryForm(storyname)
    if postform.validate_on_submit():
        post = Post(body=postform.post.data, author=current_user, storyname=storyform.storyname.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.writer', storyname=storyname))
    elif request.method == 'GET':
        storyform.storyname.data = storyname

    # user = User.query.filter_by(name=name).first_or_404()
    posts = Post.query.filter_by(storyname = storyname).all()
    #  ...storyform.storyname.data
    return render_template('writer.html', postform=postform, storyform=storyform, storyname=storyname, posts=posts)