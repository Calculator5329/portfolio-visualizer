
def arrange_arr(arr, vals):
    return [x for _, x in sorted(zip(vals, arr))]

arr = ["fun", "bot", "pro"]
vals = [1, 3, 2]

print(arrange_arr(arr, vals))