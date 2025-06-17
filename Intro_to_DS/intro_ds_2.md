# Notes: Python Regex and File Handling

---

## Regular Expressions (Regex)

### Basics
- **Regex** is a way to search for patterns in text.
- **Common functions:**
  - `re.match(pattern, string)`: Checks for a match only at the beginning of the string.
  - `re.search(pattern, string)`: Searches for the first location where the pattern matches.
  - `re.findall(pattern, string)`: Returns all non-overlapping matches of pattern in string as a list.
  - `re.finditer(pattern, string)`: Returns an iterator yielding match objects for all matches.
  - `re.sub(pattern, repl, string)`: Replaces matches with `repl`.

### Special Characters
- `\b`: Word boundary (start/end of a word).
- `\w`: Any word character (a-z, A-Z, 0-9, _).
- `\d`: Any digit.
- `.`: Any character except newline.
- `*`, `+`, `?`: Quantifiers (0 or more, 1 or more, 0 or 1).
- `[]`: Character set.
- `()`: Grouping.

### Grouping and Backreferences
- Parentheses `()` create **groups**.
- `group(0)`: The entire match.
- `group(1)`, `group(2)`, ...: The content matched by each group.
- In `re.sub`, you can use `\1`, `\2`, ... to refer to groups in the replacement string.
- Example:
  ```python
  s = "hello world"
  print(re.sub(r'(\w+) (\w+)', r'\2 \1', s))  # Output: world hello
  ```

### Greedy vs Non-Greedy
- `.*` is greedy (matches as much as possible).
- `.*?` is non-greedy (matches as little as possible).

### Examples from the File

```python
import re

# Add text after "He" or "he"
s = "He is a timelord."
print(re.sub(r'(\b[Hh]e\b)', r'\1 (The Doctor)', s))
# Output: He (The Doctor) is a timelord.

# Repeat the matched word
s = "cat"
print(re.sub(r'(cat)', r'\1 \1', s))
# Output: cat cat

# Swap two words
s = "hello world"
print(re.sub(r'(\w+) (\w+)', r'\2 \1', s))
# Output: world hello

# Match repeated group
s = "abcabc"
print(bool(re.match(r'(abc)\1', s)))
# Output: True
```

---

## File Handling in Python

### Opening Files
- `open(filename, mode)`: Opens a file.
  - Modes: `"r"` (read), `"w"` (write), `"a"` (append), `"b"` (binary), `"t"` (text, default).
- Always close files with `f.close()` or use a context manager (`with` statement).

### Reading Files
- `f.read()`: Reads the whole file as a string.
- `f.readline()`: Reads one line at a time.
- `f.readlines()`: Reads all lines into a list.

### Writing Files
- `f.write(string)`: Writes a string to the file.

### Context Manager
```python
with open("file.txt", "r") as f:
    for line in f:
        print(line)
# File is automatically closed after the block.
```

---

## Example Functions from the File

### 1. File Extensions

```python
def file_extensions(filename):
    ll = []
    dd = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for l in lines:
            l = l.strip()
            if '.' not in l:
                ll.append(l)
            else:
                dp = l.split(".")[-1]
                if dp not in dd:
                    dd[dp] = []
                dd[dp].append(l.strip())
    return (ll, dd)
```
- **Purpose:**  
  - Returns a tuple:  
    - `ll`: list of lines without a dot (no extension).
    - `dd`: dictionary mapping file extensions to lists of filenames.

---

### 2. Word Frequencies

```python
def word_frequencies(filename):
    di = {}
    with open(filename, 'r') as f:
        ls = f.read().split()
        for l in ls:
            l = l.strip("""!"#$%&'()*,-./:;?@[]_""")
            if l not in di.keys():
                di[l] = 1
            else:
                di[l] += 1
    return di
```
- **Purpose:**  
  - Counts how many times each word appears in a file (ignoring punctuation).

---

### 3. File Count

```python
def file_count(filename):
    line_count = 0
    char_count = 0
    word_count = 0
    with open(filename, 'r') as f:
        content = f.read()
    lines = content.splitlines()
    line_count = len(lines)
    for line in lines:
        word_in_line = line.split()
        word_count += len(word_in_line)
    char_count = len(content)
    return (line_count, word_count, char_count)
```
- **Purpose:**  
  - Returns the number of lines, words, and characters in a file.

---

### 4. Summary (Sum, Mean, Stddev)

```python
def summary(filename):
    sum = 0
    count = 0
    std = 0
    mean = 0
    sqr = 0
    with open(filename, 'r') as f:
        lines = []
        for line in f:
            try:
                lines.append(float(line))
            except ValueError:
                continue 
        for l in lines:
            sum += float(l)
            count += 1
            mean = sum / count
        for p in lines:
            sqr = (float(p) - mean) ** 2
            std += sqr
        std = std / (count - 1)
        std = std ** 0.5
    return (sum, mean, std)
```
- **Purpose:**  
  - Reads numbers from a file and returns their sum, mean, and standard deviation.

---

## Miscellaneous

- `.append(x)` adds the entire object `x` as a single element to the list.
- `.extend(x)` takes an iterable `x` and adds each element of `x` to the list.

---

## Regex Example: Email Extraction

```python
s = "Alice: alice@example.com, Bob: bob@example.com"
for mo in re.finditer(r'(\w+)@(\w+)\.(\w+)', s):
    print(f"Email: {mo.group(0)}")
    print(f"Username: {mo.group(1)}")
    print(f"Domain: {mo.group(2)}")
    print(f"TLD: {mo.group(3)}")
    print(f"Position: {mo.span(0)}")
```
- **Purpose:**  
  - Finds all email addresses in the string and prints their components and positions.

---

## Key Takeaways

- Use regex for powerful text searching and manipulation.
- Use file handling functions to read, write, and process files efficiently.
- Grouping in regex allows you to extract and rearrange parts of matches.
- Always close files or use a context manager to avoid resource leaks.

---