from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_by = SelectField(
        label="Search by",
        choices=[("subjects", "Genre"), ("author", "Author"), ("title", "Title")],
    )
    search_terms = StringField("Search terms")
    popular = BooleanField("New York Times Best Seller?")
    submit = SubmitField("Search")
