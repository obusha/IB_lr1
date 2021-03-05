class Blocks32Bit:
    BLOCK_LEN = 32

    def __init__(self, block):
        self.block = block

    def __rshift__(self, other):
        return Blocks32Bit(self.block[:-other].rjust(self.BLOCK_LEN, '0'))

    def __lshift__(self, other):
        return Blocks32Bit(self.block[other:].ljust(self.BLOCK_LEN, '0'))

    def __and__(self, other):
        message = ''
        for x, y in zip(self.block, other.block):
            if x == '1' and y == '1':
                message += '1'
            else:
                message += '0'
        return Blocks32Bit(message)

    def __xor__(self, other):
        message = ''
        for x, y in zip(self.block, other.block):
            if x == y:
                message += '0'
            else:
                message += '1'
        return Blocks32Bit(message)

    def __or__(self, other):
        message = ''
        for x, y in zip(self.block, other.block):
            if x == '0' and y == '0':
                message += '0'
            else:
                message += '1'
        return Blocks32Bit(message)

    def __invert__(self):
        message = ''
        for x in self.block:
            if x == '0':
                message += '1'
            else:
                message += '0'
        return Blocks32Bit(message)

    def __add__(self, other):
        x = int(self.block, 2)
        y = int(other.block, 2)
        result = (x + y) % (2 ** 32)
        return Blocks32Bit(format(result, '032b'))

    def right_rotate(self, n):
        return (self >> n) | (self << (self.BLOCK_LEN - n))

    def s_0(self):
        return self.right_rotate(7) ^ self.right_rotate(18) ^ (self >> 3)

    def s_1(self):
        return self.right_rotate(17) ^ self.right_rotate(19) ^ (self >> 10)

    def sigma_0(self):
        return self.right_rotate(2) ^ self.right_rotate(13) ^ self.right_rotate(22)

    def sigma_1(self):
        return self.right_rotate(6) ^ self.right_rotate(11) ^ self.right_rotate(25)

    def to_string_hash(self):
        return format(int(self.block, 2), '08x')

    def to_string(self):
        return self.block
