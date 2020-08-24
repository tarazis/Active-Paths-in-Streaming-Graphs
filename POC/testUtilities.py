import random
from random import choice

alpha = 0.95


# Generate a probability value based on a given alpha
# Choose a number uniformly at random from 1, 100 inclusive.
# If number is less than or equal alpha * 100, return true. Else, false
def generateProbability():
    maxInt = 100
    num = random.randint(1, maxInt)
    alphaProbability = alpha * maxInt

    if num <= alphaProbability:
        return True
    elif num > alphaProbability or num <= maxInt:
        return False


def main():
    truths = 0
    falsies = 0
    for x in range(100):
        probability = generateProbability()
        if probability is True:
            truths = truths + 1
        else:
            break

    print(str(truths))
    print(str(falsies))


main()