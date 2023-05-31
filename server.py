from flask import Flask, render_template, request, redirect, url_for
from db_functions import run_search_query_tuples
from datetime import datetime

app = Flask(__name__)
db_path = 'data/guitargroup_db.sqlite'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/learn')
def learn():
    return render_template("learn.html")


@app.route('/schedule')
def schedule():
    return render_template("schedule.html")

@app.route('/news')
def news():
    #query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
        from news
        join member on news.member_id= member.member_id
        order by news.newsdate desc;
        """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("news.html", news= result)


if __name__ == "__main__":
    app.run(debug=True)