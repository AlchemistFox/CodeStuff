import random

def d6():
    return random.randint(1, 6)

def d20():
    return random.randint(1, 20)

def d100():
    return random.randint(1, 100)

def dRoll(n):
    return random.randint(1, n)

def fill_range(start, end):
    return list(range(start, end+1))
