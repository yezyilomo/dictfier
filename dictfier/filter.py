from .factory import args_len, UseObj, NewField, custom, valid_query
from .exceptions import FormatError


def filtered_dict(
        obj, query, flat_obj, nested_flat_obj,
        nested_iter_obj):
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

            if flat_obj is not None:
                # Costomize how flat obj is obtained
                field_value = custom(flat_obj, field_value, obj, field)

            fields_container.update({field: field_value})

        elif isinstance(field, dict):
            # Nested or New or Computed field
            for sub_field_name, sub_field in field.items():

                if isinstance(sub_field, NewField):
                    # New field

                    field_value = sub_field.value
                    fields_container.update({sub_field_name: field_value})
                    continue
                elif isinstance(sub_field, UseObj):
                    # Computed field

                    computed_value = sub_field.function(obj)
                    if sub_field.query is None:
                        # Field has no child
                        fields_container.update(
                            {sub_field_name: computed_value}
                        )
                        continue
                    else:
                        # Field has a child,
                        # Create a new child and append it to it's parent
                        sub_child = filtered_dict(
                            computed_value,
                            sub_field.query,
                            flat_obj,
                            nested_flat_obj,
                            nested_iter_obj
                        )
                        fields_container.update({sub_field_name: sub_child})
                        continue
                elif (isinstance(sub_field, (list, tuple)) and
                        len(sub_field) == 0):
                        # Nested flat empty query

                    fields_container.update({sub_field_name: {}})
                    continue
                elif (isinstance(sub_field, (list, tuple)) and
                        len(sub_field) == 1 and
                        isinstance(sub_field[0], (list, tuple))):
                        # Nested iterable field

                    obj_field = obj[sub_field_name]
                    if nested_iter_obj is not None:
                        # Costomize how nested iterable obj is obtained
                        obj_field = custom(
                            nested_iter_obj,
                            obj_field,
                            obj,
                            sub_field_name
                        )

                    child_container = []
                    for sub_obj in obj_field:
                        # filter all objects on iterable object
                        child = filtered_dict(
                            sub_obj,
                            sub_field[0],
                            flat_obj,
                            nested_flat_obj,
                            nested_iter_obj
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
                    if nested_flat_obj is not None:
                        # Costomize how nested flat obj is obtained
                        obj_field = custom(
                            nested_flat_obj,
                            obj_field,
                            obj,
                            sub_field_name
                        )

                    child = filtered_dict(
                        obj_field,
                        sub_field,
                        flat_obj,
                        nested_flat_obj,
                        nested_iter_obj
                    )
                    fields_container.update({sub_field_name: child})
                else:
                    # Ivalid Assignment of value to a field
                    message = (
                        "'%s' value must be of type "
                        "NewField or UseObj, not '%s'. "
                        "Refer to 'useobj', 'dictfield' or 'newfield' "
                        "APIs for more details."
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
                    field,
                    flat_obj,
                    nested_flat_obj,
                    nested_iter_obj
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
