from . import factory

def dictfy(obj, query, call_callable=False, not_found_create=False):
    return factory._dict(
        obj, 
        query, 
        call_callable, 
        not_found_create
    )

def useobj(function):
    return factory.UseObj(function)

def usefield(field_name):
    return useobj(lambda obj: getattr(obj, field_name))