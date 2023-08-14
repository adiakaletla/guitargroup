from flask import Flask, render_template, request, redirect, url_for, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "asdfasdfasdf"
db_path = 'data/guitargroup_db.sqlite'


@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %I:%M %p")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/learn')
def learn():
    return render_template("learn.html")


@app.route('/schedule')
def schedule():
    # query for the page
    print("start schedule")
    sql = """select schedule.schedule_id, schedule.event_name, schedule.location, schedule.date_time, 
        schedule.notes, member.first_name
        from schedule
        join member on schedule.member_id= member.member_id
        order by schedule.date_time desc;
        """
    print("start schedule2")
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    return render_template("schedule.html", schedule=result)


@app.route('/schedule_cud', methods=['GET', 'POST'])
def schedule_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an id and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from schedule where schedule_id = ?"
            values_tuple = (data['id'],)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('schedule'))
        elif data['task'] == 'update':
            sql = """ select event_name, location, date_time,notes from schedule where schedule_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("schedule_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'event_name': 'Test event', 'location': 'Test location', 'date_time': '2023-05-17 12:10:00.000',
                    'notes': 'Test notes'}
            return render_template("schedule_cud.html",
                                   id=0,
                                   task=data['task'],
                                   event_name=temp['event_name'],
                                   location=temp['location'],
                                   date_time=temp['date_time'],
                                   notes=temp['notes'])
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected form information
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add the new news entry to the database
            mem_id = session['id']
            sql = """insert into schedule(event_name,location,date_time,notes, member_id)
                        values(?,?,?, datetime('now', 'localtime'),?)"""
            values_tuple = (f['event_name'], f['location'], f['notes'], mem_id)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('schedule'))
        elif data['task'] == 'update':
            sql = """update schedule set event_name=?, location=?, date_time=datetime('now'), notes=? 
                        where schedule_id=?"""
            values_tuple = (f['event_name'], f['location'], f['notes'], data['id'])
            run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database at the id
            return redirect(url_for('schedule'))

    return render_template("schedule_cud.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        f = request.form
        sql = """ select first_name, last_name, email, password, authorisation from member where email = ? """
        values_tuple = (f['email'].lower(),)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        print(result)
        error = "User already exists"
        if result:
            print("second else")
            return render_template("signup.html", email=f['email'], password=f['pswd'], error=error)
        else:
            sql = """insert into member( first_name, last_name, email, password, authorisation)
                        values(?,?,?,?,1);"""
            values_tuple = (f['first_name'], f['last_name'], f['email'].lower(), f['pswd'])
            result = run_commit_query(sql, values_tuple, db_path)
            print(result)
            error = "You have successfully signed up.  Please log in to continue."
            return render_template("login.html", email=f['email'], error=error)


@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('auth', 1)
    session.clear()
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        f = request.form
        print(f)
        sql = """ select member_id, first_name, last_name, email, password, authorisation 
                  from member where email = ? """
        values_tuple = (f['email'].lower(),)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        print(result)
        error = "User ID does not exist.  Please sign up first."
        if result:
            result = result[0]
            if result['password'] == f['pswd']:
                print("Login successful")
                session['auth'] = result['authorisation']
                session['name'] = result['first_name'] + ' ' + result['last_name']
                session['id'] = result['member_id']
                print(session)
                return redirect(url_for('index'))
            else:
                return render_template("login.html", email=f['email'], password=f['pswd'], error=error)
        else:
            return render_template("login.html", email=f['email'], password=f['pswd'], error=error)


@app.route('/news')
def news():
    # query for the page
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.first_name
                from news
                join member on news.member_id = member.member_id
                order by news.newsdate desc;
          """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)
    sql = """select comments.comment, comments.comment_date, comments.commenter_id, 
                    comments.news_tag_id, member.first_name
                from comments
                join news on news.news_id = comments.news_tag_id
                join member on comments.commenter_id = member.member_id
                order by comments.comment_id asc;
          """
    comms = run_search_query_tuples(sql, (), db_path, True)
    print(comms)

    return render_template("news.html", news=result, comments=comms)


# noinspection SqlDialectInspection
@app.route('/news_cud', methods=['GET', 'POST'])
def news_cud():
    # collect data from the web address
    data = request.args
    required_keys = ['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create read update on news (key not present)"
            return render_template('error.html', message=message)
    # have an id and a task key
    if request.method == "GET":
        if data['task'] == 'delete':
            sql = "delete from news where news_id = ?"
            values_tuple = (data['id'],)
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """ select title, subtitle, content from news where news_id=?"""
            values_tuple = (data['id'],)
            result = run_search_query_tuples(sql, values_tuple, db_path, True)
            result = result[0]
            return render_template("news_cud.html",
                                   **result,
                                   id=data['id'],
                                   task=data['task'])
        elif data['task'] == 'add':
            # dummy data for testing
            temp = {'title': 'Test Title', 'subtitle': 'Test subtitle', 'content': 'Test Content'}
            return render_template("news_cud.html",
                                   id=0,
                                   task=data['task'],
                                   title=temp['title'],
                                   subtitle=temp['subtitle'],
                                   content=temp['content'])
        elif data['task'] == 'comment':
            # dummy data for testing
            temp = {'content': 'Test Comment'}
            return render_template("news_cud.html",
                                   id=data['id'],
                                   task=data['task'],
                                   content=temp['content'])
        else:
            message = "Unrecognised task coming from news page"
            return render_template('error.html', message=message)
    elif request.method == "POST":
        # collected form information
        f = request.form
        print(f)
        if data['task'] == 'add':
            # add the new news entry to the database
            sql = """insert into news(title, subtitle, content, newsdate, member_id)
                        values(?,?,?, datetime('now', 'localtime'), ?)"""
            values_tuple = (f['title'], f['subtitle'], f['content'], session['id'])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))
        elif data['task'] == 'update':
            sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now') where news_id=?"""
            values_tuple = (f['title'], f['subtitle'], f['content'], data['id'])
            run_commit_query(sql, values_tuple, db_path)
            # collect the data from the form and update the database
            return redirect(url_for('news'))
        elif data['task'] == 'comment':
            sql = """insert into comments(comment, comment_date, commenter_id, news_tag_id)
                        values(?, datetime('now', 'localtime'), ?, ?)"""
            values_tuple = (f['content'], session['id'], data['id'])
            run_commit_query(sql, values_tuple, db_path)
            return redirect(url_for('news'))

    return render_template("news_cud.html")


if __name__ == "__main__":
    app.run(debug=True)
