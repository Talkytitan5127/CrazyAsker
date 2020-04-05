from django.core.management.base import BaseCommand

from asker.models import User, Question, Answer
from random import choice, randint

from faker import Faker

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        print("Creating answers")
        fake = Faker()
        index = 0
        count = options['count']
        while index < count:
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * index // self.get_10_procent(count)))

            user_ids = User.objects.values_list('id', flat=True)
            question_ids = Question.manager.values_list('question_id', flat=True)
            is_correct = randint(0, 1)
            answer = Answer(
                text=fake.text(max_nb_chars=200, ext_word_list=None),
                author_id=choice(user_ids),
                question_id=choice(question_ids),
                is_correct=is_correct
            )
            answer.save()
            index += 1

        self.stdout.write(self.style.SUCCESS('successfully added answers'))
