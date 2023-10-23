import os
import environ
import requests
import psycopg2
from datetime import datetime, date, timezone
import sys

def add_movie(movie_id):
    env = environ.Env()
    environ.Env.read_env('.env')
    print('API_KEY: ', env('API_KEY'))
    print('API_TOKEN: ', env('API_TOKEN'))

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {env('API_TOKEN')}"
    }

    # Obtener detalles de la película
    movie_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US', headers=headers)
    print(movie_response.json())
    m = movie_response.json()

    conn = psycopg2.connect("dbname=django_bootstrap user=ubuntu password=bugalox3")
    cur = conn.cursor()

    sql = 'SELECT * FROM movies_movie WHERE title = %s'
    cur.execute(sql, (m['title'],))
    movie_exists = cur.fetchall()

    print(movie_exists)

    # Obtener detalles del reparto y el equipo técnico
    credits_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US', headers=headers)
    credits_data = credits_response.json()

    # Obtener actores y equipo técnico
    actors = credits_data.get('cast', [])[:10]
    crew = credits_data.get('crew', [])[:15]

    print("Actors:", actors)
    print("Crew:", crew)

    actors = [(actor['name'], actor['known_for_department']) for actor in actors]
    crew = [(job['name'], job['job']) for job in crew]

    print("Actors after processing:", actors)
    print("Crew after processing:", crew)

    credits_list = actors + crew

    jobs = [job for person, job in credits_list]
    jobs = set(jobs)
    print("Jobs:", jobs)

    if jobs:
        sql = 'SELECT * FROM movies_job WHERE name IN %s'
        cur.execute(sql, (tuple(jobs),))
        jobs_in_db = cur.fetchall()

        jobs_to_create = [(name,) for name in jobs if name not in [item[1] for item in jobs_in_db]]
        if jobs_to_create:
            sql = 'INSERT INTO movies_job (name) VALUES (%s)'
            cur.executemany(sql, jobs_to_create)

    persons = [person for person, job in credits_list]
    persons = set(persons)
    print("Persons:", persons)

    sql = 'SELECT * FROM movies_person WHERE name IN %s'
    cur.execute(sql, (tuple(persons),))
    persons_in_db = cur.fetchall()

    persons_to_create = [(name,) for name in persons if name not in [name for id, name in persons_in_db]]
    sql = 'INSERT INTO movies_person (name) VALUES  (%s)'
    cur.executemany(sql, persons_to_create) 

    genres = [d['name'] for d in m['genres']] 
    print(genres)

    sql = 'SELECT * FROM movies_genre WHERE name IN %s'

    if genres:
        cur.execute(sql, (tuple(genres),))
    else:
        print("No genres to insert for movie:", m['title'])
        cur.execute(sql, (tuple(['']),))

    genres_in_db = cur.fetchall()

    genres_to_create = [(name,) for name in genres if name not in [name for id, name in genres_in_db]]
    sql = 'INSERT INTO movies_genre (name) VALUES  (%s)'
    cur.executemany(sql, genres_to_create) 

    date_obj = date.fromisoformat(m['release_date']) 
    date_time = datetime.combine(date_obj, datetime.min.time())

    sql = '''INSERT INTO movies_movie 
             (title,
              overview,
              release_date,
              running_time,
              budget,
              tmdb_id,
              revenue,
              poster_path) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'''

    movie_tuple = (m['title'], m['overview'], date_time.astimezone(timezone.utc), m['runtime'], 
                   m['budget'] , movie_id, m['revenue'], m['poster_path'] )
    print(movie_tuple)

    cur.execute(sql, movie_tuple)
    movie_id = cur.fetchone()[0]

    if genres:
        sql = '''INSERT INTO movies_movie_genres (movie_id, genre_id)
                 SELECT %s as movie_id, id as genre_id 
                 FROM movies_genre 
                 WHERE name IN %s'''
        cur.execute(sql, (movie_id, tuple(genres),))
    else:
        print("No genres to insert for movie:", m['title'])

    print(credits_list)
    for credit in credits_list:
        sql = '''INSERT INTO movies_moviecredit (movie_id, person_id, job_id)
                 SELECT %s as movie_id,
                 (SELECT id FROM movies_person WHERE name = %s)  as person_id,
                 (SELECT id FROM movies_job WHERE name = %s)  as job_id'''
        cur.execute(sql, (movie_id, credit[0], credit[1]))

    conn.commit()

if __name__ == "__main__":
    add_movie(int(sys.argv[1]))
