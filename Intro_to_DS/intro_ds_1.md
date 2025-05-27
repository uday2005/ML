# Python Programming: Comprehensive Notes

This document provides a comprehensive summary of foundational Python programming concepts, as illustrated in the provided notebook. It covers strings and encoding, string operations, functions, variable scope, data structures (lists, tuples, dictionaries, sets), comprehensions, functional programming tools, and more. The explanations are supported by code examples and practical notes.

---

## 1. Strings and Encoding

### Unicode and Bytes

Python 3 uses Unicode for its string type (`str`). Unicode allows for the representation of characters from virtually all human languages, as well as many symbols.

- **Encoding** is the process of converting a Unicode string into a sequence of bytes. The most common encoding is UTF-8.
- **Decoding** is the reverse process: converting bytes back into a Unicode string.

**Example:**
```python
b = "ä".encode("utf-8")     # Convert character(s) to a sequence of bytes
print(b)                    # Prints bytes in hexadecimal notation: b'\xc3\xa4'
print(list(b))              # Prints bytes in decimal notation: [195, 164]
print(b.decode("utf-8"))    # Converts bytes back to string: 'ä'
```

### Escape Sequences and Multiline Strings

- Escape sequences like `\n` (newline) and `\t` (tab) allow you to include special characters in strings.
- Multiline strings can be created using triple quotes (`"""` or `'''`):

```python
s = """A string
spanning over
several lines"""
```

---

## 2. String Operations and Formatting

### Concatenation and Joining

- Use `+` to concatenate strings: `"hello" + "world"`
- Use `" ".join([a, b, c])` to join a list of strings with a separator.

```python
a = "first"
b = "second"
print(a + b)  # Output: firstsecond
print(" ".join([a, b, b, a]))  # Output: first second second first
```

### String Formatting

Python provides several ways to format strings:

- **Old style (`%` operator):**
  ```python
  print("%i plus %i is equal to %i" % (1, 3, 4))
  print("%.1f %.2f %.3f" % (1.6, 1.7, 1.8))
  ```
- **`str.format()` method:**
  ```python
  print("{} plus {} is equal to {}".format(1, 3, 4))
  print("{:.1f} {:.2f} {:.3f}".format(1.6, 1.7, 1.8))
  ```
- **f-strings (Python 3.6+):**
  ```python
  print(f"{1} plus {3} is equal to {4}")
  print(f"{1.6:.1f} {1.7:.2f} {1.8:.3f}")
  ```

### Print Function

- By default, `print()` adds a newline. Use `end=""` to avoid this:
  ```python
  print("text", end="")
  print("more text")  # Output: textmore text
  ```

---

## 3. Functions and Arguments

### Defining Functions and Docstrings

Functions are defined using the `def` keyword. The first string in a function body is its docstring, which describes what the function does.

```python
def double(x):
    "This function multiplies its argument by two."
    return x * 2

print(double(4), double(1.2), double("abc"))  # Works for numbers and strings
print("The docstring is:", double.__doc__)
help(double)
```

### Variable-Length Arguments

- Use `*args` to accept any number of positional arguments (packed into a tuple).
- Use `**kwargs` to accept any number of keyword arguments (packed into a dictionary).

```python
def sum_of_squares(*t):
    "Computes the sum of squares of arbitrary number of arguments"
    s = 0
    for x in t:
        s += x ** 2
    return s

print(sum_of_squares(-2))
print(sum_of_squares(-2, 4, 5))
```

- The `*` operator can also unpack iterables into function arguments.

```python
def length(*t, degree=2):
    """Computes the length of the vector given as parameter. By default, it computes
    the Euclidean distance (degree==2)"""
    s = 0
    for x in t:
        s += abs(x) ** degree
    return s ** (1 / degree)

print(length(-4, 3))
print(length(-4, 3, degree=3))
```

---

## 4. Variable Scope

- Variables defined outside functions are **global**.
- Assigning to a variable inside a function creates a **local** variable unless declared `global`.

```python
i = 2           # global variable
def f():
    i = 3       # local variable
    print(i)    # Prints 3
f()
print(i)        # Prints 2

# To modify a global variable inside a function:
i = 2
def f():
    global i
    i = 5
    print(i)    # Prints 5
f()
print(i)        # Prints 5
```

---

## 5. Lists and Ranges

- `range(n)` creates a range object (not a list). Use `list(range(n))` to get a list.
- Lists are mutable sequences.

```python
L = range(3)
for i in L:
    print(i)
print(L)  # Output: range(0, 3)
print(list(range(0, 7, 2)))  # Output: [0, 2, 4, 6]
```

### Sorting

- `.sort()` sorts a list in place.
- `sorted()` returns a new sorted list.

```python
L = [5, 3, 7, 1]
L.sort()
print(L)  # Output: [1, 3, 5, 7]
L2 = [6, 1, 7, 3, 6]
print(sorted(L2))  # Output: [1, 3, 6, 6, 7]
print(L2)          # Output: [6, 1, 7, 3, 6]
print(sorted(L2, reverse=True))  # Output: [7, 6, 6, 3, 1]
```

---

## 6. Zipping and Enumerating

### zip()

- Combines multiple sequences into tuples.
- Use `zip(*lists)` to unpack a list of lists for zipping.

```python
L1 = [1, 2, 3]
L2 = ["first", "second", "third"]
print(list(zip(L1, L2)))  # Output: [(1, 'first'), (2, 'second'), (3, 'third')]
```

### enumerate()

- Yields pairs of (index, value).

```python
L = [1, 2, 98, 5, -1, 2, 0, 5, 10]
counter = 0
for i, x in enumerate(L):
    if x == 5:
        counter += 1
        if counter == 2:
            break
print(i)  # Prints the index of the second occurrence of 5
```

---

## 7. Dictionaries

- Dictionaries store key-value pairs. Keys must be hashable (immutable).
- Common methods: `.copy()`, `.items()`, `.keys()`, `.values()`, `.get()`, `.update()`, `.pop()`, `.popitem()`, `.setdefault()`.

```python
d = {"key1": "value1", "key2": "value2"}
print(d["key1"])
print(d["key2"])
print(d.items())
```

### Dictionary Comprehension

```python
d = {k: k**2 for k in range(10)}
print(d)
```

### Reverse Dictionary

```python
def reverse_dictionary(d):
    dict_r = {}
    for key, values in d.items():
        for value in values:
            if value not in dict_r:
                dict_r[value] = [key]
            else:
                dict_r[value].append(key)
    return dict_r
```

---

## 8. Sets

- Sets are unordered collections of unique, hashable elements.
- Set operations: union (`|`), intersection (`&`), difference (`-`), symmetric difference (`^`).

```python
s = {1, 1, 2}
print(s)  # Output: {1, 2}
s = set([1, 2, 2, 'a'])
print(s)  # Output: {1, 2, 'a'}
s = "mississippi"
print(f"There are {len(set(s))} distinct characters in {s}")
```

### Set Methods

- Non-mutating: `.copy()`, `.issubset()`, `.issuperset()`, `.union()`, `.intersection()`, `.difference()`, `.symmetric_difference()`
- Mutating: `.add()`, `.clear()`, `.discard()`, `.pop()`, `.remove()`

```python
s = set([1, 2, 7])
t = set([2, 8, 9])
print("Union:", s | t)
print("Intersection:", s & t)
print("Difference:", s - t)
print("Symmetric difference", s ^ t)
```

---

## 9. Comprehensions

### List Comprehension

- `[expression for element in iterable if condition]`

```python
L = [a**3 for a in range(1, 11)]
print(L)
```

### Dictionary and Set Comprehension

```python
d = {k: k**2 for k in range(10)}
print(d)
s = {i*j for i in range(10) for j in range(10)}
print(s)
```

### Generator Expressions

- Use parentheses instead of brackets.
- More memory efficient for large data.

```python
G = (100*a + 10*b + c for a in range(0, 10)
                        for b in range(0, 10)
                        for c in range(0, 10)
                        if a <= b <= c)
print(sum(G))
```

---

## 10. Functional Programming Tools

### map()

- Applies a function to each item in an iterable.

```python
def double(x):
    return 2 * x
L = [12, 4, -1]
print(list(map(double, L)))
```

### filter()

- Filters items by a function returning True/False.

```python
def is_odd(x):
    return x % 2 == 1
L = [1, 4, 5, 9, 10]
print(list(filter(is_odd, L)))
print([l**2 for l in L if is_odd(l)])  # List comprehension alternative
```

### reduce()

- Reduces a sequence to a single value by repeatedly applying a function.

```python
from functools import reduce
L = [1, 2, 3, 4]
print(reduce(lambda x, y: x + y, L, 0))
print(reduce(lambda x, y: x * y, L, 1))
```

### lambda Expressions

- Anonymous functions, often used with `map`, `filter`, and `reduce`.

```python
L = [2, 3, 5]
print(list(map(lambda x: x**2 + 2*x, L)))
```

---

## 11. String Methods

### strip, lstrip, rstrip

- Remove whitespace or specified characters from the ends of a string.

```python
s = "  hello world!  "
print(s.strip())  # Output: 'hello world!'
s2 = "xxxyhelloxyx"
print(s2.strip('xy'))  # Output: 'hello'
print(s.lstrip())
print(s2.lstrip('xy'))
print(s.rstrip())
print(s2.rstrip('xy'))
```

### rjust, ljust, center

- Align strings within a field of a given width.

```python
s1 = "hello"
print(s1.rjust(10, '-'))  # Output: '-----hello'
print(s1.ljust(10, '-'))  # Output: 'hello-----'
print(s1.center(11, '-')) # Output: '---hello---'
```

### join and split

- `join(seq)` joins strings in a sequence with a separator.
- `split(sep)` splits a string into a list of substrings.

```python
print("--".join(["abc", "def", "ghi"]))  # Output: 'abc--def--ghi'
print('abc--def--ghi'.split("--"))       # Output: ['abc', 'def', 'ghi']
```

---

## 12. Unpacking and Membership

- Unpack elements of a container into variables:

```python
first, second = [4, 5]
a, b, c = "bye"
print(c)  # Output: 'e'
d = dict(a=1, b=3)
key1, key2 = d
print(key1, key2)  # Output: 'a b'
for key, value in d.items():
    print(f"For key '{key}' value {value} was stored")
```

- Membership test with `in`:

```python
print(1 in [1, 2])  # Output: True
print("misi" in "misissipi")  # Output: True
print("miss" in "msisiccpi")  # Output: False
```

---

## 13. Deleting Variables

- Use `del` to remove the binding of a variable.

```python
s = "hello"
del s
```

---

## 14. Example Functions

### sum_equation

Returns a string showing the sum of a list as an equation.

```python
def sum_equation(L):
    if not L:
        return "0 = 0"
    equation = " + ".join(map(str, L))
    equation += f" = {sum(L)}"
    print(equation)
    return equation

sum_equation([1, 5, 7])  # Output: '1 + 5 + 7 = 13'
```

### distinct_characters

Returns a dictionary mapping each string in the list to the number of distinct characters it contains.

```python
def distinct_characters(L):
    d = {}
    for item in L:
        val = item
        leng = len(set(item))
        d.update({val: leng})
    return d

print(distinct_characters(["check", "look", "try", "pop"]))
```

### reverse_dictionary

Reverses a dictionary of lists, so that each value becomes a key mapping to a list of original keys.

```python
def reverse_dictionary(d):
    dict_r = {}
    for key, values in d.items():
        for value in values:
            if value not in dict_r:
                dict_r[value] = [key]
            else:
                dict_r[value].append(key)
    return dict_r
```

---

## 15. List, Set, and Dictionary Comprehensions

- **List comprehension**: `[x**2 for x in range(10)]`
- **Dictionary comprehension**: `{k: k**2 for k in range(10)}`
- **Set comprehension**: `{i*j for i in range(10) for j in range(10)}`
- **Generator expression**: `(x for x in range(10))`

Comprehensions can include conditions and multiple loops for more complex constructions.

---

## 16. Advanced String Processing

### Acronyms Extraction

Extracts acronyms (all-uppercase words of length >= 2) from a string, ignoring punctuation.

```python
def acronyms(s):
    ll = []
    lis = s.split()
    for l in lis:
        correct = ''.join(filter(str.isalnum, l))
        if len(correct) >= 2 and correct.isupper():
            ll.append(correct)
    return ll

from string import punctuation
def acronyms2(s):
    L = [x.strip(punctuation) for x in s.split()]
    return [x for x in L if x.isupper() and len(x) >= 2]
```

---

## 17. Miscellaneous

- **Immutability**: Strings are immutable in Python. You cannot change them in place.
- **Help and Documentation**: Use `help()` to get documentation on functions, methods, and types.
- **Performance**: List comprehensions and generator expressions are preferred for concise and efficient code.

---

## 18. Practical Examples

### Histogram Printing

Prints a histogram using string multiplication and centering.

```python
L = [1, 3, 5, 7, 9, 1, 1]
print('-' * 11)
for i in L:
    s = '*' * i
    print(f"|{s.center(9)}|")
print('-' * 11)
```

### Interleaving Lists

Combines multiple lists by interleaving their elements.

```python
def interleave(*lists):
    my_list = []
    for group in zip(*lists):
        my_list.extend(group)
    return my_list
```

### Transforming and Multiplying Lists

Transforms two space-separated strings of numbers into lists, multiplies corresponding elements.

```python
def transform(s1, s2):
    L1 = list(map(int, s1.split()))
    L2 = list(map(int, s2.split()))
    return [a * b for a, b in zip(L1, L2)]
```

---

## 19. Summary Table: Key Concepts

| Concept         | What It Does                                   | Example                                      |
|-----------------|------------------------------------------------|----------------------------------------------|
| `*lists`        | Collects all positional args into a tuple      | `def f(*lists):`                             |
| `zip`           | Groups elements from multiple iterables        | `zip([1,2], ['a','b'])` → (1,'a'), ...       |
| `zip(*lists)`   | Unpacks a list/tuple of lists for zip          | `zip(*[[1,2], [3,4]])`                       |
| `enumerate`     | Yields (index, value) pairs                    | `for i, x in enumerate(L): ...`              |
| `map`           | Applies a function to each item                | `map(str, [1,2,3])` → ['1','2','3']          |
| `filter`        | Filters items by a function                    | `filter(is_odd, [1,2,3])` → [1,3]            |
| `reduce`        | Reduces a sequence to a single value           | `reduce(lambda x,y: x+y, [1,2,3], 0)` → 6    |
| List comp.      | Creates a list from an expression              | `[x**2 for x in range(5)]`                   |
| Dict comp.      | Creates a dict from an expression              | `{x: x**2 for x in range(5)}`                |
| Set comp.       | Creates a set from an expression               | `{x**2 for x in range(5)}`                   |
| Generator exp.  | Creates a generator from an expression         | `(x**2 for x in range(5))`                   |

---

## 20. Conclusion

This document has covered a wide range of Python programming concepts, from basic string handling and formatting to advanced data structures and functional programming tools. Mastery of these topics is essential for effective data analysis, scripting, and general-purpose programming in Python. The examples provided illustrate both the syntax and the practical use cases for each concept, serving as a reference for both beginners and experienced programmers.

---