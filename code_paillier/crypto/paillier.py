# -*- coding: utf-8 -*-
import gmpy2
import secrets


'''
这是密码算法模块，keygen()算法位数默认值为1024

可以在最下方测试测试模块的函数传参处进行更改位数

测试模块可自行确定测试逻辑
'''


def keygen(bits=1024):
    """
    密钥生成函数keygen()
    输入：bits（可选，默认2048），表示素数的比特长度
    返回：公钥(N, g), 私钥(λ, μ)
    """
    # 生成两个大素数p和q
    state_p = gmpy2.random_state()
    state_q = gmpy2.random_state()

    p = generate_prime(bits // 2, state_p)
    q = generate_prime(bits // 2, state_q)

    while q == p:
        q = generate_prime(bits // 2, state_q)

    # 计算N、λ和μ
    N = p * q
    lambda_ = gmpy2.lcm(p - 1, q - 1)  # 私钥λ

    if gmpy2.gcd(N, lambda_) != 1:
        raise ValueError("gcd(pq, (p-1)(q-1)) should be 1")

    # 确保公钥1<=g<N**2
    k = secrets.randbits(bits)
    g = 1 + k * N

    # 私钥μ
    L = (gmpy2.powmod(g, lambda_, N**2) - 1) // N
    mu = gmpy2.invert(L, N)

    return (N, g), (lambda_, mu)


def generate_prime(bits, state, max_attempts=1000):
    """
    生成指定比特长度的大素数
    输入：bits（素数位数），state（随机状态），max_attempts（最大尝试次数）
    返回：大素数p
    """
    for _ in range(max_attempts):
        candidate = gmpy2.mpz_urandomb(state, bits)
        if candidate >= 2**(bits - 1) and gmpy2.is_prime(candidate):
            return candidate
    raise ValueError("Failed to generate a prime number after {} attempts".format(max_attempts))


def encrypt(public_key, m):
    """
    加密函数encrypt()
    输入：public_key(N, g), 消息m
    返回：密文c
    """
    N, g = public_key

    if m >= N or m < 0:
        raise ValueError("Message m must be in the range [0, N-1]")

    r = secrets.randbits(N.bit_length()) % N + 1  # 确保1 <= r < N

    N_squared = N**2
    c = (gmpy2.powmod(g, m, N_squared) * gmpy2.powmod(r, N, N_squared)) % N_squared
    return c


def decrypt(private_key, public_key, c):
    """
    解密函数decrypt()
    输入：private_key(λ, μ), public_key(N, g), 密文c
    返回：消息m
    """
    lambda_, mu = private_key
    N, _ = public_key

    if c >= N**2 or c < 0:
        raise ValueError("Ciphertext c must be in the range [0, N^2-1]")

    N_squared = N**2
    L = (gmpy2.powmod(c, lambda_, N_squared) - 1) // N
    m = (L * mu) % N
    return m

def get_valid_input(prompt, validator, error_message):
    """ 获取并校验用户输入 """
    while True:
        try:
            value = int(input(prompt))
            if validator(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print("无效输入，请输入一个整数！")

# 测试代码
if __name__ == "__main__":
    try:
        length = num_votes = get_valid_input("please enter the length of the number used in algorithm:", lambda x: x > 0, "请输入一个大于0的整数！")
        public_key, private_key = keygen(bits=length)
        print("------------Public key generated successfully------------\n  (N,g) = ",public_key)
        print("------------Private key generated successfully------------\n  (λ,μ) = ",private_key)

        N = public_key[0]

        message1 = num_votes = get_valid_input("please enter message1:", lambda x: x >= 0, "请输入一个大于等于0的整数！")
        message2 = num_votes = get_valid_input("please enter message2:", lambda x: x >= 0, "请输入一个大于等于0的整数！")

        print("------------Encrypting messages------------")
        ciphertext1 = encrypt(public_key, message1)
        ciphertext2 = encrypt(public_key, message2)
        ciphertext3 = (ciphertext2 * ciphertext1) % (N**2)  # 密文相乘

        decrypted_message1 = decrypt(private_key, public_key, ciphertext1)
        decrypted_message2 = decrypt(private_key, public_key, ciphertext2)
        decrypted_message3 = decrypt(private_key, public_key, ciphertext3)

        print("ciphertext1 and Decrypted message1:\n")
        print("ciphertext1 :\n", ciphertext1)
        print("Decrypted message1: \n", decrypted_message1)
        print("ciphertext2 and Decrypted message2:\n")
        print("ciphertext2:\n",ciphertext2)
        print("Decrypted message2:\n", decrypted_message2)
        print("-------------ciphertext_multi and Decrypted combined message-------------\n")
        print("ciphertext_multi:\n",ciphertext3)
        print("Decrypted combined message:\n", decrypted_message3)

    except Exception as e:
        print("Error during execution:", e)