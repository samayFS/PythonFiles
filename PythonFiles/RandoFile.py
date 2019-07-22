# import random
# stringfile={'TAKLI','MURGI'}
# word=list(stringfile)
# random.shuffle(word)
# y=''.join(word)
# print(y)

# import random
# def mixup(word):
#     as_list_of_letters = list(word)
#     random.shuffle(as_list_of_letters)
#     return ''.join(as_list_of_letters)
# l=['TAKLI','MURGI']
# map(mixup, l)



import random

words = ['HELLO','WORLD']
words = [''.join(random.sample(word, len(word))) for word in words]
print(words)
