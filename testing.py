from db_functions import run_search_query_tuples
from db_functions import run_commit_query


def get_news(db_path):
    sql = """select news.title, news.subtitle, news.content, member.name
    from news 
    join member on news.member_id = member.member_id;
    """
    result = run_search_query_tuples(sql, (), db_path, True)

    for row in result:
        for k in row.keys():
            print(k)
            print(row[k])

def get_all(db_path):
    sql = "select * from news"
    result = run_search_query_tuples(sql, (), db_path)
    print(result)


#def signup_member(db_path):
#    sql = ""insert into member(first_name, last_name, email, password, authorisation)
#           values ("adia", "adia", "adia@adia", "adia", 1)""
#    result = run_commit_query(sql, (), db_path)
#    print(result)


if __name__ == "__main__":
    db_path = 'data/guitargroup_db.sqlite'
    get_news(db_path)