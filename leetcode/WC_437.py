from typing import List


class Solution:

    def hasSpecialSubstring(self, s: str, k: int) -> bool:

        n = len(s)

        if n == 1:
            return True

        prev_char = s[0]
        counter = 1

        for i in range(1, n):
            cur_char = s[i]

            if cur_char == prev_char:
                counter += 1
            else:
                if counter == k:
                    return True

                counter = 1
                prev_char = cur_char

        if counter == k:
            return True

        return False

    def maxWeight(self, pizzas: List[int]) -> int:
        pizzas.sort()

        n = len(pizzas)
        r = n - 1
        days = n // 4
        odd_days = days // 2 + (days % 2 == 1)
        even_days = days // 2

        weight_gained = 0
        while odd_days > 0:
            weight_gained += pizzas[r]
            odd_days -= 1
            r -= 1

        while even_days > 0:
            weight_gained += pizzas[r - 1]
            even_days -= 1
            r -= 2

        return weight_gained

    def maxSubstringLength(self, s: str, k: int) -> bool:

        n = len(s)

        class CharConfig:
            def __init__(self, i, char):
                self.start = i
                self.end = i
                self.char = char
                self.counted = False

            def set_ending(self, i):
                self.end = i

        char_config_mapping = {}

        for i, char in enumerate(s):
            if char not in char_config_mapping:
                char_config_mapping[char] = CharConfig(i, char)
            else:
                char_config_mapping[char].set_ending(i)

        char_configs = list(char_config_mapping.values())
        char_config_pairs = [(cc_1, cc_2)
                             for cc_2 in char_configs
                             for cc_1 in char_configs
                             if cc_1.start <= cc_2.start]

        # print(len(char_config_pairs))
        # print([(cct[0].char, cct[1].char) for cct in char_config_pairs])

        def sort_key(x: tuple[CharConfig, CharConfig]):
            start = x[0].start
            end = max(x[0].end, x[1].end)

            return end - start + 1

        char_config_pairs.sort(key=sort_key)
        # print([(cct[0].char, cct[1].char) for cct in char_config_pairs])

        count = 0
        for char_config_1, char_config_2 in char_config_pairs:
            # print(char_config_1.char, char_config_2.char)

            if char_config_1.counted or char_config_2.counted:
                continue

            disjoint_flag = True

            start = char_config_1.start
            end = max(char_config_1.end, char_config_2.end)

            for i in range(start, end + 1):
                cur_char_config = char_config_mapping[s[i]]
                if cur_char_config.counted or not (
                        start <= cur_char_config.start
                        and cur_char_config.end <= end
                ):
                    # print(s[i])
                    disjoint_flag = False
                    break

            if (
                    disjoint_flag
                    and not (start == 0 and end == n - 1)
            ):
                count += 1
                for i in range(start, end + 1):
                    char_config_mapping[s[i]].counted = True

            # print(char_config_1.char, char_config_2.char)
            # print("count: ", count)

        return count >= k

    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:

        m = len(grid)
        n = len(grid[0])

        memo = [[dict() for j in range(n)] for i in range(m)]
        allowed_transitions = {
            1: 2,
            2: 0,
            0: 2
        }

        def run_dfs(i: int, j: int, di: int, dj: int, turned: bool) -> int:

            if ((di, dj, turned)) in memo[i][j]:
                return memo[i][j][(di, dj, turned)]

            max_depth = 1

            children = [(di, dj, turned)]
            if not turned:
                children.append((dj, -di, True))

            for (cur_di, cur_dj, cur_turned) in children:
                u = i + cur_di
                v = j + cur_dj

                if not (
                        (0 <= u < m and 0 <= v < n)
                        and (grid[u][v] == allowed_transitions[grid[i][j]])
                ):
                    continue

                max_depth = max(max_depth, 1 + run_dfs(i=i + cur_di,
                                                       j=j + cur_dj,
                                                       di=cur_di,
                                                       dj=cur_dj,
                                                       turned=cur_turned))

            memo[i][j][(di, dj, turned)] = max_depth

            return max_depth

        max_depth = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue

                for di in [-1, 1]:
                    for dj in [-1, 1]:
                        max_depth = max(max_depth, run_dfs(i, j, di, dj,
                                                           turned=False))

        return max_depth
