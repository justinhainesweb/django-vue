import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django

django.setup()

from django.utils import timezone
from dateutil.relativedelta import relativedelta
from configparser import ConfigParser
from random import randint, choice
from project.authjwt.models import User
from project.spa.models import Project, Task, Like

if __name__ == '__main__':

    config = ConfigParser()
    config.read('data.cfg')

    number_of_users = int(config['default']['number_of_users'])
    max_projects_per_user = int(config['default']['max_projects_per_user'])
    max_tasks_per_user = int(config['default']['max_tasks_per_user'])
    max_likes_per_user = int(config['default']['max_likes_per_user'])

    print(f"Got number_of_users: {number_of_users}")
    print(f"Got max_projects_per_user: {max_projects_per_user}")
    print(f"Got max_tasks_per_user: {max_tasks_per_user}")
    print(f"Got max_likes_per_user: {max_likes_per_user}")
    print('Wait...')

    user_ids = []  # store of added user's id

    for i in range(1, number_of_users + 1):
        username = f'django{i:d}{randint(1, 100):d}'
        user = User.objects.create_user(
            email=f'{username}@django.dev',  # djangoN@django.dev
            password='12345678'
        )

        for p in range(1, randint(1, max_projects_per_user + 1)):
            project = Project.objects.create(
                author=user,
                name=f'Project #{p} - {i}'
            )

            for t in range(1, randint(1, max_tasks_per_user + 1)):
                Task.objects.create(
                    project=project,
                    final_date=timezone.now() + relativedelta(months=+1),
                    content='What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.'
                )

        user_ids.append(user.id)

    # Like it!
    for user_id in user_ids:
        copy_ids = user_ids[:]
        copy_ids.pop(0)
        # select tasks that user did not create
        tasks_ids = list(Task.objects.
                         select_related('project').filter(project__author__in=copy_ids).values_list('id', flat=True))
        for i in range(1, randint(1, max_likes_per_user + 1)):
            post_id = choice(tasks_ids)  # get random task
            exists = Like.objects.filter(user_id=user_id, post_id=post_id).exists()
            if not exists:
                Like.objects.create(user_id=user_id, post_id=post_id)

    print('Done')
