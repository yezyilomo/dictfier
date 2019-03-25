import json
from .exceptions import FormatError


class UseObj(object):
    def __init__(self, function):
        self.function = function


class NewField(object):
    def __init__(self, value):
        self.value = value


def valid_query(obj, query):
    flat_or_nested = all(
        map(
            lambda node : isinstance(node, (str, dict)),
            query
        )
    )

    iterable = (len(query) <= 1) and all(
        map(
            lambda node: isinstance(node, (list, tuple)),
            query
        )
    )

    if flat_or_nested or iterable:
        return True
    else:
        return False


def is_serealizable(data):
    try:
        json.dumps(data)
        return True
    except:
        return False


def _dict(obj, query, call_callable, serializer, fields=None):
    # Check if the query node is valid against object
    if not valid_query(obj, query):
        message = "Invalid Query format on \"%s\" node." % str(query)
        raise FormatError(message)

    for field in query:
        if isinstance(field, str):
            # Flat field
            if fields is None:
                     fields = {}
            if callable(getattr(obj, field)) and call_callable:
                field_value = getattr(obj, field)()
            else:
                field_value = getattr(obj, field)
            
            if serializer is not None and not is_serealizable(field_value):
                fields.update({field: serializer( field_value )})
            else:
                fields.update({field: field_value})

        elif isinstance(field, dict):
            # Nested or new field
            if fields is None:
                     fields = {}
                
            for sub_field in field:
                if (isinstance(field[sub_field], NewField) and 
                        callable(field[sub_field].value) and 
                        call_callable):
                    field_value = field[sub_field].value()
                    fields.update({sub_field: field_value})
                    continue
                elif isinstance(field[sub_field], NewField):
                    field_value = field[sub_field].value
                    fields.update({sub_field: field_value})
                    continue
                elif (isinstance(field[sub_field], UseObj) and 
                        callable(field[sub_field].function(obj)) and 
                        call_callable):
                    sub_field_value = field[sub_field].function(obj)()
                    fields.update({sub_field: sub_field_value})
                    continue
                elif isinstance(field[sub_field], UseObj):
                    sub_field_value = field[sub_field].function(obj)
                    fields.update({sub_field: sub_field_value})
                    continue
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) < 1):
                    # Nested empty object,
                    # Empty dict is the default value for empty nested objects.
                    # Comment the line below to remove empty objects in results. [FIXME]
                    fields.update({sub_field: {}})
                    continue
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) == 1 and 
                        isinstance(field[sub_field][0], (list, tuple))):
                    # Nested object is iterable 
                    fields.update({sub_field: []})  # Then call _dict again
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) > 0):
                    # Nested object is flat 
                    fields.update({sub_field: {}})  # Then call _dict again
                else:
                    # Ivalid Assignment of value to a field
                    message = (
                        "'%s' value must be of type "
                        "NewField or UseObj, not '%s'. "
                        "Refer to 'useobj', 'usefield' or 'newfield' "
                        "APIs for more details "
                    ) % (str(sub_field), type(field[sub_field]).__name__)
                    raise TypeError(message)

                obj_field = getattr(obj, sub_field)
                if callable(obj_field) and call_callable:
                    obj_field = obj_field()

                # This will be executed if Nested object is flat or iterable
                # since they are the only conditions without continue statement
                _dict(
                    obj_field,
                    field[sub_field],
                    call_callable,
                    serializer,
                    fields=fields[sub_field],
                )

        elif isinstance(field, (list, tuple)):
            # Iterable nested object
            if fields is None:
                     fields = []
            for sub_obj in obj:
                sub_field = {}
                fields.append(sub_field)

                # dictfy all objects in iterable object
                _dict(
                    sub_obj,
                    field,
                    call_callable,
                    serializer,
                    fields=sub_field
                )
        else:
            message = (
                "Wrong formating of Query on '%s' node, "
                "It seems like the Query was mutated during run time."
                "Use 'tuple' instead of 'list' to avoid mutating Query "
                "accidentally."
            ) % str(field)
            raise FormatError(message)

    return fields
