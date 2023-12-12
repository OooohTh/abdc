import math
def approx_e(x, terms):
    val=0
    for i in range(terms):
        val+=(x**i)/(math.factorial(i))
    return val
print(approx_e(int(input()),int(input())))