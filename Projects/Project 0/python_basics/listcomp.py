nums = [1, 2, 3, 4, 5, 6]
strings = ['Salutations', 'WORLD', 'MERLIN', 'BeiFeng']
oddNums = [x for x in nums if x % 2 == 1]
print(oddNums)
oddNumsPlusOne = [x + 1 for x in nums if x % 2 == 1]
print(oddNumsPlusOne)
lower = [x.lower() for x in strings if len(x) > 5]
print(lower)
