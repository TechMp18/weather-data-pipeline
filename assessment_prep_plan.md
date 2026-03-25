# 📝 Highspring India — Assessment Preparation Plan

> Test kabhi bhi ho sakta hai, toh yeh plan **priority order** mein hai — sab se important topics pehle!

---

## 🔴 Week 1: Must-Know Basics (Daily 2-3 hours)

### Day 1-2: Python Fundamentals
| Topic | Kya seekhna hai | Resources |
|---|---|---|
| Variables & Data Types | int, float, str, list, dict, set, tuple | [W3Schools Python](https://www.w3schools.com/python/) |
| Control Flow | if/else, for, while, break, continue | Practice 10 problems |
| Functions | def, parameters, return, *args, **kwargs | Practice 5 problems |
| List Comprehension | `[x for x in range(10) if x%2==0]` | Very frequently asked! |
| String Methods | split, join, strip, replace, find, format | |

**Practice:** [HackerRank Python](https://www.hackerrank.com/domains/python) — Easy section (do 15-20 problems)

### Day 3-4: Data Structures & Algorithms (Basic)
| Topic | What to focus on |
|---|---|
| Arrays/Lists | Sorting, searching, two-pointer technique |
| Strings | Reverse, palindrome, anagram, character frequency |
| Dictionary/HashMap | Counting, grouping, lookup patterns |
| Sets | Union, intersection, difference (ye tumne Resume Analyser mein use kiya hai!) |
| Stack & Queue | Basic push/pop patterns, bracket matching |

**Practice:** [LeetCode Easy](https://leetcode.com/problemset/) — Do 2-3 problems daily (Solve in Python)

### Day 5-6: SQL (Bahut Important for Data Engineer!)
| Topic | Example |
|---|---|
| SELECT, WHERE, ORDER BY | `SELECT * FROM users WHERE age > 25 ORDER BY name` |
| GROUP BY, HAVING | `SELECT city, COUNT(*) FROM users GROUP BY city HAVING COUNT(*) > 5` |
| JOINs | INNER JOIN, LEFT JOIN, RIGHT JOIN — diagram draw karke samjho! |
| Aggregate Functions | COUNT, SUM, AVG, MIN, MAX |
| Subqueries | Query ke andar query |
| CREATE, INSERT, UPDATE, DELETE | Basic CRUD operations |

**Practice:** [SQLZoo](https://sqlzoo.net/) or [HackerRank SQL](https://www.hackerrank.com/domains/sql) — Easy + Medium (do 15-20 problems)

### Day 7: Linux/Unix Commands
| Command | Kya karta hai | Example |
|---|---|---|
| `ls` | Files list karta hai | `ls -la` (all files with details) |
| `cd` | Directory change | `cd /home/user/docs` |
| `pwd` | Current location | Just type `pwd` |
| `cat` | File ka content dikhata hai | `cat file.txt` |
| `grep` | Text search karta hai | `grep "error" logfile.txt` |
| `chmod` | File permissions change | `chmod 755 script.sh` |
| `mkdir/rm` | Folder create/delete | `mkdir new_folder` |
| `cp/mv` | Copy/Move files | `cp file1.txt backup/` |
| `head/tail` | File ke first/last lines | `tail -n 20 logfile.txt` |
| `pipe \|` | Commands ko connect karta hai | `cat file.txt \| grep "error" \| wc -l` |
| `>` / `>>` | Output ko file mein save | `echo "hello" > file.txt` |

**Practice:** [Linux Survival](https://linuxsurvival.com/) — complete all 4 modules

---

## 🟡 Week 2: Core Technical Skills (Daily 2-3 hours)

### Day 8-9: HTML, CSS, JavaScript Basics
| Topic | Key Concepts |
|---|---|
| HTML | Tags (div, p, h1-h6, a, img, table, form, input), Semantic HTML |
| CSS | Selectors, Box Model, Flexbox, Position, Display |
| JavaScript | Variables (let/const/var), Functions, Arrays, Objects, DOM manipulation |
| JS Advanced | Promises, async/await, fetch API, JSON.parse/stringify |

**Practice:** Build a simple calculator in HTML/JS (30 min exercise)

### Day 10-11: Data Engineering Concepts
| Topic | Kya samajhna hai |
|---|---|
| ETL vs ELT | Extract-Transform-Load vs Extract-Load-Transform — difference & when to use |
| Data Pipeline | Data ek jagah se dusri jagah jaata hai in steps, with error handling |
| Batch vs Stream | Batch = ek saath (daily), Stream = real-time (har second) |
| Data Warehouse | Bada database jo analytics ke liye optimized hai (Snowflake, BigQuery) |
| Data Lake | Raw data ka storage (S3, HDFS) — structure nahi hoti |
| Data Quality | Null values, duplicates, type checking — data clean hona chahiye |
| Idempotency | Pipeline dobara run karo toh same result aaye |
| Schema | Database ka structure — columns aur unke types |

### Day 12-13: Version Control (Git)
| Command | Kya karta hai |
|---|---|
| `git init` | New repo start |
| `git add .` | Changes ko stage karo |
| `git commit -m "msg"` | Changes save karo |
| `git push` | GitHub pe upload |
| `git pull` | GitHub se download |
| `git branch` | New branch banao |
| `git merge` | Branches combine karo |
| `git log` | History dekho |

### Day 14: Mock Test Day
- Time yourself: 60 min, 30 MCQ questions
- Topics: Python output, SQL queries, Linux commands, HTML/CSS, basic DSA
- Resources for mock tests:
  - [GeeksforGeeks MCQ](https://www.geeksforgeeks.org/quiz-corner-gq/)
  - [IndiaBIX](https://www.indiabix.com/)

---

## 🟢 Week 3: Advanced + Interview Prep

### Day 15-16: Python Advanced
- File handling (`open`, `read`, `write`, `with` statement)
- Exception handling (`try/except/finally`)
- OOP basics (class, object, inheritance, `__init__`)
- Libraries: `pandas` basics, `json`, `os`, `sys`

### Day 17-18: Problem Solving
- Do 3 LeetCode Easy daily
- Focus patterns: Two Pointers, Sliding Window, HashMap, Sorting
- Practice explaining your approach OUT LOUD (interview mein bolna padega)

### Day 19-20: Communication & HR
- **Tell me about yourself** — 2 min pitch prepare karo
- **Why Data Engineering?** — Tumhare projects se connect karo
- **Project explanation** — Weather Pipeline project ko 3 min mein explain karna seekho
- **Situational questions** — "Tell me about a time you solved a difficult bug"

---

## 🎯 Daily Routine Template

```
Morning (1 hour):  2 LeetCode/HackerRank problems
Afternoon (1 hour): Topic study (SQL/Python/Linux)
Evening (1 hour):  Build & understand the portfolio project
Night (30 min):    Revise what you learned today
```

## ⚡ Quick Revision Cheatsheet (Print & Stick)

### Python One-Liners to Remember
```python
# List comprehension
squares = [x**2 for x in range(10)]

# Dictionary comprehension
word_count = {word: text.count(word) for word in set(text.split())}

# Lambda
sort_by_age = sorted(users, key=lambda u: u['age'])

# String formatting
msg = f"Hello {name}, you scored {score}%"

# File read
data = open("file.txt").read()

# JSON
import json
data = json.loads('{"key": "value"}')
```

### SQL Templates to Remember
```sql
-- Basic query
SELECT col1, col2 FROM table WHERE condition ORDER BY col1 DESC LIMIT 10;

-- Aggregation
SELECT department, COUNT(*), AVG(salary)
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;

-- JOIN
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- Subquery
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

> [!TIP]
> **Golden Rule:** Roz kam se kam 2 coding problems solve karo. Consistency > intensity. Test chahe kal ho ya 3 weeks baad — daily practice se confidence aayega! 💪
