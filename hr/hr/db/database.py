import psycopg2


class Database(object):
    class __Singleton:
        # https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html
        def __init__(self, db_url):
            self.conn = psycopg2.connect(db_url)
            self.cursor = self.conn.cursor()

    instance = None

    def __init__(self, arg):
        if not Database.instance:
            Database.instance = Database.__Singleton(arg)

    def save(self, job):
        query = """
        INSERT INTO jobs (date, text, ref, url, email) 
        VALUES (%s, %s, %s, %s ,%s)
        """
        record = (job['date'], job['text'], job['ref'], job['url'], job['email'])
        self.instance.cursor.execute(query, record)
        self.instance.conn.commit()

    def find_by_url(self, job):
        query = """
        SELECT url 
        FROM jobs 
        WHERE url=(%s)
        """
        self.instance.cursor.execute(query, (job['url'],))
        return self.instance.cursor.fetchall()

    def find_or_create(self, job):
        if not len(self.find_by_url(job)):
            self.save(job)
