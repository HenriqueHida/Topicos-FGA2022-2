dictHW = {}
dictVM = {}
n = int(input())
for i in range(n):
    nomeH, ramH, cpuH = input().split()
    dictHW[nomeH] = [ramH, cpuH]

m = int(input())
for j in range(m):
    nomeV, ramV, cpuV = input().split()
    dictVM[nomeV] = [ramV, cpuV]

print(dictHW, dictVM)
