# Publishing ethnidata to PyPI

This guide explains how to publish ethnidata to PyPI using GitHub Actions and Trusted Publishers.

## Prerequisites

1. PyPI account at https://pypi.org/
2. GitHub repository with workflow file
3. Package already exists on PyPI: https://pypi.org/project/ethnidata/

## Trusted Publisher Configuration

### PyPI Settings

1. Go to https://pypi.org/manage/project/ethnidata/settings/publishing/
2. Scroll to "Add a new publisher"
3. Select **GitHub** tab
4. Fill in the form:

   ```
   PyPI Project Name: ethnidata
   Owner: teyfikoz
   Repository name: ethnidata
   Workflow name: publish.yml
   Environment name: pypi
   ```

5. Click **Add**

### GitHub Environment

1. Go to https://github.com/teyfikoz/ethnidata/settings/environments
2. Click **New environment**
3. Name: `pypi`
4. Protection rules (optional but recommended):
   - Required reviewers: Add yourself
   - Deployment branches: `main` or `master` only

## Publishing a New Version

### 1. Update Version

Edit `pyproject.toml`:

```toml
[project]
version = "3.1.0"  # Increment version
```

### 2. Commit Changes

```bash
git add pyproject.toml
git commit -m "Bump version to 3.1.0"
git push
```

### 3. Create Release

```bash
# Create and push tag
git tag -a v3.1.0 -m "Release version 3.1.0"
git push origin v3.1.0
```

### 4. Create GitHub Release

1. Go to https://github.com/teyfikoz/ethnidata/releases/new
2. Choose tag: `v3.1.0`
3. Release title: `ethnidata v3.1.0`
4. Description: Add changelog
5. Click **Publish release**

The GitHub Action will automatically build and publish to PyPI!

## Monitoring

- Watch the workflow: https://github.com/teyfikoz/ethnidata/actions
- Check PyPI: https://pypi.org/project/ethnidata/

## Troubleshooting

**Error: "Trusted publisher not configured"**
- Add the publisher in PyPI project settings first

**Error: "Environment not found"**
- Create `pypi` environment in GitHub settings

**Error: "Version already exists"**
- Increment version number in `pyproject.toml`

## Security Notes

- No API tokens needed with Trusted Publishers
- OpenID Connect provides secure authentication
- GitHub environment adds extra protection layer
