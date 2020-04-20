from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from asker.models import Question
from random import choice

from faker import Faker

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        print("Creating questions")
        fake = Faker()
        index = 0
        count = options['count']
        user_ids = User.objects.values_list('id', flat=True)
        while index < count:
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * index // self.get_10_procent(count)))

            question = Question(
                title=fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                text=fake.text(max_nb_chars=200, ext_word_list=None),
                author_id=choice(user_ids)
            )
            question.save()
            index += 1

        self.stdout.write(self.style.SUCCESS('successfully added questions'))
