# dictfier

[![Build Status](https://api.travis-ci.com/yezyilomo/dictfier.svg?branch=master)](https://api.travis-ci.com/yezyilomo/dictfier)
[![Latest Version](https://img.shields.io/pypi/v/dictfier.svg)](https://pypi.org/project/dictfier/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dictfier.svg)](https://pypi.org/project/dictfier/)
[![License](https://img.shields.io/pypi/l/dictfier.svg)](https://pypi.org/project/dictfier/)

**dictfier** is a library to convert/serialize Python class instances(Objects) both **flat** and **nested** into a dictionary data structure. It's very useful in converting Python Objects into JSON format especially for nested objects, because they can't be handled well by json library

### Prerequisites

python version >= 2.7

### Installing

```python
pip install dictfier
```

## Getting Started

#### Converting a flat object into a dict

```python
import dictfier

class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Danish", 24)

query = [
    "name",
    "age"
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age': 24}
```

#### Converting nested object into a dict

```python
import dictfier

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

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{
    'name': 'Danish', 
    'age': 24, 
    'course': {'code': 'CS201', 'name': 'Data Structures'}
}
```

#### Converting object nested with iterable object into a dict

```python
import dictfier

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

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{
    'name': 'Danish', 
    'age': 24, 
    'courses': [
        {'code': 'CS201', 'name': 'Data Structures'}, 
        {'code': 'CS205', 'name': 'Computer Networks'}
    ]
}
```


#### What about instance methods or callable object fields?

Well we've got good news for that, **dictfier** can use callables which return values as fields, It's very simple, you just have to pass "call=True" as a keyword argument to usefield API and add your callable field to a query. E.g.

```python
import dictfier

class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def age_in_days(self):
        return self.age * 365

student = Student("Danish", 24)

query = [
    "name",
    {
        "age_in_days": dictfier.usefield("age_in_days", call=True)
    }
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age_in_days': 8760}
```


You can also add your custom field by using **newfield** API. E.g.

```python
import dictfier

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

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age': 24, 'school': 'St Patrick'}
```


#### What if we want to use object field on a custom field to do some computations?.

Well there is a way to do that too, **dictfier** API provides **useobj** hook which is used to hook or pull the object on a current query node. To use the current object, just define a fuction which accept single argument(which is an object) and perform your computations on such function and then return a result, call **useobj** and pass that defined fuction to it. 

Let's say we want to calculate age of a student in terms of months from a student object with age field in terms of years. Here is how we would do this by using **useobj** hook.

```python
import dictfier

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
    
    # This is a custom field which is computed by using age field from a student object
    # Note how age_in_months function is passed to useobj hook(This is very important for API to work)
    {"age_in_months": dictfier.useobj(age_in_months)}
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age_in_months': 288}
```


#### What if we want to use object field on a custom field(Rename obj field)?

This can be accomplished in two ways, As you might have guessed, one way to do it is to use **useobj** hook by passing a function which return the value of a field which you want to use, another simple way is to use **usefield** hook. Just like **useobj** hook, **usefield** hook is used to hook or pull object field on a current query node. To use the current object field, just call **usefield** and pass a field name which you want to use or replace.

Let's say we want to rename **age** field to **age_in_years** in our results. Here is how we would do this by using **usefield** hook.

```python
import dictfier

class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Danish", 24)

query = [
    "name",
    {"age_in_years": dictfier.usefield("age")}
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age_in_years': 24}
```


And if you want to use **useobj** hook then this is how you would do it.

```python
import dictfier

class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Danish", 24)

query = [
    "name",
    {"age_in_years": dictfier.useobj(lambda obj: obj.age)}
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{'name': 'Danish', 'age_in_years': 24}
```


Infact **usefield** hook is implemented by using **useobj**, so both methods are the same interms of performance, but I think you would agree with me that in this case **usefield** is more readable than **useobj**.

You can also query an object returned by **useobj** hook, This can be done by passing a query as a second argument to **useobj** or use 'query=your_query' as a kwarg. E.g.

```python
import json
import dictfier

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

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{
    'name': 'Danish', 
    'age': 24, 
    'course': {
        'name': 'Data Structures', 
        'code': 'CS201'
    }
}
```


#### For iterable objects, here is how you would do it.

```python
import json
import dictfier

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
            [["name", "code"]]  # This is a query
        )
    }
]

std_info = dictfier.dictfy(student, query)
print(std_info)
```

```python
# Output
{
    'name': 'Danish', 
    'age': 24, 
    'courses': [
        {'name': 'Data Structures', 'code': 'CS201'}, 
        {'name': 'Computer Networks', 'code': 'CS205'}
    ]
}
```


## How dictfier works?

**dictfier** works by converting given Object into a corresponding dict **recursively(Hence works on nested objects)** by using a **Query**. So what's important here is to know how to structure right queries to extract right data from the object.

#### What's a Query anyway?

A Query is basically a template which tells dictfier what to extract from an object. It is defined as a list or tuple of Object's fields to be extracted.

#### Sample conversions.

When a flat student object is queried using a query below
```python
query = [
    "name",
    "age",
]
```

**dictfier** will convert it into 

```python
{
    "name": student.name,
    "age": student.age,
}   
```

**For nested queries it goes like**

```python
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
```

**Corresponding dict**

```python
{
    "name": student.name,
    "age": student.age,
    "course": {
        "code": student.course.code,
        "name": student.course.name,
    }
}
```

**For iterable objects it goes like**

```python
query = [
    "name",
    "age",
    {
        "course": [ 
            [
                "code",
                "name",
            ]
        ]
    }
]
```
Putting a list or tuple inside a list or tuple of object fields is a way to declare that the Object is iterable. In this case
```python
[ 
    [
        "code",
        "name",
    ]
]
```

**Corresponding dict**

```python
{
    "name": student.name,
    "age": student.age,
    "courses": [
        {
            "code": course.code,
            "name": course.name,
        }
        for course in student.courses
    ]
}
```
Notice the list or tuple on "courses" unlike in other fields like "name" and "age", it makes "courses" iterable, This is the reason for having nested list or tuple on "courses" query.

**It's pretty simple right?**


## What if I want to customize how dictfier works?

You might encounter a case where you have to change how dictfier works to get the result which you want, don't worry we have got your back. **dictfier** is highly configurable, it allows you to configure how each type of object is converted into a dictionary data structure. **dictfier** configuration is divided into three parts which are

* Flat objects config(pass flat_obj=function kwarg to dictfy)

* Nested flat objects config(pass nested_flat_obj=function kwarg to dictfy)

* Nested iterable objects config(pass nested_iter_obj=function kwarg to dictfy)

In all cases above, function assigned to flat_obj, nested_flat_obj or nested_iter_obj accepts three positional arguments which are field value(object) and parent object and field name. Now consider an example of a simple ORM with two relations **Many** and **One** which are used to show how objects are related.

```python
# Customize how dictfier obtains flat obj, 
# nested flat obj and nested iterable obj
import dictfier

class Many(object):
    def __init__(self, data):
        self.data = data

class One(object):
    def __init__(self, data):
        self.data = data

class Book(object):
    def __init__(self, pk, title, publish_date):
        self.pk = pk
        self.title = title
        self.publish_date = publish_date

class Mentor(object):
    def __init__(self, pk, name, profession):
        self.pk = pk
        self.name = name
        self.profession = profession

class Course(object):
    def __init__(self, pk, code, name, books):
        self.pk = pk
        self.code = code
        self.name = name
        self.books = Many(books)

class Student(object):
    def __init__(self, pk, name, age, mentor, courses):
        self.pk = pk
        self.name = name
        self.age = age
        self.mentor = One(mentor)
        self.courses = Many(courses)

book1 = Book(1, "Advanced Data Structures", "2018")
book2 = Book(2, "Basic Data Structures", "2010")
book3 = Book(1, "Computer Networks", "2011")

course1 = Course(1, "CS201", "Data Structures", [book1, book2])
course2 = Course(2, "CS220", "Computer Networks", [book3])

mentor = Mentor(1, "Van Donald", "Software Eng")
student = Student(1, "Danish", 24, mentor, [course1, course2])
query = [
    "name",
    "age",
    {   "mentor": [
            "name",
            "profession"
        ],
        "courses": [[
            "name", 
            "code",
            {
                "books": [[
                    "title", 
                    "publish_date"
                ]]
            }
        ]]
    }
]

result = dictfier.dictfy(
    student, 
    query, 
    flat_obj=lambda obj, parent: obj,
    nested_iter_obj=lambda obj, parent: obj.data,
    nested_flat_obj=lambda obj, parent: obj.data
)
print(result)
```

```python
# Output
{
    'name': 'Danish', 
    'age': 24, 
    'mentor': {'name': 'Van Donald', 'profession': 'Software Eng'}, 
    'courses': [
        {
            'name': 'Data Structures', 
            'code': 'CS201', 
            'books': [
                {'title': 'Advanced Data Structures', 'publish_date': '2018'}, 
                {'title': 'Basic Data Structures', 'publish_date': '2010'}
            ]
        }, 
        {
            'name': 'Computer Networks', 
            'code': 'CS220', 
            'books': [
                {'title': 'Computer Networks', 'publish_date': '2011'}
            ]
        }
    ]
}
````


From an example above, if you want to return primary key(pk) for nested flat or nested iterable object(which is very common in API design and serializing models) you can do it as follows.

```python
query = [
    "name",
    "age",
    "mentor",
    "courses"
]

def get_pk(obj, parent, field_name):
    if isinstance(obj, One):
        return obj.data.pk
    elif isinstance(obj, Many):
        return [rec.pk for rec in obj.data]
    else:
        return obj

result = dictfier.dictfy(
    student, 
    query, 
    flat_obj=get_pk,
    nested_iter_obj=lambda obj, parent: obj.data,
    nested_flat_obj=lambda obj, parent: obj.data
)
print(result)
```


```python
# Output
{'name': 'Danish', 'age': 24, 'mentor': 1, 'courses': [1, 2]}
```

## Contributing [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) 

I welcome all contributions. Please read [CONTRIBUTING.md](https://github.com/yezyilomo/dictfier/blob/master/CONTRIBUTING.md) first. You can submit any ideas as [pull requests](https://github.com/yezyilomo/dictfier/pulls) or as [GitHub issues](https://github.com/yezyilomo/dictfier/issues). If you'd like to improve code, check out the [Code Style Guide](https://github.com/yezyilomo/dictfier/blob/master/CONTRIBUTING.md#styleguides) and have a good time!.

