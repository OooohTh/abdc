def get_data(prompt):
    print(prompt)
    inputV=(input())
    return inputV

def get_operation_message_key():
    return_list=[]
    return_list.append(get_data('Input your desired message'))
    return_list.append(get_data('Input your desired operation, EN for encode, DE for decode'))
    return_list.append(int(get_data('Input your desired key')))
    return return_list

def encode(message, key):
    print('Encoding your message...')
    ascii_list=[]
    final_message=''
    for i in range(len(message)):
        char=message[i]
        ascii_list.append(ord(char))
        ascii_list[i]+=key
        final_message+=chr(ascii_list[i])
    return final_message

def decode(message, key):
    print('Decoding your message...')
    ascii_list=[]
    final_message=''
    for i in range(len(message)):
        char=message[i]
        ascii_list.append(ord(char))
        ascii_list[i]-=key
        final_message+=chr(ascii_list[i])
    return final_message

def main():
    print('Welcome to encoder and decoder:')
    while True:
        cmdargs=get_operation_message_key()
        if cmdargs[1]=='EN':
            result=encode(cmdargs[0],cmdargs[2])
            break
        elif cmdargs[1]=='DE':
            result=decode(cmdargs[0],cmdargs[2])
            break
        else:
            print('Something was wrong with your message, try again')
    print ('Your final message is:'+result)

main()


