import random

random.seed(0)
n = 200
print(n)
for i in range(1, n + 1):
    t = random.randint(1, 1440)
    d = random.randint(1, 60)
    p = random.randint(1, 99)
    print(i, t, d, p)