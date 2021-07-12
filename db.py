from sqlalchemy import create_engine, table
import pandas as pd
# from datetime import timedelta
from dateutil.relativedelta import relativedelta

import config

engine = create_engine("postgresql://{user}:{password}@{ip}:{port}/{dbname}"
                       .format(user=config.user, password=config.password,
                               ip=config.ip, port=config.port,
                               dbname=config.dbname))

conn = engine.connect()
# time.strftime("%Y-%m-%d %H-%M-%S")


def user_in_db(user_id):
    df = pd.read_sql("SELECT * FROM users WHERE user_id = {}".format(user_id), engine)
    if len(df):
        return True
    else:
        return False


def add_new_user(user_id, nickname):
    conn.execute("INSERT INTO users(user_id, nickname) values ({user_id}, '{nickname}')"
                 .format(user_id=user_id, nickname=nickname))


def get_username(user_id):
    usernames = pd.from_sql("SELECT * FROM users WHERE user_id = {}".format(user_id))
    return usernames["username"][0]


def get_interval_costs(user_id, start_time, weeks=0, months=0, years=0):
    costs = pd.read_sql("SELECT * FROM costs WHERE user_id = %s AND data >= %s \
                        ORDER BY cost desc LIMIT 21",
                        engine,
                        params=(user_id,
                                str(start_time - relativedelta(weeks=weeks,
                                                               months=months,
                                                               years=years))))
    return costs.T.to_dict().values()


def get_interval_sum(user_id, start_time, weeks=0, months=0, years=0):
    sums = pd.read_sql("SELECT sum(cost) FROM costs WHERE user_id = %s \
                       AND data >= %s GROUP BY user_id",
                       engine,
                       params=(user_id,
                               str(start_time - relativedelta(weeks=weeks,
                                                              months=months,
                                                              years=years))))
    return sums["sum"][0]


def get_costs_statistic(user_id, start_time, weeks=0, months=0, years=0):
    df = pd.read_sql("SELECT type, sum(cost) as cost FROM costs \
                     WHERE user_id = %s AND data >= %s GROUP BY type", engine,
                     params=(user_id, str(start_time - relativedelta(weeks=weeks,
                                                                     months=months,
                                                                     years=years))))
    return df.cost.values, df.type.values


# deprecated
def add_user_to_family(username, family_id):
    pass


def create_family(user_id, familyname):
    pass


def get_user_family(user_id):
    pass


def add_cost(user_id, cost, buy_type, description, data):
    conn.execute("INSERT INTO costs(user_id, cost, type, description, data) values \
                 ({user_id}, {cost}, '{type}', '{description}', '{data}')".format(
                    user_id=user_id, cost=cost,
                    type=buy_type, description=description, data=data))
    return "OK"


def link_to_family(user_id, ref_part):
    pass


def get_family_data(user_id):
    pass


def remove_user_from_family(user_id, family_id):
    pass