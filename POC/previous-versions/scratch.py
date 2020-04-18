'''
Scratch python app for testing
'''
import random


def main():
    # count = 0
    # maxLoop = 100
    # maxInt = 1000
    # for i in range(maxLoop):
    #     alpha = 0.90
    #     num = random.randint(1, maxInt)
    #     print (str(num))
    #     alphaProbability = alpha * maxInt
    #     if num <= alphaProbability:
    #         # return True
    #         print("keep going")
    #         count = count + 1
    #     elif num > alphaProbability and num <= maxInt:
    #         # return False
    #         break
    #
    # print("looped " + str(count) + " time(s)")

    a = 7
    b = 59457693
    p = 118915387
    d = pow(a, b, p)

    i = 0

    while True:
        print("a = " + str(a) + "b = " + str(b) + "p= " + str(p))
        d = pow(a,b,p)
        print(str(d))
        if d == 1 or d == -1:
            break

        a = d
        b = 2

        i = i + 1


    #

main()