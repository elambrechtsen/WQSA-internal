from db_functions import run_search_query_tuples


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



    # print(result)
    # first_result = result[0]
    # print(first_result['title'])


if __name__ == "__main__":
    db_path = 'data/WQSA_db.sqlite'
    get_news(db_path)
    # print(get_news('data/WQSA_db.sqlite'))
