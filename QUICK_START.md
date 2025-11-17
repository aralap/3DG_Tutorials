# Quick Start Guide

## For Users (Not Repository Owners)

### Option 1: Use Google Colab (Recommended - No Setup Required!)

1. **Click this link** (after repository owner updates with their username):
   ```
   https://colab.research.google.com/github/aralap/3DG_Tutorials/blob/main/tutorials/COX_Regression_Tutorial.ipynb
   ```

2. **Or manually:**
   - Go to [Google Colab](https://colab.research.google.com/)
   - Click `File` → `Open notebook`
   - Go to the `GitHub` tab
   - Enter: `aralap/3DG_Tutorials`
   - Select `tutorials/COX_Regression_Tutorial.ipynb`

3. **Run all cells:**
   - The notebook will automatically install dependencies
   - The notebook will generate sample data automatically
   - Follow the step-by-step tutorial

### Option 2: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aralap/3DG_Tutorials.git
   cd 3DG_Tutorials
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample data (if not already in repository):**
   ```bash
   python scripts/generate_sample_data.py
   ```

4. **Run the tutorial:**
   ```bash
   jupyter notebook tutorials/COX_Regression_Tutorial.ipynb
   ```

   **OR** run the standalone script:
   ```bash
   python scripts/cox_regression_analysis.py
   ```

## For Repository Owners

See `GITHUB_SETUP.md` for detailed instructions on setting up the GitHub repository.

## Data Files

### Option A: Use Generated Data (Recommended)
The notebook includes code to generate sample data automatically. This is the easiest approach and requires no file downloads.

### Option B: Load from GitHub
If the repository owner has committed the data files, you can load them directly:
```python
github_url = "https://raw.githubusercontent.com/aralap/3DG_Tutorials/main/data/sample_survival_data.csv"
data = pd.read_csv(github_url)
```

### Option C: Generate Locally
Run the data generation script:
```bash
python scripts/generate_sample_data.py
```

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Review the tutorial notebook for step-by-step explanations

