"""
A Sample Web-DB Application for DB-DESIGN lecture
Copyright (C) 2022 Yasuhiro Hayashi
"""
from psycopg2 import sql, connect, ProgrammingError
import flaskdb.var as v
from flaskdb.models import Item, Classes


class DataAccess:

    # Constractor called when this class is used. 
    # It is set for hostname, port, dbname, useranme and password as parameters.
    def __init__(self, hostname, port, dbname, username, password):
        self.dburl = "host=" + hostname + " port=" + str(port) + \
                     " dbname=" + dbname + " user=" + username + \
                     " password=" + password

    # This method is used to actually issue query sql to database. 
    def execute(self, query, autocommit=True):
        with connect(self.dburl) as conn:
            if v.SHOW_SQL:
                print(query.as_string(conn))
            conn.autocommit = autocommit
            with conn.cursor() as cur:
                cur.execute(query)
                if not autocommit:
                    conn.commit()
                try:
                    return cur.fetchall()
                except ProgrammingError as e:
                    return None

    # For mainly debug, This method is used to show sql to be issued to database. 
    def show_sql(self, query):
        with connect(self.dburl) as conn:
            print(query.as_string(conn))

    # search item data
    def search_items(self):
        query = sql.SQL("""
            SELECT * FROM \"items\"
        """)
        # self.show_sql(query)
        results = self.execute(query, autocommit=True)
        item_list = []
        for r in results:
            item = Item()
            item.id = r[0]
            item.user_id = r[1]
            item.itemname = r[2]
            item.price = r[3]
            item_list.append(item)
        return item_list

    # search item data by itemname
    def search_items_by_itemname(self, itemname):
        query = sql.SQL("""
            SELECT * FROM \"items\" WHERE itemname LIKE {itemname}
        """).format(
            itemname = sql.Literal(itemname)
        )
        # self.show_sql(query)
        results = self.execute(query, autocommit=True)
        item_list = []
        for r in results:
            item = Item()
            item.id = r[0]
            item.user_id = r[1]
            item.itemname = r[2]
            item.price = r[3]
            item_list.append(item)
        return item_list

    def add_item(self, item):
        query = sql.SQL("""
            INSERT INTO \"items\" ( {fields} ) VALUES ( {values} )
        """).format(
            tablename = sql.Identifier("items"),
            fields = sql.SQL(", ").join([
                sql.Identifier("itemname"),
                sql.Identifier("price")
            ]),
            values = sql.SQL(", ").join([
                sql.Literal(item.itemname),
                sql.Literal(item.price)
            ])
        )
        self.execute(query, autocommit=True)

    def management(self, contents):
        query = sql.SQL("""
                    SELECT \"username\" FROM \"s_users\" WHERE {contents} = any(\"management\");
                """).format(
            contents = sql.Literal(contents)
        )

        self.show_sql(query)
        results = self.execute(query, autocommit=True)

        return results

    def qr_time(self, contents):
        query = sql.SQL("""
                    SELECT \"qr_start.id\",\"qr_start.classes_id\", \"qr_start.qr_start_time\", \"qr_stop.qr_end_time\" FROM \"qr_start\", \"qr_stop\" WHERE \"qr_start.id = qr_stop.id\" AND \"qr_start.classes_id\" = {contents} ;
                """).format(
            contents = sql.Literal(contents)
        )

        self.show_sql(query)
        results = self.execute(query, autocommit=True)

        return results

    def attend_check(self):
        query = sql.SQL("""
                    SELECT \"qr_start.id\", \"qr_start.classes_id\", \"attend.students_id\", \"attend.date_time\", \"qr_start.qr_start_time\", \"qr_stop.qr_end_time\" 
                    FROM \"qr_start\", \"qr_stop\", \"attend\" 
                    WHERE \"attend.date_time\" 
                    BETWEEN \"qr_start.qr_start_time\" 
                    AND \"qr_stop.qr_end_time\" 
                    AND \"qr_start.classes_id = attend.classes_id\" 
                    AND \"qr_start.id = qr_stop.id\" ;
                """).format(
            # contents = sql.Literal(contents)
        )

        self.show_sql(query)
        results = self.execute(query, autocommit=True)

        return results


# SELECT qr_start.id, qr_start.classes_id, qr_start.qr_start_time, qr_stop.qr_end_time
#                     FROM qr_start, qr_stop
#                     WHERE qr_start.id = qr_stop.id
#                     AND  qr_start.classes_id  =1
#                      ;