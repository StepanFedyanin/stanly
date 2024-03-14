import random
import string


def random_promo(stringLength=8):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False


def is_promo(promo):
    res = True

    if len(promo) != 8:
        res = False

    for s in promo:
        if not is_alpha(s) and not s.isdigit():
            res = False
            break

    return res
