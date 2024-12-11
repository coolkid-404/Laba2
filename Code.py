import random
import gmpy2
from gmpy2 import powmod, invert

def extended_gcd(a, b):
    x, last_x = 0, 1
    y, last_y = 1, 0
    while b != 0:
        q = a // b
        a, b = b, a % b
        x, last_x = last_x - q * x, x
        y, last_y = last_y - q * y, y
    return last_x, last_y

def mod_inverse(e, phi):
    x, _ = extended_gcd(e, phi)
    return x % phi

def secret_number(bits, p, flag):
    if flag == 1:
        while True:    
            Ca = generate_prime_number(bits)
            if Ca < p - 1:
                return Ca
    else:
        while True:    
            Ca = generate_prime_number(bits)
            if Ca <= p - 2:
                return Ca


def is_power_of_two_multiple(number):
    # Проверяем, что число больше 0
    if number <= 0:
        return False

    # Проверяем, является ли число кратным степени 2
    while number % 2 == 0:
        number //= 2

    return number == 1

def random_multiple_of_power_of_2(max_power):
    
    power = random.randint(1, max_power)
    
    result = (2 ** power)

    return result

def miller_rabin_test(n, k=100):
    if n <= 1 or (n > 2 and n % 2 == 0):
        return False
    if n <= 3:
        return True
    
    # Представим n-1 в виде 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Тест Миллера — Рабина
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
        
    return True


def generate_prime_number(bits):
    while True:
        prime_number = random.getrandbits(bits)
        if (prime_number % 2 == 0):
            continue
        if (miller_rabin_test(prime_number)):
            return prime_number
        
def Diffie_Hellman(bits):
    a = generate_prime_number(bits)
    b = generate_prime_number(bits)
    q = generate_prime_number(bits)
    p = 2 * q + 1
    g = random.randint(2, p - 2)
    A = powmod(g, a, p)
    B = powmod(g, b, p)
    ZAB = powmod(B, a, p)
    ZBA = powmod(A, b, p)
    print(f"""
Секретный ключ a = {a}
Секретный ключ b = {b}
Простое число q = {q}
Простое число p = {p}
Число g = {g}
Открытый ключ A = {A}
Открытый ключ B = {B}
Zab = {ZAB}
Zba = {ZBA}
""")
    if ZAB == ZBA:
        print("Отлично! (Zab = Zba)")
    else:
        print("Плохо! (Zab != Zba)")

def Shamir(bits, message):
    p = generate_prime_number(bits)
    Ca = generate_prime_number(bits)
    Cb = generate_prime_number(bits)
    Da = invert(Ca, p - 1)
    Db = invert(Cb, p - 1)

    x1 = powmod(message, Ca, p)
    x2 = powmod(x1, Cb, p)
    x3 = powmod(x2, Da, p)
    x4 = powmod(x3, Db, p)
    print(f"""
Исходное сообщение message = {message}
Простое число p = {p}
Секретный ключ a = {Ca}
Секретный ключ b = {Cb}
Обратное число a = {Da}
Обратное число b = {Db}
Вывод вычислений над числами:
x1 = {x1}
x2 = {x2}
x3 = {x3}
x4 = {x4}
""")

    if x4 == message:
        print("Отлично! x4 = message")
    else:
        print("Плохо! x4 != message")

def El_Gamal(bits, message):
    p = generate_prime_number(bits)
    g = generate_prime_number(bits)
    Ca = generate_prime_number(bits)   # Секретное число абонента A
    print(g)
    print(Ca)
    print(p)
    Da = powmod(g, Ca, p)              # Открытое число абонента A
    Cb = generate_prime_number(bits)   # Секретное число абонента B
    Db = powmod(g, Cb, p)              # Открытое число абонента B
    k = generate_prime_number(bits) 
    r = powmod(g, k, p)
    e = (message * powmod(Db, k, p)) % p
    message2 = (e * powmod(r, p - 1 - Cb, p)) % p
    print(f"""
Исходное сообщение message = {message}
Простое число p = {p}
Простое число p = {g}
Секретное число абонента A = {Ca}
Секретное число абонента B = {Cb}
Открытое число абонента A = {Da}
Открытое число абонента B = {Db}
Зашифрованное сообщение (r, e)= ({r}, {e})
Расшифрованное сообщение m' = {message2}
""")
    if message == message2:
        print("Отлично! message = message2")
    else:
        print("Плохо! message != message2") 

def RSA(bits, message):
    p = generate_prime_number(bits)
    q = generate_prime_number(bits)
    #Ca = generate_prime_number(bits)
    N = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    encrypted_message = powmod(message, e, N)
    decrypted_message = powmod(encrypted_message, d, N)
    print(f"""
Исходное сообщение message = {message}
Простое число p = {p}
Простое число q = {q}
Открытая информация N = {N}
phi = {phi}
e = {e}
Открытое число d к e по модулю phi = {d}
Зашифрованное сообщение = {encrypted_message}
Расшифрованное сообщение = {decrypted_message}
""")
    if message == decrypted_message:
        print("Отлично! message = decrypted_message")
    else:
        print("Плохо! message != decrypted_message") 


def main():
    flag1 = True
    while flag1:
        print("""
1 - Сгенерировать размерность ключа (в битах)
2 - Задать вручную размерность ключа (в битах)
""")
        choose = int(input())
        if choose == 1:
            print("Введите максимальную степень для генерации размерности ключа (например 2 ... 10): ")
            bits = random_multiple_of_power_of_2(int(input()))
            print(f"Сгенерированная размерность ключа (в битах): {bits}")
            flag1 = False
        elif choose == 2:
            while flag1:
                print("Введите размерность ключа (в битах) (оптимально: 256): ")
                bits = int(input())
                if bits > 0 and is_power_of_two_multiple(bits):
                    flag1 = False 
                else:
                    print("Число должно быть кратно степени 2 и быть > 0. Попробуйте ещё раз.")
        else:
            print("Введено неверное значение")
            continue

    
    print("""
Выберите действие:
1 - Схема Диффи-Хелмана
2 - Шифр Шамира
3 - Шифр Эль-Гамаля
4 - Шифр RSA
""")
    choose = int(input())
    if choose == 1:
        print("##################################################")
        print("Схема Диффи-Хелмана")
        Diffie_Hellman(bits)
        flag2 = False
        
    elif choose == 2:
        print("##################################################")
        print("Шифр Шамира")
        message = int(input("Введите сообщение: "))
        Shamir(bits, message)
        flag2 = False
        
    elif choose == 3:
        print("##################################################")
        print("Шифр Эль-Гамаля")
        message = int(input("Введите сообщение: "))
        El_Gamal(bits, message)
        flag2 = False

    elif choose == 4:
        print("##################################################")
        print("Шифр RSA")
        message = int(input("Введите сообщение: "))
        RSA(bits, message)
        flag2 = False

    else:
        print("Введено неверное значение")

if __name__ == "__main__":
    
    main()