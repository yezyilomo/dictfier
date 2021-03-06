import unittest

import dictfier


#****************  dictify API Tests  ***********************#

class TestDictfyAPI(unittest.TestCase):
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

    def test_objfield_api(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age
        student = Student("Danish", 24)

        query = [
            "name",
            {"age_in_years": dictfier.objfield("age")},
        ]
        self.assertEqual(
            dictfier.dictfy(student, query),
            {
                'name': 'Danish',
                'age_in_years': 24
            }
        )

    def test_objfield_api_with_call_kwarg(self):
        class Student(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

            def age_in_months(self):
                return self.age * 12

        student = Student("Danish", 24)

        query = [
            "name",
            {"months": dictfier.objfield("age_in_months", call=True)},
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

    def test_empty_query_against_flat_nested_and_iterable_obj(self):
        class Book(object):
            def __init__(self, title, publish_date):
                self.title = title
                self.publish_date = publish_date

        class Course(object):
            def __init__(self, code, name, book):
                self.code = code
                self.name = name
                self.book = book

        class Student(object):
            def __init__(self, name, age, courses):
                self.name = name
                self.age = age
                self.courses = courses

        book1 = Book("Advanced Data Structures", "2018")
        book2 = Book("Basic Data Structures", "2010")

        course1 = Course("CS201", "Data Structures", book1)
        course2 = Course("CS205", "Computer Networks", book2)
        courses = [course1, course2]

        student = Student("Danish", 24, courses)

        query1 = []  # Empty outer flat query

        query2 = [[]]  # Empty outer iterable query

        # Empty nested flat query
        query3 = [
            {
                "book": []
            }
        ]

        # Empty nested iterable query
        query4 = [
            {
                "courses": [[]]
            }
        ]

        self.assertEqual(
            dictfier.dictfy(student, query1), {}
        )

        self.assertEqual(
            dictfier.dictfy(courses, query2), [{},{}]
        )

        self.assertEqual(
            dictfier.dictfy(course1, query3),
            {
                "book": {}
            }
        )

        self.assertEqual(
            dictfier.dictfy(student, query4),
            {
                "courses": [{}, {}]
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



#****************  filter API Tests  ***********************#

class TestFilterAPI(unittest.TestCase):
    def test_flat_dict(self):
        student = {
            "name": "Danish",
            "age": 24
        }

        query = [
            "name",
            "age",
        ]
        self.assertEqual(
            dictfier.filter(student, query),
            {
                "name": "Danish",
                "age": 24
            }
        )

    def test_nested_dict(self):
        student = {
            "name": "Danish",
            "age": 24,
            "course": {
                "code": "CS201",
                "name": "Data Structures"
            }
        }

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
            dictfier.filter(student, query),
            {
                "name": "Danish",
                "age": 24,
                "course": {
                    "code": "CS201",
                    "name": "Data Structures"
                }
            }
        )

    def test_custom_nested_dict(self):
        # Customize how dictfier obtains nested flat obj
        # per nested field
        student = {
                'name': 'Danish',
                'age': 24,
                'course':
                {
                    'name': 'Data Structures',
                    'code': 'CS201'
                }
        }

        query = [
            "name",
            "age",
            {
                "course": dictfier.useobj(
                    lambda obj: obj["course"],
                    ["name", "code"]  # This is a query
                )
            }
        ]
        self.assertEqual(
            dictfier.filter(student, query),
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

    def test_iterable_nested_dict(self):
        student = {
            'name': 'Danish',
            'age': 24,
            'courses': [
                {'code': 'CS201', 'name': 'Data Structures'},
                {'code': 'CS205', 'name': 'Computer Networks'}
            ]
        }

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
            dictfier.filter(student, query),
            {
                'name': 'Danish',
                'age': 24,
                'courses': [
                    {'code': 'CS201', 'name': 'Data Structures'},
                    {'code': 'CS205', 'name': 'Computer Networks'}
                ]
            }
        )

    def test_custom_iterable_nested_dict(self):
        # Customize how dictfier obtains nested iterable obj
        # per nested field
        student = {
                'name': 'Danish',
                'age': 24,
                'courses': [
                    {'code': 'CS201', 'name': 'Data Structures'},
                    {'code': 'CS205', 'name': 'Computer Networks'}
                ]
        }
        query = [
            "name",
            "age",
            {
                "courses": dictfier.useobj(
                    lambda obj: obj["courses"],
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
            dictfier.filter(student, query),
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
        student = {
                'name': 'Danish',
                'age': 24
        }
        query = [
            "name",
            "age",
            {
                "school": dictfier.newfield("St Patrick")
            }
        ]
        self.assertEqual(
            dictfier.filter(student, query),
            {
                'name': 'Danish',
                'age': 24,
                'school': 'St Patrick'
            }
        )

    def test_useobj_api(self):
        student = {
                'name': 'Danish',
                'age': 24
        }
        def age_in_months(obj):
            # Do the computation here then return the result
            return obj["age"] * 12

        query = [
            "name",
            {"age_in_months": dictfier.useobj(age_in_months)},
        ]
        self.assertEqual(
            dictfier.filter(student, query),
            {
                'name': 'Danish',
                'age_in_months': 288
            }
        )

    def test_dictfield_api(self):
        student = {
                'name': 'Danish',
                'age': 24
        }
        query = [
            "name",
            {"age_in_years": dictfier.dictfield("age")},
        ]
        self.assertEqual(
            dictfier.filter(student, query),
            {
                'name': 'Danish',
                'age_in_years': 24
            }
        )

    def test_dictfield_api_with_call_kwarg(self):
        def age_in_months():
            return 24 * 12
        student = {
                'name': 'Danish',
                'age': 24,
                'age_in_months': age_in_months
        }
        query = [
            "name",
            {"months": dictfier.dictfield("age_in_months", call=True)},
        ]
        self.assertEqual(
            dictfier.filter(student, query),
            {
                'name': 'Danish',
                'months': 288
            }
        )

    def test_global_filter_config_with_obj_param(self):
        # Customize how dictfier obtains flat obj,
        # nested flat obj and nested iterable obj
        # per filter call (global)
        student = {
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
            dictfier.filter(
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

    def test_global_filter_config_with_parent_and_field_name_params(self):
        # Customize how dictfier obtains flat obj,
        # nested flat obj and nested iterable obj
        # per filter call (global)
        student = {
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
            dictfier.filter(
                student,
                query,
                flat_obj=lambda obj, parent, field_name: parent[field_name],
                nested_iter_obj=lambda obj, parent, field_name: parent[field_name],
                nested_flat_obj=lambda obj, parent, field_name: parent[field_name]
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

    def test_empty_query_against_flat_nested_and_iterable_dict(self):
        book1 = {'title': 'Advanced Data Structures', 'publish_date': '2018'},
        book2 = {'title': 'Basic Data Structures', 'publish_date': '2010'}

        course1 = {'code': 'CS201', 'name': 'Data Structures', 'book': book1}
        course2 = {'code': 'CS205', 'name': 'Computer Networks', 'book': book2}
        courses = [course1, course2]

        student = {
            'name': 'Danish',
            'age': 24,
            'courses': [
                {'code': 'CS201', 'name': 'Data Structures'},
                {'code': 'CS205', 'name': 'Computer Networks'}
            ]
        }

        query1 = []  # Empty outer flat query

        query2 = [[]]  # Empty outer iterable query

        # Empty nested flat query
        query3 = [
            {
                "book": []
            }
        ]

        # Empty nested iterable query
        query4 = [
            {
                "courses": [[]]
            }
        ]

        self.assertEqual(
            dictfier.filter(student, query1), {}
        )

        self.assertEqual(
            dictfier.filter(courses, query2), [{},{}]
        )

        self.assertEqual(
            dictfier.filter(course1, query3),
            {
                "book": {}
            }
        )

        self.assertEqual(
            dictfier.filter(student, query4),
            {
                "courses": [{}, {}]
            }
        )

    def test_query_format_violation(self):
        book1 = {'title': 'Advanced Data Structures', 'publish_date': '2018'},
        book2 = {'title': 'Basic Data Structures', 'publish_date': '2010'}

        course1 = {'code': 'CS201', 'name': 'Data Structures', 'book': book1}
        course2 = {'code': 'CS205', 'name': 'Computer Networks', 'book': book2}
        courses = [course1, course2]

        student = {
            'name': 'Danish',
            'age': 24,
            'courses': [
                course1,
                course2
            ]
        }

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
            dictfier.filter(student, query1)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.filter(student, query2)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.filter(student, query3)

        with self.assertRaises(dictfier.exceptions.FormatError):
            dictfier.filter(student, query4)

        with self.assertRaises(TypeError):
            dictfier.filter(student, query5)


if __name__ == "main":
    unittest.main()
