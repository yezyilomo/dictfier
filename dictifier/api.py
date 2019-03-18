from . import factory

def dictify(obj, query, call_callable=False, not_found_create=False):
    return factory._dict(
        obj, 
        query, 
        call_callable, 
        not_found_create
    )

def useobj(function):
    return factory.UseObj(function)