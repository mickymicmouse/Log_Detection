# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:21:45 2021

@author: seoun
"""
n=8
k=2
cmd = ["D 2","C","U 3","C","D 4","C","U 2","Z","Z"]

rows = len(cmd)
answer = ["O"]*n
cut_list = []

for op in range(len(cmd)):
    operation = cmd[op].split(" ")
    if len(operation)==2:
        # 이동 명령어
        if operation[0]=="U":
            #상위 이동
            moving = int(operation[1])
            point = k
            while True:
                point = point-1
                if answer[point]=="O":
                    moving-=1
                
                if moving == 0:
                    k=point
                    break
            
        else:
            # 하위 이동
            moving = int(operation[1])
            point = k
            while True:
                point = point+1
                if answer[point]=="O":
                    moving-=1
                
                if moving == 0:
                    k=point
                    break
    else:
        # 삭제 혹은 복구 명령어
        if operation[0]=="C":
            #삭제
            cut_list.append(k)
            answer[k]="X"
            
            # 현재 위치에 따라 다음 포인트 설정
            if k==n-1:
                # 마지막일 경우 위로 한칸 이동
                moving = 1
                point = k
                while True:
                    point = point-1
                    if answer[point]=="O":
                        moving-=1
                    if moving == 0:
                        k=point
                        break
            else:
                # 아래로 한칸 이동
                moving = 1
                point = k
                while True:
                    point = point+1
                    if answer[point]=="O":
                        moving-=1
                    if moving == 0:
                        k=point
                        break
            n-=1
            
        else:
            #복구
            p = cut_list.pop()
            answer[p]="O"
            n+=1
    print(answer)
    print(k)
    
result = ""
for i in answer:
    result+=i
return result