from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import User
from wtforms import SelectField

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=250)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(name=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
                
class PostForm(FlaskForm):
    post = TextAreaField('Write something', validators=[
        DataRequired(), Length(min=1, max=5000)
    ])
    submit = SubmitField('Submit')

class StoryForm(FlaskForm):
    storyname = TextAreaField('The Name of this Story', validators=[Length(min=0, max=100)])
    submitstoryname = SubmitField('Submit')

    def __init__(self, original_storyname, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        self.original_storyname = original_storyname

class SelectStoryForm(FlaskForm):
    story = SelectField('story', choices=[])