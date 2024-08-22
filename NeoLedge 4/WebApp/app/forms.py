from wtforms import Form, FileField
from wtforms.validators import DataRequired

class ImageForm(Form):
    image = FileField('image', validators=[DataRequired()])
