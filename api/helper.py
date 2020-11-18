import uuid
import random
from faker import Faker
fake = Faker()


def get_data():
    data = list()
    for _ in range(10):
        data.append({'userId': str(uuid.uuid4()), 'id': str(random.randrange(1, 100)), 'name': fake.name(), 'address':
            fake.address()})
    for d in data:
        yield d


def get_schd_time():
    return random.randrange(5,20)


if __name__ == '__main__':
    print(next(get_data()))