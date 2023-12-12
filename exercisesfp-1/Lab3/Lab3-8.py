def get_data(prompt):
    print(prompt)
    inputV=int(input())
    return inputV

def main():
    print('Prime factorization')
    n=get_data('Input number')
    result=''
    for i in range(2,n):
        Exponent_counter=0
        while n%i==0:
            n=n/i
            Exponent_counter+=1
        if Exponent_counter!=0:
            result+=str(i)+' ** '+str(Exponent_counter)+'\n'
    print (result)

main()