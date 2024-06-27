import string

# 1. wget https://standards-oui.ieee.org/oui/oui.txt > oui.txt
# 2. cat oui.txt | grep 'base 16' > ouis, then:
# 3. cat oui.txt | grep 'base 16' > ouis, then:
if __name__ == '__main__':
    with open('ouis') as fd:
        s = fd.read().splitlines()
    m = ['vendors = {']
    while s:
        line = s.pop().split()
        v = line[3]
        if v in {'China'}:
            v += ' ' + line[4]
        while v[-1] in string.punctuation:
            v = v[:-1]
        m.append('"%s": "%s",' % (line[0], v))  # 🟥 some have "'" -> use "
    m.append('}')
    with open('vendors-new.py', 'w') as fd:
        fd.write('\n'.join(m))
    print('written: vendors-new.py. check and overwrite vendors.py')
