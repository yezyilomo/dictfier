from . import factory

def dictfy(obj, query, call_callable=False, serializer=None):
    return factory._dict(
        obj, 
        query, 
        call_callable, 
        serializer,
    )

def useobj(function):
    return factory.UseObj(function)

def usefield(field_name):
    return useobj(lambda obj: getattr(obj, field_name))

def newfield(value):
    return factory.NewField(value)