n=int(input('ENTER THeR NUMBER'))
# for i in range(1,n+1):
#    for j in range(1,i+1):
#            if j==1 or j==i or i==n:
#                    print("#",end=" ")
#            else:
#                    print(" ",end=" ")
#    print(" ")


for i in range(1,n+1):
    for j in range(1,i):
        print(" ",end=" ")
    for k in range(i,n+1):
        if k == i or k == n or i == 1:
         print("*",end=" ")
        else:
         print(" ",end=" ")
    print(" ")


