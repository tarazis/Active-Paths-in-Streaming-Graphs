import random


def main():
    count = 0
    maxLoop = 100
    maxInt = 1000
    for i in range(maxLoop):
        alpha = 0.90
        num = random.randint(1, maxInt)
        print (str(num))
        alphaProbability = alpha * maxInt
        if num <= alphaProbability:
            # return True
            print("keep going")
            count = count + 1
        elif num > alphaProbability and num <= maxInt:
            # return False
            break

    print("looped " + str(count) + " time(s)")



main()