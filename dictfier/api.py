from . import factory

def dictfy(obj, query):
    return factory._dict(
        obj, 
        query, 
    )


def useobj(function, fields=None):
    return factory.UseObj(function, fields)


def usefield(field_name, call=False, args=tuple(), kwargs={}):
    if call:
        return useobj(
            lambda obj: getattr(obj, field_name)(*args, **kwargs), 
            fields=None
        )
    else:
        return useobj(lambda obj: getattr(obj, field_name), fields=None)


def newfield(value):
    return factory.NewField(value)