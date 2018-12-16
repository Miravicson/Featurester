from builtins import sorted

unsorted_list = [1]

num_ins = 1

num_greater = sorted(list(filter(lambda f: f >= num_ins, unsorted_list)))
print(num_greater)
num_less = sorted(list(filter(lambda f: f < num_ins, unsorted_list)))
num_less.append(num_ins)
print(num_less)

res = []

for idx in range(0, len(num_greater)):
    if idx == 0:
        if num_greater[idx] == num_ins:
            res.append(num_ins + 1)
        else:
            res.append(num_greater[idx])
    elif num_greater[idx] == res[-1]:
        res.append(num_greater[idx] + 1)
    else:
        res.append(num_greater[idx])

print(res)


final = num_less + res
print(final)
