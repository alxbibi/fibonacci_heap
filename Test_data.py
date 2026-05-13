import json
import random


lst = [random.randint(-10000, 10000) for _ in range(10000)]

with open('Data.json', 'w') as f:
    json.dump(lst, f)



