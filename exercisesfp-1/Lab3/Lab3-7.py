def get_data(prompt):
    print(prompt)
    inputV=int((input()))
    return inputV

def main():
    print('Welcome to Collatz series:')
    C0=get_data('Input Collatz Series number')
    Cn=C0
    steps=0
    while Cn!=1:
        if Cn%2==0:
            Cn=Cn//2
        elif Cn%2!=0:
            Cn=3*Cn+1
        steps+=1
    print(C0,'\t',steps)

main()
