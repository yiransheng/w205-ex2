from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt

import psycopg2



class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.conn = psycopg2.connect(database="tcount", user="twuser", password="tweetcount")
        self.counts = Counter()
       

    def process(self, tup):
        word = tup.values[0]
        self.counts[word] += 1

        cur = self.conn.cursor()
     
        self.upsert(cur, "tweetwordcount", ("word", ), word=word, count=self.counts[word])
        self.conn.commit()
        cur.close()

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
        self.emit([word, self.counts[word]])

    def upsert(self, db_cur, table, pk_fields, schema=None, **kwargs):
        """Updates the specified relation with the key-value pairs in kwargs if a
        row matching the primary key value(s) already exists.  Otherwise, a new row
        is inserted.  Returns True if a new row was inserted.
        schema     the schema to use, if any (not sanitized)
        table      the table to use (not sanitized)
        pk_fields  tuple of field names which are part of the primary key
        kwargs     all key-value pairs which should be set in the row
        """
        assert len(pk_fields) > 0, "must be at least one field as a primary key"
        if schema:
            rel = '%s.%s' % (schema, table)
        else:
            rel = table

        # check to see if it already exists
        where = ' AND '.join('%s=%%s' % pkf for pkf in pk_fields)
        where_args = [kwargs[pkf] for pkf in pk_fields]
        db_cur.execute("SELECT COUNT(*) FROM %s WHERE %s LIMIT 1" % (rel, where), where_args)
        fields = [f for f in kwargs.keys()]
        if db_cur.fetchone()[0] > 0:
            set_clause = ', '.join('%s=%%s' % f for f in fields if f not in pk_fields)
            set_args = [kwargs[f] for f in fields if f not in pk_fields]
            db_cur.execute("UPDATE %s SET %s WHERE %s" % (rel, set_clause, where), set_args+where_args)
            return False
        else:
            field_placeholders = ['%s'] * len(fields)
            fmt_args = (rel, ','.join(fields), ','.join(field_placeholders))
            insert_args = [kwargs[f] for f in fields]
            db_cur.execute("INSERT INTO %s (%s) VALUES (%s)" % fmt_args, insert_args)
            return True
