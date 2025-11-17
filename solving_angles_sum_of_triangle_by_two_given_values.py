import copy
from sympy import Symbol, cos, sin, exp, diff, integrate, limit, solve, oo, pi

'''
# Define symbols
x = Symbol('x')
y = Symbol('y')

y  = 180 - x
print( x + y )
print( type(x+y) )
'''

points = ["A", "B", "C"]

def generate_edges(pnts):
    edges = []
    for i in range(len(pnts)-1):
        for j in range(i+1, len(pnts)):
            edges += [pnts[i]+pnts[j]]
    return edges

print(generate_edges(points))

def generate_triangles(pnts):
    triangles = []
    for i in range(len(pnts)-2):
        for j in range(i+1, len(pnts)-1):
            for z in range(j+1, len(pnts)):
                triangles += [pnts[i]+pnts[j]+pnts[z]]
    return triangles

print(generate_triangles(points))

def generate_angles(triangles):
    angles = []
    for tri in triangles:
        for i in range(len(tri)):
            angles += [tri[i:]+tri[:i]]
    return angles

print(generate_angles(generate_triangles(points)))

def values_of_angles(triangle):
    angles = generate_angles([triangle])
    angles_dict = {}
    for angle in angles:
        if angle not in angles_dict.keys():
            angles_dict[angle] = 0
        else:
            continue
    return angles_dict

print(values_of_angles('ABC'))
    
def verify_axiom_of_triangle(triangle):
    angles = generate_angles([triangle])
    angles_dict = values_of_angles(triangle)
    sum_of_angles = 0
    for angle in angles:
        sum_of_angles += angles_dict[angle]
    return sum_of_angles == 180

print(verify_axiom_of_triangle('ABC'))

'''
d = {'a': 1, 'b': 2, 'c': 3}
d.update({'d': 4, 'e': 5})
print(d)
'''

def solving_values_of_triangle_by_two_given_angles(trian, angl_dic):
    print(sorted(generate_angles(trian)))
    print(sorted(list(angl_dic.keys())))
    assert sorted(generate_angles(trian)) == sorted(list(angl_dic.keys()))
    unknown_angle = ""
    unknown_cnt = 0
    sum_of_known_angle = 0
    for angle in angl_dic.keys():
        if angl_dic[angle] == 0:
            unknown_angle = angle
            unknown_cnt += 1
        else:
            sum_of_known_angle += angl_dic[angle]
    assert unknown_cnt == 1
    assert sum_of_known_angle < 180
    angl_dic_ans = copy.deepcopy(angl_dic)
    angl_dic_ans[unknown_angle] = 180 - sum_of_known_angle
    return angl_dic_ans

print(solving_values_of_triangle_by_two_given_angles(['ABC'], {'ABC':0,'BCA': 99, 'CAB': 10}))
