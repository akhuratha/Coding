from typing import List


class Solution:

    def sumOfGoodNumbers(self, nums: List[int], k: int) -> int:
        ans = 0
        n = len(nums)
        for i, val in enumerate(nums):

            if (
                    (i - k < 0 or nums[i-k] < val)
                    and (n <= i + k or nums[i+k] < val)
            ):
                ans += val

        return ans

    def separateSquares(self, squares: List[List[int]]) -> float:

        # (y, w, {start=True,end=False})
        triplets = []
        total_area = 0
        tol = 1e-5

        for (x, y, l) in squares:
            total_area += l * l
            triplets.append((y, l, True))
            triplets.append((y + l, l, False))

        triplets.sort(key=lambda t: t[0])
        # print(triplets)

        prev_y, running_w, _ = triplets[0]
        cur_area = 0
        half_area = total_area / 2

        for (y, w, is_start) in triplets[1:]:
            # print(cur_area, half_area, prev_y, y, running_w, w, is_start)

            area_gain = (y - prev_y) * running_w
            # print("area gain: ", area_gain)

            if cur_area + area_gain >= half_area:
                dy = (half_area - cur_area) / running_w
                return prev_y + dy

            cur_area += area_gain

            if is_start:
                running_w += w
            else:
                running_w -= w
            prev_y = y

        return 0.0

    def separateSquares2(self, squares):
        # TODO: Upsolve https://leetcode.com/problems/separate-squares-ii/description/
        pass

    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # p = remove * from p
        # is p a subsequence of s?

        def rk_hash_prefix_finder(s, sub_string, base=31, mod=10 ** 9 + 7):
            # TODO: Write the Rabin Karp Algo yourself. This is from chatGPT
            n = len(s)
            m = len(sub_string)
            # print(s, sub_string)

            if m > n:
                # sub_string cannot be a suffix of s[:i] if it's longer
                return [0] * n
            elif m == 0:
                return list(range(n))

            # Define the base and modulus for the hash function
            base = 257  # A prime number larger than the character set (this helps in reducing hash collisions)
            modulus = 10 ** 9 + 7  # A large prime modulus to reduce hash collisions

            # Precompute the hash for the substring `sub_string`
            sub_hash = 0
            for i in range(m):
                sub_hash = (sub_hash * base + ord(sub_string[i])) % modulus

            # Precompute the hash of the first `m` characters of `s`
            curr_hash = 0
            for i in range(m):
                curr_hash = (curr_hash * base + ord(s[i])) % modulus

            # This is the base^m % modulus, used to remove the leading character from the rolling hash
            base_m = pow(base, m, modulus)

            result = [0] * (m - 1)

            # Check from s[m-1] to s[n-1], i.e., check every suffix
            for i in range(m - 1, n):
                if curr_hash == sub_hash:
                    result.append(1)
                else:
                    result.append(0)

                # Roll the hash for the next substring: remove the leftmost character, add the new rightmost character
                if i + 1 < n:
                    curr_hash = (curr_hash * base - ord(s[i - m + 1]) * base_m + ord(s[i + 1])) % modulus
                    curr_hash = (curr_hash + modulus) % modulus  # To ensure positive modulus

            # print(sub_string, result)

            result[0] = 0 if result[0] == 1 else -1
            for i in range(1, n):
                if result[i] == 1:
                    result[i] = i
                else:
                    result[i] = result[i - 1]

            # print(sub_string, result)

            return result

        n = len(s)
        x, y, z = p.split("*")

        X = rk_hash_prefix_finder(s, x)
        Y = rk_hash_prefix_finder(s, y)
        Z = rk_hash_prefix_finder(s, z)

        # print(x, X)
        # print(y, Y)
        # print(z, Z)

        ans = -1

        for i in range(n):
            if Z[i] != -1:
                j = Z[i] - len(z)
                if 0 <= j < n and Y[j] != -1:
                    k = Y[j] - len(y)
                    if 0 <= k < n and X[k] != -1:
                        cur_len = Z[i] - (X[k] - len(x) + 1) + 1
                        ans = min(ans, cur_len) if ans != -1 else cur_len

        return ans
