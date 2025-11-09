# Quick Start Guide

## Installation

```bash
pip install nbd-database
```

## Basic Usage

```python
from nbd import NBD

# Initialize
nbd = NBD()

# Predict nationality
result = nbd.predict_nationality("Ahmet")
print(result['country'])  # 'TUR'

# Predict from full name
result = nbd.predict_full_name("John", "Smith")
print(result['country_name'])  # 'United States'
```

## Building from Source

```bash
# 1. Clone repository
git clone https://github.com/yourusername/nbd-database.git
cd nbd-database

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fetch data (takes 10-30 minutes)
cd scripts
python 1_fetch_names_dataset.py
python 2_fetch_wikipedia.py
python 3_fetch_olympics.py
python 4_fetch_phone_directories.py
python 5_merge_all_data.py
python 6_create_database.py

# 4. Install package
cd ..
pip install -e .

# 5. Test it
python examples/demo.py
```

## Common Use Cases

### 1. User Signup Demographics

```python
from nbd import NBD

nbd = NBD()

def analyze_user_signup(first_name, last_name):
    result = nbd.predict_full_name(first_name, last_name, top_n=3)

    return {
        'predicted_country': result['country'],
        'confidence': result['confidence'],
        'alternatives': result['top_countries']
    }

# Example
print(analyze_user_signup("Wei", "Chen"))
```

### 2. Customer Segmentation

```python
import pandas as pd
from nbd import NBD

nbd = NBD()

# Load customer data
customers = pd.read_csv("customers.csv")

# Predict countries
customers['predicted_country'] = customers.apply(
    lambda row: nbd.predict_full_name(
        row['first_name'],
        row['last_name']
    )['country'],
    axis=1
)

# Analyze by country
print(customers['predicted_country'].value_counts())
```

### 3. Content Localization

```python
from nbd import NBD

nbd = NBD()

def suggest_language(name):
    result = nbd.predict_nationality(name, name_type="first", top_n=1)

    # Map country to language
    language_map = {
        'TUR': 'tr',
        'USA': 'en',
        'GBR': 'en',
        'DEU': 'de',
        'FRA': 'fr',
        'ESP': 'es',
        'JPN': 'ja',
        'CHN': 'zh',
    }

    return language_map.get(result['country'], 'en')

# Example
print(suggest_language("Mehmet"))  # 'tr'
print(suggest_language("John"))    # 'en'
```

## Next Steps

- Read the [full documentation](../README.md)
- Check out [examples/demo.py](../examples/demo.py)
- Run the test suite: `pytest tests/`
- Explore the [API reference](API.md)
