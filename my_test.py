import os

def MyTrim_line(inputstr):
    i1 = 0
    i2 = len(inputstr)-1
    restr = inputstr
  
    for i in range(len(inputstr)):
        if inputstr[i] == ' ':
            i1 = i
        else: 
            break

    for i in range(len(inputstr)):
        if inputstr[len(inputstr)-i-1] == ' ':
            i2 = len(inputstr)-i-1
        else:
            break 

    restr = inputstr[i1+1:i2]

    return restr

def trim_multiline(input):
    res = ''
    newline_list = []
    cur_s = 0
    first_line = True

    for i in range(len(input)):
        if input[i] == '\n':
            if not first_line:
                res += '\n'
            res += MyTrim_line(input[cur_s:i])
            cur_s = i + 1
            first_line = False

    if cur_s < len(input):
        res += '\n'
        res += MyTrim_line(input[cur_s:len(input)])   

    return res



if __name__ == '__main__':
    print(f'start...')
    strr = '   heee ooo    \n     yo oo \n 88 99 \n 000000 11     \nhey '
    print(f'//{strr}//')
    print(f'//{trim_multiline(strr)}//')