str1 = list(input())
str2 = list(input())
dp = [[0]*(len(str1)+1) for _ in range(len(str2)+1)]
for i in range(len(str1)):
    for j in range(len(str2)):
        if str1[i] == str2[j]:
            dp[j+1][i+1] = dp[j][i]+1
        else:
            dp[j+1][i+1] = max(dp[j][i+1],dp[j+1][i])
print(dp[-1][-1])
