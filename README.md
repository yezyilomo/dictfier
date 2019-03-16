# dictifier

**dictifier** is a library to convert Python class instances(Objects) both **flat** and **nested** into a dictionary data structure. It's very useful in converting Python Objects into JSON format especially for nested objects, because they can't be handled well by json library

### Prerequisites

-python3

### Installing

```
pip3 install dictifier
```

## Getting Started

-**Converting flat object into dict**

```
import dictifier

class Student(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Danish", 24)

query = [
    "name",
    "age"
]

std_info = dictifier.dictify(student, query)
print(std_info)
```

-**Converting nested object into dict**

```
import dictifier

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

std_info = dictifier.dictify(student, query)
print(std_info)
```

-**Converting objects nested with iterable objects into dict**

```
import dictifier

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
course2 = Course('CS205", "Computer Networks")

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

std_info = dictifier.dictify(student, query)
print(std_info)
```

-**Important Tip**

What's important here is to know how to structure right queries to extract right data from your object.

-**What's a query anyway?**

A Query is basically a template which tells dictifier what to extract from an object.

A Query is defined as a list of Object's fields to be extracted.

-**How dictifier works**

**dictifier** works by converting query given into a corresponding dict

**Eg**.

When student object is queried using query below
```
query = [
    "name",
    "age"
]
```

**dictifier** will convert it into 

```
{
    "name": student.name,
    "age": student.age,
}   
```


**For nested queries it goes like**

```
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

```
{
    "name": student.name,
    "age": student.age,
    "course": {
        "code": student.course.code,
        "name": student.course.name,
    }
}
```

**It's pretty simple right?**