from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from datetime import date
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):

        # Use PyMongo to clear collections directly (avoids Djongo ORM delete issues)
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['leaderboard'].delete_many({})
        db['activities'].delete_many({})
        db['users'].delete_many({})
        db['teams'].delete_many({})
        db['workouts'].delete_many({})

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc),
        ]

        # Create Workouts
        workouts = [
            Workout.objects.create(name='Super Strength', description='Strength training for heroes', suggested_for='Marvel'),
            Workout.objects.create(name='Stealth Moves', description='Stealth and agility training', suggested_for='DC'),
        ]

        # Create Activities
        Activity.objects.create(user=users[0], type='Web Swinging', duration=30, date=date.today())
        Activity.objects.create(user=users[1], type='Suit Up', duration=45, date=date.today())
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=40, date=date.today())
        Activity.objects.create(user=users[3], type='Gadget Training', duration=50, date=date.today())

        # Create Leaderboard
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=95)
        Leaderboard.objects.create(user=users[3], score=85)

        # Ensure unique index on email
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
