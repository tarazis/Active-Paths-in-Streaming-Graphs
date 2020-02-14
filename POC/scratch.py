def main():
    adj = {}
    adj['A'] = {'B': 1, 'E': 1, 'D': 1}
    adj['B'] = {'A': 1}

    del (adj['B']['A'])
    del adj['A']
    print(adj)


main()