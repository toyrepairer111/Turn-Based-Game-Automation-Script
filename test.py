import random

if __name__ == '__main__':
     arry_randon = []
     for i in range(10):
         arry_randon.append(random.randint(1,10))
     print('待排序数组',arry_randon)
     for i in range(len(arry_randon)):
         swap_status = False
         for j in range(len(arry_randon)-1-i):
             if arry_randon[j] > arry_randon[j+1]:
                 arry_randon[j],arry_randon[j+1] = arry_randon[j+1],arry_randon[j]
                 swap_status = True
         if not swap_status:
             print('已排好序，提前结束')
             break

     print('已排序好数组',arry_randon)


