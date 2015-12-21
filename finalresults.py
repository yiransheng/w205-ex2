import psycopg2
import argparse

def query_word(word, cur):
    cur.execute("SELECT count FROM tweetwordcount WHERE word='%s'" % word)
    result = cur.fetchone()
    return result if result else (0,)


def query_all(cur, limit=1000):
    cur.execute("SELECT * FROM tweetwordcount ORDER BY COUNT DESC")
    result = cur.fetchmany(limit)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('word', help='Word to query count for.', default=None, nargs='?')
    parser.add_argument(
        '-n', '--num',
        help='max number of words to return',
        type=int,
        default=1000)

    args = parser.parse_args()

    with psycopg2.connect(database="tcount", user="twuser", password="tweetcount") as conn:
        with conn.cursor() as cur:
            if args.word is not None:
                count, = query_word(args.word, cur)
                print 'Total number of occurences of \"%s\" is: %d' % (args.word, count)
            else:
                print query_all(cur, args.num)
