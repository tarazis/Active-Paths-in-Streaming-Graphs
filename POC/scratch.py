import random


def main():
    count = 0
    for i in range(1000000):
        randomNum = random.uniform(0, 1)
        if randomNum <= 0.9:
            count = count + 1

    print(str(count))
    print(str(count / 1000000))



main()