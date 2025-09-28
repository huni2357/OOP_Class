import math
import re


########################################################
# TODO: MUST REPLACE THIS WITH YOUR STUDENT ID
student_id = "2025150048"  # Replace with your student ID
########################################################

class RepeatingDecimal:
    # TODO: IMPLEMENT THIS CONSTRUCTOR (Place for definition)
    def __init__(self, sign, int_part, non_repeat, repeat):
        """
        Initializes a RepeatingDecimal object.
        (sign) int_part.non_repeat[repeat]
        """
        # TODO: IMPLEMENT THE BODY OF THE CONSTRUCTOR (Probably < 10 lines of code)
        self.__sign = 1 if sign >= 0 else -1
        self.__int_part = int(int_part)
        self.__non_repeat = [int(d) for d in (non_repeat or [])]
        self.__repeat = [int(d) for d in (repeat or [])]
        self.cleanup()

    @classmethod
    def fromString(cls, s):
        """
        Creates a RepeatingDecimal object from string "±int.non[rep]".
        """
        pattern = r'^([+-]?)(\d+)(?:\.(\d*?))?(?:\[(\d+)\])?$'
        match = re.fullmatch(pattern, s.strip())
        if not match:
            raise ValueError(f"Invalid repeating-decimal string: {s}")

        sign_str, int_part, non_repeat, repeat = match.groups()
        sign = -1 if sign_str == '-' else 1
        int_part = int(int_part)
        non_repeat = [int(d) for d in (non_repeat or "")]
        repeat = [int(d) for d in (repeat or "")]
        return cls(sign, int_part, non_repeat, repeat)


    @staticmethod
    def __lcm(a, b):
        if a == 0:
            return b
        if b == 0:
            return a
        return abs(a // math.gcd(a, b) * b)

    @staticmethod
    def __shortest_period(digits):
        n = len(digits)
        if n <= 1:
            return digits[:]
        
        lps = [0] * n
        j = 0
        for i in range(1, n):
            while j and digits[i] != digits[j]:
                j = lps[j - 1]
            if digits[i] == digits[j]:
                j += 1
                lps[i] = j
        p = n - lps[-1]
        return digits[:p] if p < n and n % p == 0 else digits[:]

    @staticmethod
    """
    Idea for this part(expand window, add frac digits and fold back),
    but some parts(why the code i wrote didnt go right / which parts to rewrite)
    of this function was helped by LLM
    """
    def __expand_window(int_part, non_repeat, repeat, k_target, L_target, extra=1):
        non = list(non_repeat or [])
        if len(non) < k_target:
            need = k_target - len(non)
            if repeat:
                repeat_times = (need + len(repeat) - 1) // len(repeat)
                non += (repeat * repeat_times)[:need]
            else:
                non += [0] * need

        frac_digits = non[:]
        if L_target:
            if repeat:
                repeat_times = (L_target + len(repeat) - 1) // len(repeat)
                period_block = (repeat * repeat_times)[:L_target]
            else:
                period_block = [0] * L_target
            frac_digits += period_block * (1 + extra)
        return int_part, frac_digits

    @staticmethod
    def __add_frac_digits(left_ip, left_frac, right_ip, right_frac, op=+1):

        max_len = max(len(left_frac), len(right_frac))
        left_frac += [0] * (max_len - len(left_frac))
        right_frac += [0] * (max_len - len(right_frac))

        carry = 0
        result_frac = [0] * max_len
        for idx in range(max_len - 1, -1, -1):
            s = left_frac[idx] + op * right_frac[idx] + carry
            if s >= 0:
                result_frac[idx] = s % 10
                carry = s // 10
            else:
                borrow_units = (-s + 9) // 10
                result_frac[idx] = s + 10 * borrow_units
                carry = -borrow_units

        result_ip = left_ip + op * right_ip + carry
        return result_ip, result_frac

    @staticmethod
    def __fold_back(int_part, frac_digits, k_target, L_target):

        if len(frac_digits) <= k_target:
            return int_part, frac_digits[:], []
        non_repeat = frac_digits[:k_target]
        tail_digits = frac_digits[k_target:]

        if L_target == 0:
            return int_part, frac_digits[:], []
        repeat_block = tail_digits[:L_target]
        return int_part, non_repeat, repeat_block

    def cleanup(self):
        # non_repeat: carry/borrow
        for idx in range(len(self.__non_repeat) - 1, -1, -1):
            digit = self.__non_repeat[idx]
            if digit >= 10:
                q, r = divmod(digit, 10)
                self.__non_repeat[idx] = r
                if idx > 0:
                    self.__non_repeat[idx - 1] += q
                else:
                    self.__int_part += q
            elif digit < 0:
                borrow_units = (-digit + 9) // 10
                self.__non_repeat[idx] = digit + 10 * borrow_units
                if idx > 0:
                    self.__non_repeat[idx - 1] -= borrow_units
                else:
                    self.__int_part -= borrow_units

        # repeat: carry/borrow
        for idx in range(len(self.__repeat) - 1, -1, -1):
            digit = self.__repeat[idx]
            if digit >= 10:
                q, r = divmod(digit, 10)
                self.__repeat[idx] = r
                if idx > 0:
                    self.__repeat[idx - 1] += q
                else:
                    if self.__non_repeat:
                        self.__non_repeat[-1] += q
                    else:
                        self.__int_part += q
            elif digit < 0:
                borrow_units = (-digit + 9) // 10
                self.__repeat[idx] = digit + 10 * borrow_units
                if idx > 0:
                    self.__repeat[idx - 1] -= borrow_units
                else:
                    if self.__non_repeat:
                        self.__non_repeat[-1] -= borrow_units
                    else:
                        self.__int_part -= borrow_units

        # special cycles -- Used LLM for this part. 
        if self.__repeat and all(x == 9 for x in self.__repeat):
            carry = 1
            i = len(self.__non_repeat) - 1
            while i >= 0 and carry:
                s = self.__non_repeat[i] + carry
                self.__non_repeat[i] = s % 10
                carry = s // 10
                i -= 1
            self.__int_part += carry
            self.__repeat = []
        elif self.__repeat and all(x == 0 for x in self.__repeat):
            self.__repeat = []

        # 최소 주기화
        if self.__repeat:
            self.__repeat = self.__shortest_period(self.__repeat)

        # 반복 없으면 끝의 0 제거
        if not self.__repeat:
            while self.__non_repeat and self.__non_repeat[-1] == 0:
                self.__non_repeat.pop()

        # -0 방지
        if self.__int_part == 0 and not self.__non_repeat and not self.__repeat:
            self.__sign = 1

    def __compare_abs(self, other):
        # 정수부 비교
        if self.__int_part != other.__int_part:
            return 1 if self.__int_part > other.__int_part else -1


        self_non_len, other_non_len = len(self.__non_repeat), len(other.__non_repeat)
        k_target = max(self_non_len, other_non_len)

        def pad_to_k_target(non, rep, k_target):
            non = non[:]
            if len(non) < k_target:
                need = k_target - len(non)
                if rep:
                    t = (need + len(rep) - 1) // len(rep)
                    non += (rep * t)[:need]
                else:
                    non += [0] * need
            return non

        left_non = pad_to_k_target(self.__non_repeat, self.__repeat, k_target)
        right_non = pad_to_k_target(other.__non_repeat, other.__repeat, k_target)
        if left_non != right_non:
            return 1 if left_non > right_non else -1

        # 반복 비교 주기
        self_rep_len = len(self.__repeat) or 0
        other_rep_len = len(other.__repeat) or 0
        L_target = self.__lcm(self_rep_len, other_rep_len)
        if L_target == 0:
            return 0

        def make_period(rep, L_target):
            if rep:
                t = (L_target + len(rep) - 1) // len(rep)
                return (rep * t)[:L_target]
            return [0] * L_target

        left_rep = make_period(self.__repeat, L_target)
        right_rep = make_period(other.__repeat, L_target)
        if left_rep != right_rep:
            return 1 if left_rep > right_rep else -1
        return 0

    def __add_abs(self, other):
        self_non_len, self_rep_len = len(self.__non_repeat), (len(self.__repeat) or 0)
        other_non_len, other_rep_len = len(other.__non_repeat), (len(other.__repeat) or 0)
        k_target = max(self_non_len, other_non_len)
        L_target = self.__lcm(self_rep_len, other_rep_len)

        left_ip, left_frac = self.__expand_window(self.__int_part, self.__non_repeat, self.__repeat, k_target, L_target, 1)
        right_ip, right_frac = self.__expand_window(other.__int_part, other.__non_repeat, other.__repeat, k_target, L_target, 1)

        result_ip, result_frac = self.__add_frac_digits(left_ip, left_frac, right_ip, right_frac, +1)
        result_ip, non_repeat, repeat = self.__fold_back(result_ip, result_frac, k_target, L_target)
        result = RepeatingDecimal(1, result_ip, non_repeat, repeat)
        result.cleanup()
        return result

    def __sub_abs(self, other):
        self_non_len, self_rep_len = len(self.__non_repeat), (len(self.__repeat) or 0)
        other_non_len, other_rep_len = len(other.__non_repeat), (len(other.__repeat) or 0)
        k_target = max(self_non_len, other_non_len)
        L_target = self.__lcm(self_rep_len, other_rep_len)

        left_ip, left_frac = self.__expand_window(self.__int_part, self.__non_repeat, self.__repeat, k_target, L_target, 1)
        right_ip, right_frac = self.__expand_window(other.__int_part, other.__non_repeat, other.__repeat, k_target, L_target, 1)

        result_ip, result_frac = self.__add_frac_digits(left_ip, left_frac, right_ip, right_frac, -1)
        if result_ip < 0:
            # 절댓값 전제 위배시 뒤집어 보정
            result_ip, result_frac = self.__add_frac_digits(0, [0] * len(result_frac), result_ip, result_frac, -1)

        result_ip, non_repeat, repeat = self.__fold_back(result_ip, result_frac, k_target, L_target)
        result = RepeatingDecimal(1, result_ip, non_repeat, repeat)
        result.cleanup()
        return result

    def __neg__(self):
        """
        Returns a new RepeatingDecimal object with the sign negated.
        """
        if self.__int_part == 0 and not self.__non_repeat and not self.__repeat:
            return RepeatingDecimal(1, 0, [], [])
        return RepeatingDecimal(-self.__sign, self.__int_part, self.__non_repeat[:], self.__repeat[:])

    # TODO: ADDITION HEADER (i.e., x + y binary operator)
    def __add__(self, other):
        """
        Adds two RepeatingDecimal objects and returns a new RepeatingDecimal object.
        """
        if not isinstance(other, RepeatingDecimal):
            return NotImplemented

        # 같은 부호: 절댓값 덧셈 후 부호 유지
        if self.__sign == other.__sign:
            result = self.__add_abs(other)
            result.__sign = self.__sign
            result.cleanup()
            return result

        # 다른 부호: 절댓값 큰 쪽 - 작은 쪽
        cmp_abs = self.__compare_abs(other)
        if cmp_abs == 0:
            return RepeatingDecimal(1, 0, [], [])  

        if cmp_abs > 0:
            result = self.__sub_abs(other)
            result.__sign = self.__sign
            result.cleanup()
            return result
        else:
            result = other.__sub_abs(self)
            result.__sign = other.__sign
            result.cleanup()
            return result

    # TODO: SUBTRACTION HEADER 
    def __sub__(self, other):
        """
        Subtracts another RepeatingDecimal object from this one and returns a new RepeatingDecimal object.
        """
        if not isinstance(other, RepeatingDecimal):
            return NotImplemented
        return self.__add__(-other)

    # TODO: STRING REPRESENTATION HEADER -- THIS ONE IS OPTIONAL, BUT CAN BE HELPFUL FOR DEBUGGING
    def __str__(self):
        sign_str = "-" if self.__sign < 0 else ""
        ip_str = str(self.__int_part)
        non_str = "".join(str(d) for d in self.__non_repeat)
        rep_str = "".join(str(d) for d in self.__repeat)

        if not non_str and not rep_str:
            return f"{sign_str}{ip_str}"
        if rep_str and not non_str:
            return f"{sign_str}{ip_str}.[{rep_str}]"
        if not rep_str:
            return f"{sign_str}{ip_str}.{non_str}"
        return f"{sign_str}{ip_str}.{non_str}[{rep_str}]"

    def __repr__(self):
        return f"RepeatingDecimal.fromString('{self.__str__()}')"


if __name__ == "__main__":
    pass
