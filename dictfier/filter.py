from .factory import valid_query
from .exceptions import FormatError


def filtered_dict(obj, query):
    # Check if the query node is valid
    if not valid_query(query):
        message = "Invalid Query format on \"%s\" node." % str(query)
        raise FormatError(message)

    # Initial value for flat empty query
    fields_container = {}
    for field in query:
        if isinstance(field, str):
            # Flat field
            field_value = obj[field]
            fields_container.update({field: field_value})

        elif isinstance(field, dict):
            # Nested field
            for sub_field_name, sub_field in field.items():
                if (isinstance(sub_field, (list, tuple)) and
                        len(sub_field) == 0):
                        # Nested flat empty query

                    fields_container.update({sub_field_name: {}})
                    continue
                elif (isinstance(sub_field, (list, tuple)) and
                        len(sub_field) == 1 and
                        isinstance(sub_field[0], (list, tuple))):
                        # Nested iterable field

                    obj_field = obj[sub_field_name]

                    child_container = []
                    for sub_obj in obj_field:
                        # filter all objects on iterable object
                        child = filtered_dict(
                            sub_obj,
                            sub_field[0]
                        )
                        child_container.append(child)

                    fields_container.update(
                        {sub_field_name: child_container}
                    )
                    continue

                elif (isinstance(sub_field, (list, tuple)) and
                        len(sub_field) > 0):
                        # Nested flat field

                    obj_field = obj[sub_field_name]

                    child = filtered_dict(
                        obj_field,
                        sub_field
                    )
                    fields_container.update({sub_field_name: child})
                else:
                    # Ivalid Assignment of value to a field
                    message = (
                        "'%s' value must be of type "
                        "list or dict when filtering, not '%s'. "
                        "Refer to 'filter'"
                        "API for more details "
                    ) % (str(sub_field_name), type(sub_field).__name__)
                    raise TypeError(message)

        elif isinstance(field, (list, tuple)):
            # Iterable field

            # Initial value for iterable empty query
            fields_container = []
            for sub_obj in obj:
                # filter all objects on iterable object
                child = filtered_dict(
                    sub_obj,
                    field
                )
                fields_container.append(child)
        else:
            message = (
                "Wrong formating of Query on '%s' node, "
                "It seems like the Query was mutated during run time."
                "Use 'tuple' instead of 'list' to avoid mutating Query "
                "accidentally."
            ) % str(field)
            raise FormatError(message)

    return fields_container
