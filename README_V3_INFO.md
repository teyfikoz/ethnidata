# EthniData v3.0.0 - Ultra Database Information

## Database Versions

EthniData offers two database versions:

### v2.0.0 (Default - Included in Package)
- **Records**: 415,734
- **Size**: 75 MB
- **Installation**: Included automatically with `pip install ethnidata`
- **Use case**: Most applications, fast download, lightweight

### v3.0.0 (Optional - Download on Demand)
- **Records**: 5,787,259 (14x larger!)
- **Size**: 1.1 GB
- **Installation**: Manual download
- **Use case**: Maximum accuracy, research, large-scale applications

## How to Use v3.0.0

### Option 1: Programmatic Download
```python
from ethnidata.downloader import download_v3_database

# Download v3.0.0 database (1.1 GB)
db_path = download_v3_database()
print(f"Downloaded to: {db_path}")

# Use it
from ethnidata import EthniData
ed = EthniData(use_v3=True)

result = ed.predict_all("Maria")
# Now using 5.8M records for prediction!
```

### Option 2: Manual Download
1. Download from: https://github.com/teyfikoz/ethnidata/releases/download/v3.0.0/ethnidata_v3.db
2. Place in your ethnidata package directory
3. Use with `EthniData(use_v3=True)`

### Option 3: Direct URL (in code)
```python
import os
import urllib.request
from pathlib import Path

# Download v3 database
v3_url = "https://github.com/teyfikoz/ethnidata/releases/download/v3.0.0/ethnidata_v3.db"
v3_path = Path.home() / ".ethnidata" / "ethnidata_v3.db"
v3_path.parent.mkdir(exist_ok=True)

if not v3_path.exists():
    print("Downloading v3.0.0 database (1.1 GB)...")
    urllib.request.urlretrieve(v3_url, v3_path)
    print("Download complete!")

# Use it
from ethnidata import EthniData
ed = EthniData(db_path=str(v3_path))
```

## Comparison

| Feature | v2.0.0 (Default) | v3.0.0 (Optional) |
|---------|------------------|-------------------|
| Records | 415K | 5.8M |
| Size | 75 MB | 1.1 GB |
| Download Time | Instant | 2-10 minutes |
| Memory Usage | ~100 MB | ~200 MB |
| Query Speed | Fast | Fast |
| Asia Coverage | 14.1% | 34% |
| Africa Coverage | 13.4% | 31% |
| Americas Coverage | 32.3% | 32% |
| Buddhism Records | 6.9K | 1.1M |
| Islam Records | 69.7K | 503K |
| Hinduism Records | 3.9K | 90K |

## Recommendation

- **For most users**: Use v2.0.0 (default) - it's excellent for most use cases
- **For maximum accuracy**: Use v3.0.0 - especially if you work with Asian/African names
- **For production**: Start with v2.0.0, upgrade to v3.0.0 if needed

## Database Location

After installation:
- v2.0.0: `site-packages/ethnidata/ethnidata.db`
- v3.0.0: `site-packages/ethnidata/ethnidata_v3.db` (after download)

Find it programmatically:
```python
from ethnidata import EthniData
ed = EthniData()
print(f"Database location: {ed.db_path}")
```

## Storage Requirements

Make sure you have enough disk space:
- Package installation: ~100 MB (includes v2.0.0)
- With v3.0.0: ~1.2 GB total

## Performance

Both versions offer excellent query performance:
- Single prediction: ~0.001s
- Batch (1000 names): ~1s
- Memory efficient: Queries don't load entire DB into RAM

The performance difference between v2 and v3 is negligible for individual queries.
