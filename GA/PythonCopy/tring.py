# 草稿

def main():
    a = [0,1,2]
    b = []
    for i in a:
        b.append(i)

    print(a,' ',b)
    a[0] = 222
    print(a,' ',b)

if __name__ == '__main__':
    main()