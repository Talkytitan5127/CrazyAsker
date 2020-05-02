from django.core.management.base import BaseCommand

from asker.models import Tag, Question

from faker import Faker
from random import choices, randint

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)
        parser.add_argument('--count_tags_on_question', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        print("Creating tags")
        fake = Faker()
        uniq = set()
        index = 0
        count = options['count']
        count_tags_on_question = options['count_tags_on_question']
        while index < count:
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * index // self.get_10_procent(count)))
            random_int = randint(1000, 10000)
            title = "{}{}".format(fake.word(), random_int)
            if title not in uniq:
                tag = Tag(title=title)
                tag.save()

                question_ids = Question.objects.values_list('question_id', flat=True)
                choose_questions = choices(question_ids, k=count_tags_on_question)

                tag.questions.add(*choose_questions)
                uniq.add(title)
                index += 1

        self.stdout.write(self.style.SUCCESS('successfully added tags'))