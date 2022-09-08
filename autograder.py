import os
import sys
import subprocess
import importlib
from cryptography.fernet import Fernet


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file
    and writes it.

    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open('test.py', "wb") as file:
        file.write(decrypted_data)


def check(funcname, args, received, evaluate):
    is_correct, error_msg = evaluate(received)
    if not is_correct:
        msg = '\n' + '-' * 50
        msg += '\nTEST FAILURE!\n'
        msg += "\n{}{} returned the wrong value.".format(funcname, tuple(args))
        msg += f"\n{error_msg}"
        msg += '\n' + '-' * 50
        assert False, msg


def check_effects(funcname, args, received, evaluate):
    is_correct, error_msg = evaluate(received)
    if not is_correct:
        msg = '\n' + '-' * 50
        msg += '\nTEST FAILURE!\n'
        msg += "\n{}{} did not perform the correct side effects.".format(funcname, tuple(args))
        msg += f"\n{error_msg}"
        msg += '\n' + '-' * 50
        assert False, msg


def call_func(func, args):
    try:
        result = func(*args)
    except Exception:
        msg = '\n' + '-' * 50
        msg += '\nTEST FAILURE!\n'
        msg += "\n{}{} crashed!".format(func.__name__, tuple(args))
        msg += '\n' + '-' * 50
        assert False, msg
    return result


def function_test(package_name, funcname, args, evaluate):
    package = importlib.import_module(package_name)
    func = getattr(package, funcname)
    result = call_func(func, args)
    check(funcname, args, result, evaluate)


def method_test(package_name, classname, methodname, args, evaluate):
    package = importlib.import_module(package_name)
    cls = getattr(package, classname)
    method = getattr(cls, methodname)
    result = call_func(method, args)
    check("{}.{}".format(classname, methodname), args, result, evaluate)


def exact_compare(candidate, gold):
    if candidate != gold:
        return False, f"the proposed solution is incorrect:\n{candidate}"
    return True, "correct"


if __name__ == '__main__':
    crypto_key = sys.argv[1]
    test = sys.argv[2]
    try:
        decrypt('test.py.encrypted', crypto_key)
        call_result = subprocess.call(['pytest', '--tb=short', '-rN', 'test.py::' + test])
    except Exception as e:
        print(e)
        call_result = 1
    #finally:
    #    if os.path.exists("test.py"):
    #        os.remove("test.py")

    if call_result == 1:
        exit(1)