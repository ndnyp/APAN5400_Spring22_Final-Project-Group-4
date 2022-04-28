from flask import render_template, make_response, send_from_directory
from app import app
from app.forms import SearchForm
import bson
from elasticsearch import Elasticsearch
from bson.objectid import ObjectId
from pprint import pprint


es_connection = Elasticsearch(
    "https://elastic:apan5400@localhost:9200", use_ssl=True, verify_certs=False
)


@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page."""
    form = SearchForm()
    search_results = None
    if form.validate_on_submit():
        search_by = form.search_by.data
        search_terms = form.search_terms.data
        popular = form.popular.data

        index_name = "book_data_v4"

        if search_by == "subjects":
            match_condition = "match"
            order = "asc"
        elif search_by == "author":
            match_condition = "match_phrase"
            order = "asc"
        else:
            match_condition = "match_phrase"
            order = "desc"

        resp = es_connection.search(
            index=index_name,
            size=10,
            query={
                "bool": {
                    "must": [
                        {
                            match_condition: {
                                search_by: search_terms,
                            },
                        },
                        {
                            "match": {
                                "NYT_bestseller": popular,
                            },
                        },
                    ]
                }
            },
            sort={"number_of_pages": {"order": order}},
        )
        hits = resp["hits"]["hits"]
        if len(hits) > 0:
            search_results = hits

    return render_template("home.html", form=form, search_results=search_results)


@app.route("/static/<path>", methods=["GET"])
def static_serve(path):
    return send_from_directory("static", path)
