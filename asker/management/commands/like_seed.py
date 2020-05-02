from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from asker.models import Question, Answer, LikeDislike

from faker import Faker
from random import choice, randint


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        vote_type = [1, -1]
        print("Seeding likes")
        fake = Faker()
        index = 0
        count = options['count']
        bulk_list = []
        user_ids = User.objects.values_list('id', flat=True)
        question_ids = Question.objects.values_list('question_id', flat=True)
        answer_ids = Answer.objects.values_list('answer_id', flat=True)
        while index < count:
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * (index // self.get_10_procent(count))))
            q_or_a = randint(0, 1)
            if q_or_a:
                question = Question.objects.get(pk=choice(question_ids))
                question.votes.create(author_id=choice(user_ids), vote=choice(vote_type))
                question._rating = question.count_rating()
                index += 1
            else:
                answer = Answer.objects.get(pk=choice(answer_ids))
                answer.votes.create(author_id=choice(user_ids), vote=choice(vote_type))
                answer._rating = answer.count_rating()
                index += 1


        self.stdout.write(self.style.SUCCESS('successfully added likes'))