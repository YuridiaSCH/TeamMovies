from django.core.management.base import BaseCommand, CommandError
from movies.models import Genre, Movie, Person, Job, MovieCredit

from django.utils.timezone import timezone
from datetime import datetime

class Command(BaseCommand):
    help = "Loads a movie, we assume the database is empty"

    def handle(self, *args, **options):
        jobs = ['Director', 'Producer', 'Actor', 'Voice Actor']
        genres = ['Action', 'Adventure', 'Animation', 'Drama', 'Science Fiction', 'Thriller', 'Musical', 'Fantasy', 'Family']

        for name in genres:
            g = Genre(name=name)
            g.save()

        for job in jobs:
            j = Job(name=job)
            j.save()

        m1 = Movie(title='Tangled',
                   overview='When the kingdoms most wanted and most charming bandit Flynn Rider hides out in a mysterious tower, hes taken hostage by Rapunzel, a beautiful and feisty tower bound teen with 70 feet of magical, golden hair. Flynns curious captor, whos looking for her ticket out of the tower where shes been locked away for years, strikes a deal with the handsome thief and the unlikely duo sets off on an action packed escapade, complete with a super cop horse, an over protective chameleon and a gruff gang of pub thugs.',
                   release_date=datetime(10, 9, 26, tzinfo=timezone.utc),
                   running_time=100,
                   budget=260_000_000,
                   tmdb_id=1,
                   revenue=592_461_732,
                   poster_path='https://www.themoviedb.org/t/p/original/ym7Kst6a4uodryxqbGOxmewF235.jpg')
        m1.save()

        j = Job.objects.get(name='Actor')

        for name in ['Mandy Moore',
                     'Zachary Levi',
                     'Donna Murphi']:
            a = Person.objects.create(name=name)
            MovieCredit.objects.create(person=a, movie=m1, job=j)

        m2 = Movie(title='Me Before You',
                   overview='A small town girl is caught between dead-end jobs. A high-profile, successful man becomes wheelchair bound following an accident. The man decides his life is not worth living until the girl is hired for six months to be his new caretaker. Worlds apart and trapped together by circumstance, the two get off to a rocky start. But the girl becomes determined to prove to the man that life is worth living and as they embark on a series of adventures together, each finds their world changing in ways neither of them could begin to imagine.',
                   release_date=datetime(16, 6, 3, tzinfo=timezone.utc),
                   running_time=110,
                   budget=20_000_000,
                   tmdb_id=2,
                   revenue=207_945_075,
                   poster_path='https://www.themoviedb.org/t/p/w600_and_h900_bestv2/5OGXTUrAA1555hW9VfJO0mrPULf.jpg')
        m2.save()

        for name in ['Emilia Clarke',
                     'Sam Claflin',
                     'Janet McTeer']:
            b = Person.objects.create(name=name)
            MovieCredit.objects.create(person=b, movie=m2, job=j)
