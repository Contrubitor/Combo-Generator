import string
import random
import os
import random
import json

from tqdm.contrib.concurrent import process_map
import multiprocessing

random.seed = (os.urandom(2048))

namesfile = 'names.json'

email_domains = ['gmail.', 'yahoo.', 'hotmail.', 'aol.', 'outlook.', 'icloud', 'protonmail', 'mail']

domain_end = ['com']

combos = []

class Generator:
    def __init__(self, names, surnames, passwordlist, file, count):
        self.names = names
        self.surnames = surnames
        self.passwordlist = passwordlist
        self.file = file
        self.count = count
        self.combos = []

    def run(self):
        output = process_map(self.combo, range(0, multiprocessing.cpu_count()), max_workers=multiprocessing.cpu_count(), chunksize=1)
        output = [ent for sublist in output for ent in sublist]
        self.combos = output

    def combo(self, x):
        # This Number can max out a Ryzen 1 1600 using all cores with 12.000.000 Combos (-c 12000000) in under 15 Seconds
        combos = []
        for x in range(round(self.count / multiprocessing.cpu_count())):
            name = random.choice(self.names).lower() + random.choice(self.surnames).lower()
            name_extra = ''.join(random.choice(string.digits) for _ in range(random.randint(1, 4)))
            email_domain = random.choice(email_domains) + random.choice(domain_end)
            email = name + name_extra + '@' + email_domain
            password = random.choice(self.passwordlist)
            combo = ('{0}:{1}\n'.format(email, password)).encode()
            combos.append(combo)
        return combos

    def write(self):
        with open(self.file, 'ab') as f:
            f.writelines(self.combos)
        f.close()
        del self.combos[:]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="the output file", default='output.txt')
    parser.add_argument("-c", "--count", help="the amount of combos", default=1000000)
    args = parser.parse_args()
    file = args.output
    count = args.count

    try:
        names = json.loads(open(namesfile, encoding="utf8").read())
        surnames = json.loads(open(namesfile, encoding="utf8").read())
        passwordlist = json.loads(open('passlist.json', encoding="utf8").read())

    except FileNotFoundError:
        print('You are missing the Following Files: names.json or passlist.json')
        exit()

    print('avalible modes: standard(email:pass), email(email)')

    generator = Generator(names, surnames, passwordlist, file, int(count))
    generator.run()
    generator.write()
