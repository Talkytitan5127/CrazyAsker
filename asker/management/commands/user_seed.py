from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int)

    def get_10_procent(self, number):
        return number // 10

    def handle(self, *args, **options):
        print("Creating users")
        fake = Faker()
        uniq = set()
        index = 0
        count = options['count']
        while index < count:
            if not (index % self.get_10_procent(count)):
                print("Done {}%".format(10 * (index // self.get_10_procent(count))))
            profile = fake.profile()

            username = profile['username']
            if username not in uniq:
                user = User.objects.create_user(
                    username=username,
                    password=profile['mail'],
                    email=profile['mail']
                )

                user.profile_set.create()

                uniq.add(username)
                index += 1

        self.stdout.write(self.style.SUCCESS('successfully added users'))