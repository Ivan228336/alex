# mas_len = int(input())
# mas = [int(x) for x in input().split()]
#
# def func():
#     for i in range(mas_len):
#         for j in range(mas_len - 1):
#             pair_sum = mas[i] + mas[j]
#             other_numbers = [x for x in mas if x!= mas[i] and x!=mas[j]]
#             if all(x == pair_sum for x in other_numbers):
#                 print("YES")
#                 return
#     print("NO")
#
# func()

# import sys
# from collections import Counter
#
#
# def func():
#     input_data = sys.stdin.read().split()
#
#     if not input_data:
#         return
#     mas_len = int(input_data[0])
#     strings = input_data[1:]
#     counts = Counter(strings)
#     max_count = max(counts.values())
#     best_strings = []
#     for word, count in counts.items():
#         if count == max_count:
#             best_strings.append(word)
#
#     best_strings.sort()
#     for word in best_strings:
#         print(word)
#
# func()

# import sys
#
#
# def func():
#     input_data = sys.stdin.read().split()
#
#     if not input_data:
#         return
#
#     n = int(input_data[0])
#     t = int(input_data[1])
#
#     rows_count = [0] * n
#     cols_count = [0] * n
#
#     diag1_count = 0
#     diag2_count = 0
#
#     for i in range(t):
#         cell_num = int(input_data[2 + i]) - 1
#         row = cell_num // n
#         col = cell_num % n
#         rows_count[row] += 1
#         cols_count[col] += 1
#
#         if row == col:
#             diag1_count += 1
#
#         if row + col == n - 1:
#             diag2_count += 1
#
#         if rows_count[row] == n or cols_count[col] == n or diag1_count == n or diag2_count == n:
#             print(i + 1)
#             return
#     print("-1")
#
#
# func()

# import sys
# 
# 
# def func():
#     input_data = sys.stdin.read().split()
#     if not input_data:
#         return
# 
#     n = int(input_data[0])
#     k = int(input_data[1])
# 
#     ans = []
#     left = 1
#     right = n
# 
#     while left <= right:
#         max_inv_for_pos = right - left
# 
#         if k >= max_inv_for_pos:
#             ans.append(right)
#             k -= max_inv_for_pos
#             right -= 1
#         else:
#             target = left + k
#             ans.append(target)
#             for x in range(left, right + 1):
#                 if x != target:
#                     ans.append(x)
# 
#             break
# 
#     sys.stdout.write(" ".join(map(str, ans)) + "\n")
# 
# 
# func()


# import sys
#
# def func():
#     data = list(map(int, sys.stdin.read().split()))
#     if not data:
#         return
#
#     n = data[0]
#     N = 1 << n
#     c = [0] * (N * n)
#     idx = 1
#     for i in range(N):
#         base = i * n
#         for j in range(n):
#             c[base + j] = data[idx]
#             idx += 1
#
#     dp = [0] * N
#
#     for t in range(n):
#         block_size = 1 << t
#         num_pairs = N >> (t + 1)
#         total_blocks = num_pairs * 2
#         if t == 0:
#             max_plus = [0] * total_blocks
#         else:
#             max_plus = [0] * total_blocks
#             t_idx = t - 1
#             for b in range(total_blocks):
#                 start = b * block_size
#                 end = start + block_size
#                 best = -10**30
#                 for i in range(start, end):
#                     val = dp[i] + c[i * n + t_idx]
#                     if val > best:
#                         best = val
#                 max_plus[b] = best
#
#         for pair_idx in range(num_pairs):
#             left_b = pair_idx * 2
#             right_b = left_b + 1
#             maxL = max_plus[left_b]
#             maxR = max_plus[right_b]
#
#             left_start = left_b * block_size
#             left_end = left_start + block_size
#             for i in range(left_start, left_end):
#                 dp[i] += maxR
#
#             right_start = right_b * block_size
#             right_end = right_start + block_size
#             for i in range(right_start, right_end):
#                 dp[i] += maxL
#
#     ans = -10**30
#     for i in range(N):
#         total = dp[i] + c[i * n + (n - 1)]
#         if total > ans:
#             ans = total
#
#     print(ans)
#
# func()

import sys

def func():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    n = next(it)
    q = next(it)

    parent = [None] * 11
    rank = [None] * 11
    for k in range(1, 11):
        parent[k] = list(range(n + 1))
        rank[k] = [0] * (n + 1)

    ans = 0

    for _ in range(n - 1):
        a = next(it)
        b = next(it)
        c = next(it)
        ans += c
        for k in range(c, 11):
            p = parent[k]
            r = rank[k]
            x = a
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            ra = x
            x = b
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            rb = x
            if ra != rb:
                if r[ra] < r[rb]:
                    ra, rb = rb, ra
                p[rb] = ra
                if r[ra] == r[rb]:
                    r[ra] += 1

    out = []
    for _ in range(q):
        u = next(it)
        v = next(it)
        w = next(it)

        max_path = -1
        for k in range(1, 11):
            p = parent[k]
            x = u
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            ru = x
            x = v
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            rv = x
            if ru == rv:
                max_path = k
                break

        if max_path > w:
            ans -= (max_path - w)

        for k in range(w, 11):
            p = parent[k]
            r = rank[k]
            x = u
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            ru = x
            x = v
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            rv = x
            if ru != rv:
                if r[ru] < r[rv]:
                    ru, rv = rv, ru
                p[rv] = ru
                if r[ru] == r[rv]:
                    r[ru] += 1

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

func()