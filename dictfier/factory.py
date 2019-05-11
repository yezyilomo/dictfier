import sys
from .exceptions import FormatError


if sys.version_info[0] < 3:
    from inspect import getargspec
    get_args = getargspec
    args_prop = "args"
else:
    from inspect import signature
    get_args = signature
    args_prop = "parameters"


def args_len(function):
        args = getattr(get_args(function), args_prop)
        return len(args)


class UseObj(object):
    def __init__(self, function, query):
        self.function = function
        self.query = query


class NewField(object):
    def __init__(self, value):
        self.value = value


def custom(customr, field_value, parent_obj, field_name):
    # Costomize how object is obtained
    # Pass both field value, parent obj and field name
    # for the purpose of flexibility
    args_length = args_len(customr)
    if args_length == 1:
        return customr(field_value)
    elif args_length == 2:
        return customr(field_value, parent_obj)
    elif args_length == 3:
        return customr(field_value, parent_obj, field_name)
    else:
        raise TypeError(
            "%s() takes at most 3 argument (%s given)"
            %(customr.__name__, args_length)
        )


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


def _dict(
        obj, query, flat_obj, nested_flat_obj, 
        nested_iter_obj, fields_container=None):
    # Check if the query node is valid against object
    if not valid_query(obj, query):
        message = "Invalid Query format on \"%s\" node." % str(query)
        raise FormatError(message)

    if not query:
        # Outer flat empty query
        return {}

    for field in query:
        if isinstance(field, str):
            # Flat field
            if fields_container is None:
                     fields_container = {}
            field_value = getattr(obj, field)

            if flat_obj is not None:
                # Costomize how flat obj is obtained
                field_value = custom(flat_obj, field_value, obj, field)

            fields_container.update({field: field_value})

        elif isinstance(field, dict):
            # Nested or New or Computed field
            if fields_container is None:
                     fields_container = {}
                
            for sub_field in field:
                if isinstance(field[sub_field], NewField):
                    # New field
                    field_value = field[sub_field].value
                    fields_container.update({sub_field: field_value})
                    continue
                elif isinstance(field[sub_field], UseObj):
                    # Computed field
                    sub_field_value = field[sub_field].function(obj)
                    if field[sub_field].query is None:
                        # Field has no child
                        fields_container.update({sub_field: sub_field_value})
                        continue
                    else:
                        # Field has a child,
                        # Create a new child and append it to it's parent
                        sub_child = _dict(
                            sub_field_value,
                            field[sub_field].query,
                            flat_obj,
                            nested_flat_obj,
                            nested_iter_obj,
                            fields_container=None,
                        )
                        fields_container.update({sub_field: sub_child})
                        continue
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) < 1):
                    # Nested flat empty query
                    fields_container.update({sub_field: {}})
                    continue
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) == 1 and 
                        isinstance(field[sub_field][0], (list, tuple))):
                    # Nested iterable field 

                    # works for empty & non-empty nested iterable query
                    fields_container.update({sub_field: []}) 

                    obj_field = getattr(obj, sub_field)
                    if nested_iter_obj is not None:
                        # Costomize how nested iterable obj is obtained
                        obj_field = custom(
                            nested_iter_obj, 
                            obj_field, 
                            obj, 
                            sub_field
                        )
                    else:
                        pass
                    # Then call _dict again
                elif (isinstance(field[sub_field], (list, tuple)) and 
                        len(field[sub_field]) > 0):
                    # Nested flat field
                    fields_container.update({sub_field: {}})
                    obj_field = getattr(obj, sub_field)
                    if nested_flat_obj is not None:
                        # Costomize how nested flat obj is obtained
                        obj_field = custom(
                            nested_flat_obj, 
                            obj_field, 
                            obj, 
                            sub_field
                        )
                    else:
                        pass
                    # Then call _dict again
                else:
                    # Ivalid Assignment of value to a field
                    message = (
                        "'%s' value must be of type "
                        "NewField or UseObj, not '%s'. "
                        "Refer to 'useobj', 'usefield' or 'newfield' "
                        "APIs for more details "
                    ) % (str(sub_field), type(field[sub_field]).__name__)
                    raise TypeError(message)

                # This will be executed if Nested field is flat or iterable
                # since they are the only blocks without continue statement
                _dict(
                    obj_field,
                    field[sub_field],
                    flat_obj,
                    nested_flat_obj,
                    nested_iter_obj,
                    fields_container=fields_container[sub_field],
                )

        elif isinstance(field, (list, tuple)):
            # Iterable nested query or Iterable outer query
            if fields_container is None:
                     # Iterable outer query
                     fields_container = []

            for sub_obj in obj:
                sub_field = {}
                fields_container.append(sub_field)

                # dictfy all objects in iterable object
                _dict(
                    sub_obj,
                    field,
                    flat_obj,
                    nested_flat_obj,
                    nested_iter_obj,
                    fields_container=sub_field
                )
        else:
            message = (
                "Wrong formating of Query on '%s' node, "
                "It seems like the Query was mutated during run time."
                "Use 'tuple' instead of 'list' to avoid mutating Query "
                "accidentally."
            ) % str(field)
            raise FormatError(message)

    return fields_container
