import psycopg2
from psycopg2._psycopg import IntegrityError


class Database(object):
    class __Singleton:
        # https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self):
            # @TODO inject params
            self.conn = psycopg2.connect(
                host="localhost",
                dbname="hr_jobs",
                user="postgres",
                password="postgres"
            )
            self.cursor = self.conn.cursor()

    instance = None

    def __init__(self):
        if not Database.instance:
            Database.instance = Database.__Singleton()

    def save(self, job):
        query = """
        INSERT INTO jobs (date, text, ref, url, email) 
        VALUES (%s, %s, %s, %s ,%s)
        """
        record = tuple(job.values())
        try:
            self.instance.cursor.execute(query, record)
            self.instance.conn.commit()
        except IntegrityError as ex:
            print(ex)
