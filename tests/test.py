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

    def test_create_new_field(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        student = Student("Danish", 24)

        query = [
            "name",
            "age",
            {
                "school": "St Patrick"
            }
        ]

        try:
            dictfier.dictfy(student, query, not_found_create=True)
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
            dictfier.dictfy(student, query, not_found_create=True)
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
            dictfier.dictfy(student, query, not_found_create=True)
        except dictfier.exceptions.FormatError as e:
            self.fail(e)
        except AttributeError as e:
            self.fail(e)

if __name__ == "main":
    unittest.main()
