# GitHub Repository Setup Guide

This guide will help you set up this tutorial as a public GitHub repository.

## Step 1: Initialize Git Repository

```bash
cd /path/to/3DG_Tutorials
git init
git add .
git commit -m "Initial commit: COX Multiple Regression Tutorial"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it: `3DG_Tutorials`
5. Make it **Public**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

## Step 3: Connect Local Repository to GitHub

```bash
git remote add origin https://github.com/aralap/3DG_Tutorials.git
git branch -M main
git push -u origin main
```

Repository already configured with username: `aralap`

## Step 4: Update README Links

After pushing to GitHub, update the following in `README.md`:

1. All links have been updated with username `aralap`:
   - Colab link: `https://colab.research.google.com/github/aralap/3DG_Tutorials/blob/main/tutorials/COX_Regression_Tutorial.ipynb`
   - GitHub clone URL: `https://github.com/aralap/3DG_Tutorials.git`

2. All references in the notebook have been updated:
   - In the cell that loads data from GitHub

## Step 5: Generate Sample Data

The sample data can be generated in two ways:

### Option A: Generate via Colab/Notebook
The notebook includes code to generate sample data automatically. This is the recommended approach.

### Option B: Generate Locally
If you want to commit the data files:

```bash
pip install -r requirements.txt
python scripts/generate_sample_data.py
```

Then commit the generated CSV:
```bash
git add data/sample_survival_data.csv
git commit -m "Add sample survival data"
git push
```

## Step 6: Enable Colab Integration

1. Go to your repository on GitHub
2. Navigate to `tutorials/COX_Regression_Tutorial.ipynb`
3. Click on the file to view it
4. At the top, you'll see an "Open in Colab" button (if the file is a .ipynb)
5. Alternatively, use the direct link format in your README:
   ```
   https://colab.research.google.com/github/aralap/3DG_Tutorials/blob/main/tutorials/COX_Regression_Tutorial.ipynb
   ```

## Step 7: Optional - Add GitHub Pages

If you want to create a nice landing page:

1. Go to repository Settings
2. Navigate to Pages
3. Select main branch and /docs folder (or root)
4. Your tutorial will be available at: `https://aralap.github.io/3DG_Tutorials/`

## Verification Checklist

- [ ] Repository is public
- [ ] All files are committed and pushed
- [ ] README links are updated with your username
- [ ] Colab link works (click the link in README)
- [ ] Sample data can be generated or loaded from GitHub
- [ ] Notebook runs successfully in Colab

## Troubleshooting

### Issue: Colab can't find the data file
**Solution**: Make sure:
- Repository is public
- Data file is committed and pushed
- Use raw GitHub URLs: `https://raw.githubusercontent.com/aralap/3DG_Tutorials/main/data/sample_survival_data.csv`

### Issue: Notebook doesn't open in Colab
**Solution**: 
- Use the direct link format in README
- Or manually upload the .ipynb file to Colab

### Issue: Dependencies not installing in Colab
**Solution**: The first cell in the notebook should install all dependencies. Make sure the cell runs before other cells.

