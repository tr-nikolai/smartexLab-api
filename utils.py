from flask import jsonify
from random import randint


def generate_new_card():
    list_number = []
    while len(list_number) != 13:
        list_number.append(str(randint(0, 9)))
    number_new_card = ''.join(list_number)
    list_cvv = []
    while len(list_cvv) != 3:
        list_cvv.append(str(randint(0, 9)))
    cvv_new_card = ''.join(list_cvv)
    list_pin = []
    while len(list_pin) != 4:
        list_pin.append(str(randint(0, 9)))
    pin_new_card = ''.join(list_pin)
    return number_new_card, cvv_new_card, pin_new_card


def bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response


def not_found(message):
    response = jsonify({'error': message})
    response.status_code = 404
    return response