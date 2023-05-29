from db_functions import run_search_query_tuples


def get_news(p):
    sql = """select news.title, news.subtitle, news.content, member.name
    from news
    join member on news.member_id = member.member_id;

    """

    result = run_search_query_tuples(sql, (), p)
    return result


if __name__ == "__main__":
    print(get_news('data/WQSA_db.sqlite'))
