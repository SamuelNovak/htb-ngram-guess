import psycopg2
import json

def connect():
    with open("ngram_guesser/config.json") as f:
        config = json.loads(f.read())
    try:
        return psycopg2.connect("dbname='{database}' user='{user}' host='{host}' password='{password}'".format_map(config))
    except:
        print("Unable to connect to the database.")
        return None

def load_players(conn):
    if conn != None:
        cur = conn.cursor()
        cur.execute("SELECT * from players;")
        rows = cur.fetchall()
        print(rows)
        return {row[0]: [None, row[2]] for row in rows}
    else:
        print("Warning! No database connection!")
        return {}

def load_player(conn, player):
    if conn != None:
        cur = conn.cursor()
        cur.execute("SELECT * from players WHERE player='{}';".format(player))
        rows = cur.fetchall()
        print(rows)
        if len(rows) == 1:
            return [None, rows[0][2]]
        else:
            return [None, 0]
    else:
        print("Warning! No database connection!")
        return [None, 0]

def is_player_in_db(conn, player):
    if conn != None:
        cur = conn.cursor()
        cur.execute("SELECT * from players WHERE player='{}';".format(player))
        rows = cur.fetchall()
        return len(rows) >= 1
    else:
        print("Warning! No database connection!")
        return False

def save_player(conn, player, points):
    if conn != None:
        cur = conn.cursor()
        if is_player_in_db(conn, player):
            cur.execute("UPDATE players SET points={} WHERE player='{}';".format(points, player))
        else:
            cur.execute("INSERT INTO players VALUES ('{}', {});".format(player, points))
        conn.commit()
        return True
    else:
        print("Warning! No database connection!")
        return False


# def load_players():
#     try:
#         with open("ngram_guesser/players.json", "r") as f:
#             data = json.loads(f)
#             return {player: [None, points] for (player, points) in data.items()}
#     except:
#         return {}

# def save_players(players):
#     with open("ngram_guesser/players.json", "w") as f:
#         f.write(json.dumps({player: value[1] for (player, value) in players.items()}))
