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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                "name": "Danish",
                "age": 24
            }
        )

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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                "name": "Danish",
                "age": 24,
                "course": {
                    "code": "CS201",
                    "name": "Data Structures"
                }
            }
        )

    def test_custom_nested_obj(self):
        # Customize how dictfier obtains nested flat obj
        # per nested field
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
                "course": dictfier.useobj(
                    lambda obj: obj.course, 
                    ["name", "code"]  # This is a query
                )
            }
        ]
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish', 
                'age': 24, 
                'course': 
                {
                    'name': 'Data Structures', 
                    'code': 'CS201'
                }
            }
        )

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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish',
                'age': 24,
                'courses': [
                    {'code': 'CS201', 'name': 'Data Structures'},
                    {'code': 'CS205', 'name': 'Computer Networks'}
                ]
            }
        )

    def test_custom_iterable_nested_obj(self):
        # Customize how dictfier obtains nested iterable obj
        # per nested field
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
                "courses": dictfier.useobj(
                    lambda obj: obj.courses, 
                    [
                        [
                            "code",
                            "name",
                        ]
                    ]
                )
            }
        ]
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish', 
                'age': 24, 
                'courses': [
                    {'code': 'CS201', 'name': 'Data Structures'}, 
                    {'code': 'CS205', 'name': 'Computer Networks'}
                ]
            }
        )

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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish', 
                'age': 24, 
                'school': 'St Patrick'
            }
        )

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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish', 
                'age_in_months': 288
            }
        )

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
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish', 
                'age_in_years': 24
            }
        )

    def test_usefield_api_with_call_kwarg(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age
            
            def age_in_months(self):
                return self.age * 12

        student = Student("Danish", 24)

        query = [
            "name",
            {"months": dictfier.usefield("age_in_months", call=True)},
        ]
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish',
                'months': 288
            }
        )

    def test_global_dictfy_config_with_obj_param(self):
        # Customize how dictfier obtains flat obj, 
        # nested flat obj and nested iterable obj
        # per dictfy call (global)
        class Book(object):
            def __init__(self, title, publish_date):
                self.title = title
                self.publish_date = publish_date

        class Course(object):
            def __init__(self, code, name, books):
                self.code = code
                self.name = name
                self.books = books

        class Student(object):
            def __init__(self, name, age, course):
                self.name = name
                self.age = age
                self.course = course

        book1 = Book("Advanced Data Structures", "2018")
        book2 = Book("Basic Data Structures", "2010")
        course = Course("CS201", "Data Structures", [book1, book2])
        student = Student("Danish", 24, course)
        query = [
            "name",
            "age",
            {
                "course": [
                    "name", 
                    "code",
                    {
                        "books": [[
                            "title", 
                            "publish_date"
                        ]]
                    }
                ]
            }
        ]
        self.assertEqual(
            dictfier.dictfy(
                student,
                query,
                flat_obj=lambda obj: obj,
                nested_iter_obj=lambda obj: obj,
                nested_flat_obj=lambda obj: obj
            ),
            {
                'name': 'Danish', 
                'age': 24, 
                'course': {
                    'name': 'Data Structures', 
                    'code': 'CS201', 'books': [
                        {'title': 'Advanced Data Structures', 'publish_date': '2018'}, 
                        {'title': 'Basic Data Structures', 'publish_date': '2010'}
                    ]
                }
            }
        )

    def test_global_dictfy_config_with_parent_and_field_name_params(self):
        # Customize how dictfier obtains flat obj, 
        # nested flat obj and nested iterable obj
        # per dictfy call (global)
        class Book(object):
            def __init__(self, title, publish_date):
                self.title = title
                self.publish_date = publish_date

        class Course(object):
            def __init__(self, code, name, books):
                self.code = code
                self.name = name
                self.books = books

        class Student(object):
            def __init__(self, name, age, course):
                self.name = name
                self.age = age
                self.course = course

        book1 = Book("Advanced Data Structures", "2018")
        book2 = Book("Basic Data Structures", "2010")
        course = Course("CS201", "Data Structures", [book1, book2])
        student = Student("Danish", 24, course)
        query = [
            "name",
            "age",
            {
                "course": [
                    "name", 
                    "code",
                    {
                        "books": [[
                            "title", 
                            "publish_date"
                        ]]
                    }
                ]
            }
        ]
        self.assertEqual(
            dictfier.dictfy(
                student,
                query,
                flat_obj=lambda obj, parent, field_name: getattr(parent, field_name),
                nested_iter_obj=lambda obj, parent, field_name: getattr(parent, field_name),
                nested_flat_obj=lambda obj, parent, field_name: getattr(parent, field_name)
            ),
            {
                'name': 'Danish', 
                'age': 24, 
                'course': {
                    'name': 'Data Structures', 
                    'code': 'CS201', 'books': [
                        {'title': 'Advanced Data Structures', 'publish_date': '2018'}, 
                        {'title': 'Basic Data Structures', 'publish_date': '2010'}
                    ]
                }
            }
        )

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
