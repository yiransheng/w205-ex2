import psycopg2
import argparse


def query_hist(cur, lo=0, hi=1):
    cur.execute("SELECT * FROM tweetwordcount WHERE count>%d AND count<= %d" % (lo, hi))
    result = cur.fetchall()
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("lower", help="k1", type=int)
    parser.add_argument("upper", help="k2", type=int)

    args = parser.parse_args()

    with psycopg2.connect(database="tcount", user="twuser", password="tweetcount") as conn:
        with conn.cursor() as cur:
            results = query_hist(cur, args.lower, args.upper)
            for (w,count) in results:
                print "%s : %d" % (w, count)
