import os
from django.core.management.base import BaseCommand
from random import randint, choice
from configparser import ConfigParser
from project.authjwt.models import User
from project.spa.models import Project, Task, Like
from project.settings import BASE_DIR


class Command(BaseCommand):
    """ This command was created to insert users and others seed records into database """

    help = "Insert seed data into database"

    def handle(self, *args, **options):

        self.stdout.write("Cleaning database...")
        User.objects.all().delete()
        Project.objects.all().delete()
        Task.objects.all().delete()
        Like.objects.all().delete()

        config = ConfigParser()
        config.read(os.path.join(BASE_DIR, 'load_data.cfg'))

        number_of_users = int(config['seed']['number_of_users'])
        max_projects_per_user = int(config['seed']['max_projects_per_user'])
        max_tasks_per_user = int(config['seed']['max_tasks_per_user'])
        max_likes_per_user = int(config['seed']['max_likes_per_user'])

        self.stdout.write(f"Got number_of_users: {number_of_users}")
        self.stdout.write(f"Got max_projects_per_user: {max_projects_per_user}")
        self.stdout.write(f"Got max_tasks_per_user: {max_tasks_per_user}")
        self.stdout.write(f"Got max_likes_per_user: {max_likes_per_user}")
        self.stdout.write('Wait...')

        user_ids = []  # array of added users id

        for i in range(0, number_of_users):
            user = User.objects.create_user(
                email=f'django' + (str(i) if i > 0 else '') + '@django.dev',  # django[N]@django.dev
                password='12345678'
            )

            for p in range(1, max_projects_per_user + 1):
                project = Project.objects.create(
                    author=user,
                    name=f'Project #{p} - {i}',
                    shared=True if randint(1, 101) % 2 == 0 else False
                )

                tasks = []
                for t in range(1, max_tasks_per_user + 1):
                    tasks.append(Task(project=project))
                Task.objects.bulk_create(tasks)

            user_ids.append(user.id)

        # Like it!
        for user_id in user_ids:
            copy_ids = user_ids[:]
            copy_ids.pop(0)

            # select tasks that user did not create
            tasks_ids = list(
                Task.objects.select_related('project').filter(project__author__in=copy_ids).values_list('id', flat=True)
            )

            for i in range(1, randint(1, max_likes_per_user + 1)):
                task_id = choice(tasks_ids)  # get random task
                exists = Like.objects.filter(user_id=user_id, task_id=task_id).exists()
                if not exists:
                    Like.objects.create(user_id=user_id, task_id=task_id)

        self.stdout.write(
            self.style.SUCCESS(f'Done. Created '
                               f'{User.objects.count()} users, '
                               f'{Project.objects.count()} projects, '
                               f'{Task.objects.count()} tasks.')
        )
