# TOON (Token Oriented Object Notation)

Token-Oriented Object Notation is a compact, human-readable encoding of the JSON data model that minimizes tokens and makes structure easy for models to follow. It's intended for LLM input as a drop-in, lossless representation of your existing JSON.

TOON combines **YAML's** indentation-based structure for nested objects with a **CSV-style** tabular layout for uniform arrays.
TOON's sweet spot is uniform arrays of objects (multiple fields per row, same structure across items), achieving CSV-like compactness while adding explicit structure that helps LLMs parse and validate data reliably.

## **Why TOON?**

Standard JSON is verbose and token-expensive. For uniform arrays of objects, JSON repeats every field name for every record

```bash
{
  "users": [
    { "id": 1, "name": "Alice", "role": "admin" },
    { "id": 2, "name": "Bob", "role": "user" }
  ]
}
```

YAML already reduces some redundancy with indentation instead of braces

```bash
users:
  - id: 1
    name: Alice
    role: admin
  - id: 2
    name: Bob
    role: user
```

TOON goes further by declaring fields once and streaming data as rows:

```bash
users[2]{id,name,role}:
  1,Alice,admin
  2,Bob,user
```

The [2] declares the array length, enabling LLMs to answer dataset size questions and detect truncation. The `{id,name,role}` declares the field names. Each row is then a compact, comma-separated list of values. This is the core pattern: declare structure once, stream data compactly. The format approaches CSV's efficiency while adding explicit structure.

### More robust dataset examples on JSON and TOON

**JSON (235 tokens)**

```bash
{
  "context": {
    "task": "Our favorite hikes together",
    "location": "Boulder",
    "season": "spring_2025"
  },
  "friends": ["ana", "luis", "sam"],
  "hikes": [
    {
      "id": 1,
      "name": "Blue Lake Trail",
      "distanceKm": 7.5,
      "elevationGain": 320,
      "companion": "ana",
      "wasSunny": true
    },
    {
      "id": 2,
      "name": "Ridge Overlook",
      "distanceKm": 9.2,
      "elevationGain": 540,
      "companion": "luis",
      "wasSunny": false
    },
    {
      "id": 3,
      "name": "Wildflower Loop",
      "distanceKm": 5.1,
      "elevationGain": 180,
      "companion": "sam",
      "wasSunny": true
    }
  ]
}
```

**TOON (106 tokens)**

```bash
context:
  task: Our favorite hikes together
  location: Boulder
  season: spring_2025
friends[3]: ana,luis,sam
hikes[3]{id,name,distanceKm,elevationGain,companion,wasSunny}:
  1,Blue Lake Trail,7.5,320,ana,true
  2,Ridge Overlook,9.2,540,luis,false
  3,Wildflower Loop,5.1,180,sam,true
```

### When to Use TOON

TOON excels with uniform arrays of objects – data with the same structure across items. For LLM prompts, the format produces deterministic, minimally quoted text with built-in validation. Explicit array lengths `([N])` and field headers `({fields})` help detect truncation and malformed data, while the tabular structure declares fields once rather than repeating them in every row.

### When Not to Use TOON

- Deeply nested or non-uniform structures (tabular eligibility ≈ 0%): JSON-compact often uses fewer tokens. Example: complex configuration objects with many nested levels.

- Semi-uniform arrays (~40–60% tabular eligibility): Token savings diminish. Prefer JSON if your pipelines already rely on it.

- Pure tabular data: CSV is smaller than TOON for flat tables. TOON adds minimal overhead (~5-10%) to provide structure (array length declarations, field headers, delimiter scoping) that improves LLM reliability.

- Latency-critical applications: Benchmark on your exact setup. Some deployments (especially local/quantized models) may process compact JSON faster despite TOON's lower token count.

### Below is the output of this demo

```bash
================================================================================
1. Simple Object
================================================================================
JSON (pretty):
{
  "name": "Alice",
  "age": 30,
  "city": "Bengaluru",
  "active": true
}

TOON:
name: Alice
age: 30
city: Bengaluru
active: true

 TOKEN COMPARISON
JSON pretty     :   32 tokens
JSON minified   :   26 tokens
TOON            :   17 tokens
 Savings vs pretty JSON : 15 tokens (46.9%)
 Savings vs minified JSON: 9 tokens (34.6%)
 Lossless round-trip     : YES

 LLM PROMPT — JSON version (copy to test)
Answer the question using ONLY the data below.

Data (JSON):
{
  "name": "Alice",
  "age": 30,
  "city": "Bengaluru",
  "active": true
}

Question: What is the person's city and age?
Answer:

 LLM PROMPT — TOON version (much cheaper)
Answer the question using ONLY the data below.

Data (TOON):
name: Alice
age: 30
city: Bengaluru
active: true

Question: What is the person's city and age?
Answer:

================================================================================
2. Array of Primitives
================================================================================
JSON (pretty):
{
  "colors": [
    "red",
    "green",
    "blue",
    "yellow"
  ]
}

TOON:
colors[4]: red,green,blue,yellow

 TOKEN COMPARISON
JSON pretty     :   25 tokens
JSON minified   :   15 tokens
TOON            :   11 tokens
 Savings vs pretty JSON : 14 tokens (56.0%)
 Savings vs minified JSON: 4 tokens (26.7%)
 Lossless round-trip     : YES

 LLM PROMPT — JSON version (copy to test)
Answer the question using ONLY the data below.

Data (JSON):
{
  "colors": [
    "red",
    "green",
    "blue",
    "yellow"
  ]
}

Question: How many colors are there and what is the last one?
Answer:

 LLM PROMPT — TOON version (much cheaper)
Answer the question using ONLY the data below.

Data (TOON):
colors[4]: red,green,blue,yellow

Question: How many colors are there and what is the last one?
Answer:

================================================================================
3. Uniform Array of Objects (Users)
================================================================================
JSON (pretty):
{
  "users": [
    {
      "id": 1,
      "name": "Alice",
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Bob",
      "role": "user"
    },
    {
      "id": 3,
      "name": "Charlie",
      "role": "moderator"
    }
  ]
}

TOON:
users[3]{id,name,role}:
  1,Alice,admin
  2,Bob,user
  3,Charlie,moderator

 TOKEN COMPARISON
JSON pretty     :   85 tokens
JSON minified   :   59 tokens
TOON            :   33 tokens
 Savings vs pretty JSON : 52 tokens (61.2%)
 Savings vs minified JSON: 26 tokens (44.1%)
 Lossless round-trip     : YES

 LLM PROMPT — JSON version (copy to test)
Answer the question using ONLY the data below.

Data (JSON):
{
  "users": [
    {
      "id": 1,
      "name": "Alice",
      "role": "admin"
    },
    {
      "id": 2,
      "name": "Bob",
      "role": "user"
    },
    {
      "id": 3,
      "name": "Charlie",
      "role": "moderator"
    }
  ]...

 LLM PROMPT — TOON version (much cheaper)
Answer the question using ONLY the data below.

Data (TOON):
users[3]{id,name,role}:
  1,Alice,admin
  2,Bob,user
  3,Charlie,moderator

Question: Who has the 'moderator' role?
Answer:

================================================================================
4. Complex Nested + Array (Hikes — original example)
================================================================================
JSON (pretty):
{
  "context": {
    "task": "Our favorite hikes together",
    "location": "Boulder",
    "season": "spring_2025"
  },
  "friends": [
    "ana",
    "luis",
    "sam"
  ],
  "hikes": [
    {
      "id": 1,
      "name": "Blue Lake Trail",
      "distanceKm": 7.5,
      "elevationGain": 320,
      "companion": "ana",
      "wasSunny": true
    },
    {
      "id": 2,
      "name": "Ridge Overlook"...

TOON:
context:
  task: Our favorite hikes together
  location: Boulder
  season: spring_2025
friends[3]: ana,luis,sam
hikes[3]{id,name,distanceKm,elevationGain,companion,wasSunny}:
  1,Blue Lake Trail,7.5,320,ana,true
  2,Ridge Overlook,9.2,540,luis,false
  3,Wildflower Loop,5.1,180,sam,true

 TOKEN COMPARISON
JSON pretty     :  235 tokens
JSON minified   :  186 tokens
TOON            :  106 tokens
 Savings vs pretty JSON : 129 tokens (54.9%)
 Savings vs minified JSON: 80 tokens (43.0%)
 Lossless round-trip     : YES

 LLM PROMPT — JSON version (copy to test)
Answer the question using ONLY the data below.

Data (JSON):
{
  "context": {
    "task": "Our favorite hikes together",
    "location": "Boulder",
    "season": "spring_2025"
  },
  "friends": [
    "ana",
    "luis",
    "sam"
  ],
  "hikes": [
    {
      "id": 1,
      "name": "Blue Lake Trail",...

 LLM PROMPT — TOON version (much cheaper)
Answer the question using ONLY the data below.

Data (TOON):
context:
  task: Our favorite hikes together
  location: Boulder
  season: spring_2025
friends[3]: ana,luis,sam
hikes[3]{id,name,distanceKm,elevationGain,companion,wasSunny}:
  1,Blue Lake Trail,7.5,320,ana,true
  2,Ridge Overlook,9.2,540,...

================================================================================
5. Large Uniform Array (10 items — biggest savings)
================================================================================
JSON (pretty):
{
  "logs": [
    {
      "id": 1,
      "user": "user1",
      "action": "logout",
      "timestamp": "2025-04-01"
    },
    {
      "id": 2,
      "user": "user2",
      "action": "login",
      "timestamp": "2025-04-02"
    },
    {
      "id": 3,
      "user": "user3",
      "action": "logout",
      "timestamp": "2025-04-03"
    },
    {
      "id": 4,
      "user": "user4",
      "action": ...

TOON:
logs[10]{id,user,action,timestamp}:
  1,user1,logout,2025-04-01
  2,user2,login,2025-04-02
  3,user3,logout,2025-04-03
  4,user4,login,2025-04-04
  5,user5,logout,2025-04-05
  6,user6,login,2025-04-06
  7,user7,logout,2025-04-07
  8,user8,login,2025-04-08
  9,user9,logout,2025-04-09
  10,user10,login,2025-04-010

 TOKEN COMPARISON
JSON pretty     :  389 tokens
JSON minified   :  304 tokens
TOON            :  161 tokens
 Savings vs pretty JSON : 228 tokens (58.6%)
 Savings vs minified JSON: 143 tokens (47.0%)
 Lossless round-trip     : YES

 LLM PROMPT — JSON version (copy to test)
Answer the question using ONLY the data below.

Data (JSON):
{
  "logs": [
    {
      "id": 1,
      "user": "user1",
      "action": "logout",
      "timestamp": "2025-04-01"
    },
    {
      "id": 2,
      "user": "user2",
      "action": "login",
      "timestamp": "2025-04-02"
    },
    {
  ...

 LLM PROMPT — TOON version (much cheaper)
Answer the question using ONLY the data below.

Data (TOON):
logs[10]{id,user,action,timestamp}:
  1,user1,logout,2025-04-01
  2,user2,login,2025-04-02
  3,user3,logout,2025-04-03
  4,user4,login,2025-04-04
  5,user5,logout,2025-04-05
  6,user6,login,2025-04-06
  7,user7,logout,2025-04-07
  8,user8,...

================================================================================
```
