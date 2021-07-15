from sqlalchemy import create_engine, table
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

import config

engine = create_engine("postgresql://{user}:{password}@{ip}:{port}/{dbname}"
                       .format(user=config.user, password=config.password,
                               ip=config.ip, port=config.port,
                               dbname=config.dbname))

conn = engine.connect()


def screen(text):
    return "''".join(str(text).split("'"))


def user_in_db(user_id):
    df = pd.read_sql("SELECT * FROM users WHERE user_id = {}".format(user_id), conn)
    if len(df):
        return True
    else:
        return False


def add_new_user(user_id, nickname):
    conn.execute(f"INSERT INTO users(user_id, nickname) values ({user_id}, '{screen(nickname)}')")


def get_username(user_id):
    usernames = pd.read_sql("SELECT * FROM users WHERE user_id = {}".format(user_id))
    return usernames["username"][0]


def get_interval_costs(user_id, start_time, weeks=0, months=0, years=0):
    costs = pd.read_sql("SELECT * FROM costs WHERE user_id = %s AND data >= %s \
                        ORDER BY cost desc LIMIT 21",
                        conn,
                        params=(user_id,
                                str(start_time - relativedelta(weeks=weeks,
                                                               months=months,
                                                               years=years))))
    return costs.T.to_dict().values()


def get_interval_sum(user_id, start_time, weeks=0, months=0, years=0):
    sums = pd.read_sql("SELECT sum(cost) FROM costs WHERE user_id = %s \
                       AND data >= %s GROUP BY user_id",
                       conn,
                       params=(user_id,
                               str(start_time - relativedelta(weeks=weeks,
                                                              months=months,
                                                              years=years))))
    if len(sums["sum"]):
        return sums["sum"][0]
    else:
        return None


def get_costs_statistic(user_id, start_time, weeks=0, months=0, years=0):
    df = pd.read_sql("SELECT type, sum(cost) as cost FROM costs \
                     WHERE user_id = %s AND data >= %s GROUP BY type", conn,
                     params=(user_id, str(start_time - relativedelta(weeks=weeks,
                                                                     months=months,
                                                                     years=years))))
    return df.cost.values, df.type.values


def get_family_costs_statistic(family_id):
    month_period = str(datetime.now() - relativedelta(months=1))
    costs = pd.read_sql(f"SELECT sum(cost) as cost, type FROM costs \
                        LEFT JOIN users ON costs.user_id = users.user_id \
                        WHERE family_id =  {family_id}\
                        AND costs.data >= '{month_period}' \
                        GROUP BY type ORDER BY cost DESC", conn)
    return costs.cost.values, costs.type.values


def get_users_infamily_sums(family_id):
    month_period = str(datetime.now() - relativedelta(months=1))
    users_costs = pd.read_sql(f"SELECT sum(cost) as cost, nickname FROM costs \
                              LEFT JOIN users ON costs.user_id = users.user_id \
                              WHERE family_id = {family_id} \
                              AND costs.data >= '{month_period}' \
                              GROUP BY nickname ORDER BY cost DESC", conn)
    return users_costs.nickname.values, users_costs.cost.values


def get_family_total_in_month(family_id):
    month_period = str(datetime.now() - relativedelta(months=1))
    total = pd.read_sql(f"SELECT sum(cost) as cost, family_id FROM costs \
                        LEFT JOIN users ON costs.user_id = users.user_id \
                        WHERE family_id = {family_id} \
                        AND costs.data >= '{month_period}' \
                        GROUP BY family_id ORDER BY cost DESC", conn)["cost"]
    if len(total):
        return total[0]
    else:
        return None


def create_family(user_id, familyname):
    families = pd.read_sql(f"SELECT * FROM families \
                           WHERE creator_id = {user_id}", conn)
    if len(families["creator_id"]) == 0:
        conn.execute(f"INSERT INTO families(creator_id, name) values \
                 ({user_id}, '{screen(familyname)}')")
        conn.execute(f"UPDATE users SET family_id = \
                     (SELECT id FROM families WHERE creator_id = {user_id}) \
                     WHERE user_id = {user_id}")
        return "OK"
    else:
        return "EXISTS"


def link_user_to_family(user_id, ref_part):
    conn.execute(f"UPDATE users SET family_id = (SELECT family_id FROM links \
                  WHERE ref_part = '{screen(ref_part)}') WHERE user_id = {user_id}")


def get_user_family(user_id):
    family_id = pd.read_sql(f"SELECT family_id as fid FROM users \
                            WHERE user_id = {user_id}", conn)["fid"][0]
    return family_id


def get_family_by_admin_id(user_id):
    family_id = pd.read_sql(f"SELECT id FROM families \
                            WHERE creator_id = {user_id}", conn)["id"]
    if len(family_id):
        return family_id[0]
    else:
        return None


def add_cost(user_id, cost, buy_type, description, data):
    conn.execute(f"INSERT INTO costs(user_id, cost, type, description, data) values \
                 ({screen(user_id)}, {cost}, '{screen(buy_type)}',\
                 '{screen(description)}', '{screen(data)}')")
    return "OK"


def append_family_link(family_id, ref_part):
    conn.execute(f"INSERT INTO links(family_id, ref_part) \
                 values ({family_id}, '{ref_part}')")


def get_family_name(user_id):
    raw_data = pd.read_sql("SELECT families.name FROM users \
                           LEFT JOIN families ON users.family_id = families.id \
                           WHERE user_id = %s", conn, params=(user_id,))
    return raw_data["name"][0]


def remove_user_from_family(user_id, family_id):
    if family_id is None:
        return "INCORRECTFID"
    if get_user_family(user_id) == family_id:
        creator_id = pd.read_sql(f"SELECT creator_id FROM families \
                                 WHERE id = {family_id}", conn)["creator_id"][0]
        if user_id == creator_id:
            return "USERISADMIN"
        conn.execute(f"UPDATE users SET family_id = NULL \
                     WHERE user_id = {user_id}")
        return "OK"
    else:
        return "NOTINFAMILY"


def get_userid_by_nickname(nickname):
    user_id = pd.read_sql(f"SELECT user_id FROM users WHERE nickname = '{screen(nickname)}'",
                          conn)["user_id"]
    if len(user_id):
        return user_id[0]
    else:
        return None