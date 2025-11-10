import psycopg2
import key as rds
import traceback

def run():
    try:
        with psycopg2.connect(host=rds.host, port=rds.port, user=rds.user, password=rds.password, database=rds.db) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_user, session_user;")
                print("users:", cur.fetchone())

                cur.execute("SHOW search_path;")
                print("search_path:", cur.fetchone()[0])

                cur.execute("SELECT has_schema_privilege(current_user, 'public', 'CREATE'), has_schema_privilege(current_user, 'public', 'USAGE');")
                print("has CREATE, USAGE on public:", cur.fetchone())

                cur.execute("SELECT nspname, pg_get_userbyid(nspowner) AS owner FROM pg_namespace WHERE nspname = 'public';")
                print("public schema owner:", cur.fetchone())

                cur.execute("SELECT rolname, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles WHERE rolname = %s;", (rds.user,))
                print("role flags:", cur.fetchone())

                print("\nTRY CREATE TABLE:")
                try:
                    cur.execute("CREATE TABLE test_perm_debug (id SERIAL PRIMARY KEY);")
                    conn.commit()
                    print("CREATE succeeded")
                    cur.execute("DROP TABLE test_perm_debug;")
                    conn.commit()
                    print("DROP succeeded")
                except Exception as e:
                    print("CREATE failed:")
                    traceback.print_exc()
    except Exception:
        traceback.print_exc()

if __name__ == '__main__':
    run()