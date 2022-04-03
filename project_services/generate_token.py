# coding=utf-8


from random import choice


alphabet = list("qwertyuiopasdfghjklzxcvbnm1234567890")


async def generate_token():
    token = [choice(alphabet) for letter in range(100)]
    return token
