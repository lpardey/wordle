from functools import wraps
"""
Decorator
    Nace como un patron de diseño de OOP.
    Un decoratior es una funcion o clase.
    Es un patron que permite anadir nueva funcionalidad a un objeto existente, sin modificar su estructura.
    Se llama decorator porque "decora" el funcionamiento y se ubica arriba de la funcion.
"""
def decorator1(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        print("mi decorator 1")
        func(*args, **kwargs)
    return wrap

def decorator2(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        print("mi decorator 2")
        func(*args, **kwargs)
    return wrap

@decorator1
@decorator2
def mi_funcion():
    print("mi funcion")
    pass

def mi_funcion2():
    print("mi funcion 2")

#@decorator1
@decorator2
def mi_funcion3(cosa: int):
    print(f"mi funcion 3: {cosa}")

if __name__ == "__main__":
    mi_funcion3(42)
    print(mi_funcion3.__name__)


decorator1(decorator2(mi_funcion2))
