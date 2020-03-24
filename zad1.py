import random
from functools import reduce
from Crypto.Util import number

class LCG:
    def __init__(self, size):
        #self.mod = random.getrandbits(size)
        #self.mod = number.getPrime(size)
        self.mod = pow(2,size)
        self.a = random.randint(2, self.mod-1)
        self.c = random.randint(2, self.mod-1)
        self.x = random.randint(2, self.mod-1)
        self.seed = self.x
        self.values = []

    def next(self):
        next = (self.a * self.x + self.c) % self.mod
        self.values.append(next)
        self.x = next
        return next

    def to_string(self):
        print("modulus:")
        print(self.mod)
        print("a:")
        print(self.a)
        print("c:")
        print(self.c)
        print("x0:")
        print(self.seed)
        print("***\n")


def distinguish(bits = 64, sequence_size = 50):

    good = 0
    total = 1000

    for z in range (total):

        sequence = []
        algo = random.randint(0,1)

        if algo == 0:
            lcg = LCG(bits)
            for j in range(sequence_size):
                sequence.append(lcg.next())
        else:
            for j in range(sequence_size):
                sequence.append(random.getrandbits(bits))

        differences = {}
        multiples = {}

        for i in range(sequence_size-1):    # do przedostatniego włącznie
            
            if i == 0 :
                continue

            differences[i] = sequence[i] - sequence[i-1]
    
            if i < 3:
                continue

            multiples[i-2] = (differences[i-2]*differences[i]) - (differences[i-1] * differences[i-1])  

            approx = abs(reduce(number.GCD, list(multiples.values()) ))

        a = (((sequence[i-1] - sequence[i]) % approx) * number.inverse((sequence[i-2] - sequence[i-1]) % approx, approx)) % approx
        c = (sequence[i-1] - (a * sequence[i-2]) % approx) % approx
        last_guess = (sequence[i] * a + c ) % approx
    
        if last_guess == sequence[-1]:
            guess = 0
        else:
            guess = 1

        if guess == algo:
            good = good + 1
        

    return good/total



print(distinguish(64,100))




'''
def test():
    lcg = LCG(64)
    #lcg.to_string()

    differences = {}
    multiples = {}
    values = {}

    i = 0
    guess = 0

    while True:

        next = lcg.next()

        if abs(guess-next) < 0.1:
            print("Success, in "+str(i)+" trials.")
            return True
            #break

        values[i] = next

        if i == 0 :
            i = i + 1
            continue

        differences[i] = values[i] - values[i-1]

        if i < 3:
            i = i + 1
            continue

        multiples[i-2] = (differences[i-2]*differences[i]) - (differences[i-1] * differences[i-1])  

        approx = abs(reduce(number.GCD, list(multiples.values()) ))

        a = (((values[i-1] - values[i]) % approx) * number.inverse((values[i-2] - values[i-1]) % approx, approx)) % approx
        c = (values[i-1] - (a * values[i-2]) % approx) % approx
        guess = (values[i] * a + c ) % approx

        if i > 100:
            print("too many iterations")
            return False
            #break

        i = i + 1
'''
'''
count = 0
for i in range(1000):
    if test():
        count = count + 1

print(count)

'''



'''

print("\n")
print('modulo:')
print(lcg.mod)
print("guess:")
print(approx)
print(approx / lcg.mod)

print("\n")
print('a:')
print(lcg.a)
print("guess:")
print(a)

print("\n")
print('c:')
print(lcg.c)
print("guess:")
print(c)

print("\n")
print("guess:")
print(guess)
print("next is:")
print(next)
print(guess/next)
'''