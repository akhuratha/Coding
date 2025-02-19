from typing import List


class Solution:

    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:

        n = len(grid)

        # sorting lower diagnonal including diagonal in descending order
        for i in range(n):
            start = n - i - 1
            a = [grid[row][row - start] for row in range(start, n)]
            a.sort(reverse=True)
            for row in range(start, n):
                grid[row][row - start] = a[row - start]

        # sorting lower diagnonal including diagonal in descending order
        for j in range(1, n):
            start = j
            a = [grid[col - j][col] for col in range(start, n)]
            a.sort()
            for col in range(start, n):
                grid[col - start][col] = a[col - start]

        return grid

    def assignElements(self, groups: List[int], elements: List[int]) -> List[int]:

        siv = [-1 for i in range(100_000 + 1)]

        for i, e in enumerate(elements):

            if siv[e] != -1:
                continue

            for j in range(e, 100_000 + 1, e):
                if siv[j] == -1:
                    siv[j] = i

        assigned = [siv[gi] for gi in groups]
        return assigned

    def countSubstrings(self, s: str) -> int:

        n = len(s)
        old_memo = [[0 for d in range(D)] for D in range(1, 10)]

        ans = 0

        for i in range(n):

            a = int(s[i])
            new_memo = [[0 for d in range(D)] for D in range(1, 10)]

            for D in range(1, 10):
                a_mod_D = a % D
                new_memo[D - 1][a_mod_D] += 1

                if i == 0:
                    continue

                for d in range(D):
                    cur_d = (10 * d + (a_mod_D)) % D
                    # print(i, D, d, new_memo[D-1][cur_d], old_memo[D-1][d])
                    new_memo[D - 1][cur_d] += old_memo[D - 1][d]

            # print(a)
            # print(old_memo[:1])
            # print(new_memo[:1])

            if a != 0:
                ans += new_memo[a - 1][0]

            old_memo = new_memo
            # print(old_memo[:1])

        return ans

    # TODO: Upsolve https://leetcode.com/problems/maximize-the-minimum-game-score/
