import math
import asyncio

async def func1():
    global n
    while True:
        isprime = True
        for i in range(2, int(math.sqrt(n))+1):
            if n % i == 0:
                print("A's Prime Number: ", i)
                await asyncio.sleep(0.001)
                n = int(n / i)
                isprime = False
                break
        if isprime is True:
            print("A's Prime Nunber: ", n)
            break


async def func2():
    global m
    while True:
        isprime = True
        for j in range(2, int(math.sqrt(m)) + 1):
            if m % j == 0:
                print("B's Prime Number: ", j)
                await asyncio.sleep(0.001)
                m = int(m / j)
                isprime = False
                break
        if isprime is True:
            print("B's Prime Number: ", m)
            break


def read_nm():
    global n, m
    while True:
        x = input("input an int for A: ")
        if x.isnumeric():
            n = int(x)
            break
        else:
            continue
    while True:
        y = input("inout an int for B: ")
        if y.isnumeric():
            m = int(y)
            break
        else:
            continue


n = 0
m = 0
read_nm()
a = func1()
b = func2()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([a, b]))
loop.close()

