import unittest

import dictfier


class TestAPI(unittest.TestCase):
    def test_flat_obj(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        student = Student("Danish", 24)

        query = [
            "name",
            "age",
        ]
        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_nested_obj(self):
        class Course(object):
            def __init__(self, code, name):
                self.code = code
                self.name = name

        class Student(object):
            def __init__(self, name, age, course):
                self.name = name
                self.age = age
                self.course = course
        course = Course("CS201", "Data Structures")
        student = Student("Danish", 24, course)
        query = [
            "name",
            "age",
            {
                "course": [
                    "code",
                    "name",
                ]
            }
        ]
        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_iterable_nested_obj(self):
        class Course(object):
            def __init__(self, code, name):
                self.code = code
                self.name = name

        class Student(object):
            def __init__(self, name, age, courses):
                self.name = name
                self.age = age
                self.courses = courses

        course1 = Course("CS201", "Data Structures")
        course2 = Course("CS205", "Computer Networks")

        student = Student("Danish", 24, [course1, course2])

        query = [
            "name",
            "age",
            {
                "courses": [
                    [
                        "code",
                        "name",
                    ]
                ]
            }
        ]

        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_callable_field(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

            def age_in_days(self):
                return self.age * 365

        student = Student("Danish", 24)

        query = [
            "name",
            "age_in_days"
        ]

        try:
            dictfier.dictfy(student, query, call_callable=True)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_newfield_api(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        student = Student("Danish", 24)

        query = [
            "name",
            "age",
            {
                "school": dictfier.newfield("St Patrick")
            }
        ]

        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_useobj_api(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        student = Student("Danish", 24)

        def age_in_months(obj):
            # Do the computation here then return the result
            return obj.age * 12

        query = [
            "name",
            {"age_in_months": dictfier.useobj(age_in_months)},
        ]

        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_usefield_api(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        student = Student("Danish", 24)

        query = [
            "name",
            {"age_in_years": dictfier.usefield("age")},
        ]

        try:
            dictfier.dictfy(student, query)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_serializer_kwarg_on_flat_nested_obj(self):
        class Course(object):
            def __init__(self, code, name):
                self.code = code
                self.name = name

        class Student(object):
            def __init__(self, name, age, course):
                self.name = name
                self.age = age
                self.course = course
        course = Course("CS201", "Data Structures")
        student = Student("Danish", 24, course)
        query = [
            "name",
            "age",
            "course",
        ]
        try:
            dictfier.dictfy(student, query, serializer=lambda obj: obj.name)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

    def test_serializer_kwarg_on_iterable_nested_obj(self):
        class Course(object):
            def __init__(self, code, name):
                self.code = code
                self.name = name

        class Student(object):
            def __init__(self, name, age, courses):
                self.name = name
                self.age = age
                self.courses = courses

        course1 = Course("CS201", "Data Structures")
        course2 = Course("CS205", "Computer Networks")

        student = Student("Danish", 24, [course1, course2])

        query = [
            "name",
            "age",
            "courses"
        ]

        try:
            dictfier.dictfy(student, query, serializer=lambda obj: [c.name for c in obj])
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)


    def test_query_format_violation(self):
        class Course(object):
            def __init__(self, code, name):
                self.code = code
                self.name = name

        class Student(object):
            def __init__(self, name, age, courses):
                self.name = name
                self.age = age
                self.courses = courses

        course1 = Course("CS201", "Data Structures")
        course2 = Course("CS205", "Computer Networks")

        student = Student("Danish", 24, [course1, course2])

        query1 = [
            "name",
            "age",
            566  # FormatError
        ]
        query2 = [
            "name",
            "age",
            ["name"]  # FormatError
        ]

        query3 = [
            "name",
            "age",
            {
                "courses": [
                    ["code", "name"],
                    "name", # FormatError
                ]
            }
        ]

        query4 = [
            "name",
            "age",
            {
                "courses": [
                    "name",  # FormatError
                    ["code", "name"],
                ]
            }
        ]

        query5 = [
            "name",
            "age",
            {
                "class": "HBO"  # TypeError
            }
        ]

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.dictfy(student, query1)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.dictfy(student, query2)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.dictfy(student, query3)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.dictfy(student, query4)

        with self.assertRaises(TypeError):
            dictfier.dictfy(student, query5)


if __name__ == "main":
    unittest.main()
