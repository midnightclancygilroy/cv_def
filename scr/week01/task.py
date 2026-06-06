

# def num_to(n):
#     ret = 0
#     while n > 0:
#         ret = ret + n
#         n = n - 1
#     return ret

# sum = num_to(5)
# print(sum)

# def is_motion(diff_value, threshold):
#     if diff_value > threshold:
#         return True
#     else:
#         return False
    
# print(is_motion(5, 15))

# def read_dif():
#     n = 0
#     while True:
#         value = int(input())
#         if value > 25:
#             n = n + 1
#         elif value == 0:
#             print(n)
#             break


# read_dif()


# def filter_contours(areas, min_area):
#     result = []
#     for area in areas:
#         if area > min_area:
#             result.append(area)
#     return result        

# print(filter_contours([300, 1200, 500, 2000], 800))

def differences(numbers): 
    result = []
    n = 0
    for element in numbers:
        if n == 0:
            prev_elemant = element
            n = n + 1
        elif prev_elemant:
            result.append(element - prev_elemant)
            prev_elemant = element
    return result

print(differences([10, 15, 13, 20]))