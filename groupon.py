total_amount = float(input('Enter Groupon payment amount: '))

tickets = round((total_amount * 0.5875), 2)  # 58.75% for ticket sales
concessions = round((total_amount * 0.4125), 2)  # 41.25% for concession sales

print()
print(f'GL 4005: {tickets}')
print(f'GL 4200: {concessions}')
input('Press enter to exit: ')  # keeps window open
