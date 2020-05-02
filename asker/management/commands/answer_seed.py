from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from asker.models import Question, Answer
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
        bulk_list = []
        count = options['count']
        user_ids = User.objects.values_list('id', flat=True)
        question_ids = Question.objects.values_list('question_id', flat=True)
        while index < count:
            print(index)
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * index // self.get_10_procent(count)))

            for i in range(100):
                is_correct = randint(0, 1)
                answer = Answer(
                    text=fake.text(max_nb_chars=200, ext_word_list=None),
                    author_id=choice(user_ids),
                    question_id=choice(question_ids),
                    is_correct=is_correct
                )
                bulk_list.append(answer)

            Answer.objects.bulk_create(bulk_list)
            index += len(bulk_list)
            bulk_list.clear()

        self.stdout.write(self.style.SUCCESS('successfully added answers'))
