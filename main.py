import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from PIL import Image
import random

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "sjfaker045!#$kdhfa94rad"


class ImageForm(FlaskForm):
    img = FileField(label="File to upload:", validators=[DataRequired()])
    num = IntegerField(label="Number of colors:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


def rgb2hex(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ImageForm()
    if form.validate_on_submit():
        create_folder("static/images")
        img_name = form.data.get('img').filename
        saved_img = os.path.join("static/images", img_name)
        form.data.get('img').save(saved_img)
        color_num = form.data.get('num')
        with Image.open(saved_img) as im:
            colors = im.getcolors(im.size[0] * im.size[1])
            random_colors = random.sample(colors, k=color_num)
            random_colors = [rgb2hex(item[1]) for item in random_colors]
        return render_template("index.html", form=form, img=saved_img, colors=random_colors)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
