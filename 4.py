# -*- coding: utf-8 -*-
"""
Created on Sat May  8 16:31:03 2021

@author: seoun
"""

from collections import deque


n=4
start=1
end=4
roads = [[1, 2, 1], [3, 2, 1], [2, 4, 1]]
traps = [2,3]

from collections import deque

road_dict[2]=[(1,2),(3,4)]
for key,value in road_dict.items():
    print(value)



q.append(())
print(q)
def check(start, end, traps, road_dict, n):
    visit = [-1]*(n+1)
    q=deque()
    result = 0
    visit[start] = 0
    road_list = road_dict
    q.append((start, road_list))
    flag = True
    while q:
        p, road_list = q.popleft()
        # p 가 트랩일 경우
        if p in traps:
            print(p)
            new_road_list = dict()
            for i in range(1,n+1):
                new_road_list[i]=[]
            
            for value in road_list.pop(p):
                for i in value: 
                    new_road_list[i[0]].append((p,i[1]))
            for key, value in road_list.items():
                for i in value:
                    print(i)
                    if i[0]==p:
                        new_road_list[i[0]].append((key, i[1]))
                    else:
                        new_road_list[key].append(i)
            print(new_road_list)
            road_list = new_road_list
        for dx,c in road_list[p]:
            # 가는데 걸리는 비용 visit 리스트
            visit[dx] = visit[p]+c
            print(visit)
            q.append((dx, road_list))
            if dx == end:
                result = visit[end]
                flag = False
                break
        if flag == False:
            break
    return result
                 
def solution(n, start, end, roads, traps):
    
    answer = 0
    road_dict = dict()
    for i in range(1,n+1):
        road_dict[i]=[]
    for s,e,c in roads:
        road_dict[s].append((e,c))
    answer = check(start, end, traps, road_dict, n)
    print(road_dict)
    return answer