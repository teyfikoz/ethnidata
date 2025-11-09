# API Reference

## NBD Class

Main class for name-based demographic predictions.

### Constructor

```python
NBD(db_path: Optional[str] = None)
```

**Parameters:**
- `db_path` (str, optional): Path to SQLite database. If None, uses default location.

**Raises:**
- `FileNotFoundError`: If database not found

**Example:**
```python
from nbd import NBD

# Use default database
nbd = NBD()

# Use custom database
nbd = NBD(db_path="/path/to/custom.db")
```

---

### Methods

#### `predict_nationality()`

Predict nationality from a name.

```python
predict_nationality(
    name: str,
    name_type: Literal["first", "last"] = "first",
    top_n: int = 5
) -> Dict
```

**Parameters:**
- `name` (str): First or last name
- `name_type` (str): Either "first" or "last" (default: "first")
- `top_n` (int): Number of top predictions to return (default: 5)

**Returns:**
```python
{
    'name': str,              # Normalized name
    'country': str,           # ISO 3166-1 alpha-3 code (e.g., 'USA')
    'country_name': str,      # Full country name
    'confidence': float,      # Confidence score (0-1)
    'top_countries': [
        {
            'country': str,
            'country_name': str,
            'probability': float,
            'frequency': int
        },
        ...
    ]
}
```

**Example:**
```python
result = nbd.predict_nationality("Ahmet", name_type="first", top_n=3)
print(result)
# {
#   'name': 'ahmet',
#   'country': 'TUR',
#   'country_name': 'Turkey',
#   'confidence': 0.89,
#   'top_countries': [...]
# }
```

---

#### `predict_ethnicity()`

Predict ethnicity from a name.

```python
predict_ethnicity(
    name: str,
    name_type: Literal["first", "last"] = "first"
) -> Dict
```

**Parameters:**
- `name` (str): First or last name
- `name_type` (str): Either "first" or "last"

**Returns:**
```python
{
    'name': str,
    'ethnicity': Optional[str],  # May be None if not available
    'country': str,
    'country_name': str,
    'frequency': int             # How common this name-ethnicity pair is
}
```

**Note:** Ethnicity data is only available where source data included it (primarily Wikipedia/Wikidata).

**Example:**
```python
result = nbd.predict_ethnicity("Muhammad", name_type="first")
print(result)
# {
#   'name': 'muhammad',
#   'ethnicity': 'Arab',
#   'country': 'SAU',
#   'country_name': 'Saudi Arabia',
#   'frequency': 1234
# }
```

---

#### `predict_full_name()`

Predict nationality from full name (combines first + last name predictions).

```python
predict_full_name(
    first_name: str,
    last_name: str,
    top_n: int = 5
) -> Dict
```

**Parameters:**
- `first_name` (str): First name
- `last_name` (str): Last name
- `top_n` (int): Number of top predictions

**Returns:**
```python
{
    'first_name': str,
    'last_name': str,
    'country': str,
    'country_name': str,
    'confidence': float,
    'top_countries': [...]
}
```

**Methodology:**
- First name contributes 40% to final score
- Last name contributes 60% to final score
- Scores are combined and normalized

**Example:**
```python
result = nbd.predict_full_name("Wei", "Chen", top_n=5)
print(result)
# {
#   'first_name': 'wei',
#   'last_name': 'chen',
#   'country': 'CHN',
#   'country_name': 'China',
#   'confidence': 0.92,
#   'top_countries': [...]
# }
```

---

#### `get_stats()`

Get database statistics.

```python
get_stats() -> Dict
```

**Returns:**
```python
{
    'total_first_names': int,    # Total first name entries
    'total_last_names': int,     # Total last name entries
    'countries_first': int,      # Unique countries in first names
    'countries_last': int        # Unique countries in last names
}
```

**Example:**
```python
stats = nbd.get_stats()
print(stats)
# {
#   'total_first_names': 123456,
#   'total_last_names': 234567,
#   'countries_first': 195,
#   'countries_last': 198
# }
```

---

#### `normalize_name()` (static)

Normalize a name for database lookup.

```python
@staticmethod
normalize_name(name: str) -> str
```

**Parameters:**
- `name` (str): Name to normalize

**Returns:**
- Normalized name (lowercase, Unicode-normalized)

**Example:**
```python
normalized = NBD.normalize_name("José")
print(normalized)  # "jose"

normalized = NBD.normalize_name("Müller")
print(normalized)  # "muller"
```

---

## Database Schema

### Tables

#### `first_names`
```sql
CREATE TABLE first_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    ethnicity TEXT,
    source TEXT,
    frequency INTEGER DEFAULT 1,
    UNIQUE(name, country_code)
)
```

#### `last_names`
```sql
CREATE TABLE last_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    ethnicity TEXT,
    source TEXT,
    frequency INTEGER DEFAULT 1,
    UNIQUE(name, country_code)
)
```

#### `countries`
```sql
CREATE TABLE countries (
    country_code TEXT PRIMARY KEY,
    country_name TEXT,
    region TEXT,
    population INTEGER
)
```

### Indexes

- `idx_first_name` on `first_names(name)`
- `idx_last_name` on `last_names(name)`
- `idx_first_country` on `first_names(country_code)`
- `idx_last_country` on `last_names(country_code)`

---

## Error Handling

### Common Errors

**FileNotFoundError**
```python
try:
    nbd = NBD()
except FileNotFoundError as e:
    print("Database not found. Run scripts/6_create_database.py")
```

**Unknown Name**
```python
result = nbd.predict_nationality("XxXUnknownXxX")
print(result['country'])  # None
print(result['confidence'])  # 0.0
```

---

## Best Practices

### 1. Singleton Pattern

```python
# Create once, reuse
_nbd_instance = None

def get_nbd():
    global _nbd_instance
    if _nbd_instance is None:
        _nbd_instance = NBD()
    return _nbd_instance

# Use
nbd = get_nbd()
```

### 2. Batch Processing

```python
import pandas as pd

nbd = NBD()

# Process dataframe
def predict_batch(df):
    df['country'] = df.apply(
        lambda row: nbd.predict_full_name(
            row['first_name'],
            row['last_name']
        )['country'],
        axis=1
    )
    return df
```

### 3. Caching

```python
from functools import lru_cache

nbd = NBD()

@lru_cache(maxsize=10000)
def cached_predict(name, name_type):
    return nbd.predict_nationality(name, name_type)
```

---

## Performance

- **Database size**: ~50-500 MB (depends on data sources)
- **Query time**: <1ms per lookup (SQLite with indexes)
- **Memory**: ~10-50 MB (database kept in memory by OS)
- **Batch processing**: ~1000-10000 names/second

---

## Limitations

1. **Name variations**: "Jon" vs "John" may give different results
2. **Transliteration**: "Мария" vs "Maria" are different
3. **Spelling**: "Muhammad" vs "Mohammed" vs "Mohamed"
4. **Context**: Doesn't account for location or other metadata

**Recommendation**: Use with other signals (IP geolocation, language preference, etc.)
