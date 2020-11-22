from faker import Faker
from faker.providers import misc

f = Faker()
Faker.seed(63)

for _ in range(15):
    print(f.name())
