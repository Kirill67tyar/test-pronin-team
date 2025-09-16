import random
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from fees.models import Collect, Payment

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Заполняет БД моковыми данными"

    def handle(self, *args, **options):
        # Количество записей
        NUM_USERS = 100
        NUM_COLLECTS = 500
        NUM_PAYMENTS = 2000

        # Создание пользователей
        users = []
        for _ in range(NUM_USERS):
            username = fake.user_name()
            email = fake.email()
            first_name = fake.file_name()
            last_name = fake.last_name()
            password = fake.password()
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            users.append(user)

        # Создание сборов (Collect)
        collects = []
        for _ in range(NUM_COLLECTS):
            collect = Collect(
                name=fake.sentence(nb_words=3).strip("."),
                author=random.choice(users),
                cause=random.choice(Collect.Cause.choices)[0],
                description=fake.paragraph(nb_sentences=3),
                planned_amount=Decimal(fake.random_number(digits=5, fix_len=True)) / 100,
                image=None,
                closing_to=fake.date_time_between(start_date="-1y", end_date="+30d"),
            )
            collect.created_at = fake.date_time_between(start_date="-1y", end_date="now")
            collect.updated_at = collect.created_at + timedelta(days=random.randint(1, 30))
            if collect.closing_to < collect.created_at:
                collect.closing_to = collect.created_at + timedelta(days=random.randint(1, 60))
            collects.append(collect)

        Collect.objects.bulk_create(collects)

        # Обновляем список сборов
        collects = list(Collect.objects.all())

        # Создание платежей (Payment)
        payments = []
        for _ in range(NUM_PAYMENTS):
            collection = random.choice(collects)
            payment = Payment(
                comment=fake.sentence(nb_words=5).strip("."),
                author=random.choice(users),
                collection=collection,
                amount=Decimal(fake.random_number(digits=3, fix_len=True)) / 100,
            )
            min_date = collection.created_at
            payment.created_at = fake.date_time_between(start_date=min_date, end_date="now")
            payment.updated_at = payment.created_at + timedelta(hours=random.randint(1, 24))
            payments.append(payment)

        Payment.objects.bulk_create(payments)
