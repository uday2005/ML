
---

# The NumPy & Pandas Foundation: My Personal Notes

This document is a summary of the core concepts, functions, and techniques learned in "The NumPy & Pandas Foundation" course. It is designed for quick reference and future revision.

## Table of Contents
- [The NumPy \& Pandas Foundation: My Personal Notes](#the-numpy--pandas-foundation-my-personal-notes)
  - [Table of Contents](#table-of-contents)
  - [Week 1: The Bedrock (From Lists to DataFrames)](#week-1-the-bedrock-from-lists-to-dataframes)
    - [Core Concept: The Evolution of Data Structures](#core-concept-the-evolution-of-data-structures)
    - [Key Code \& Syntax](#key-code--syntax)
  - [Week 2: The Data Detective (Exploring Data)](#week-2-the-data-detective-exploring-data)
    - [Core Concept: Asking Your Data Questions](#core-concept-asking-your-data-questions)
    - [Key Code \& Syntax](#key-code--syntax-1)
  - [Week 3: The Forensic Expert (Selecting \& Filtering)](#week-3-the-forensic-expert-selecting--filtering)
    - [Core Concept: Slicing the Data Cake](#core-concept-slicing-the-data-cake)
    - [Key Code \& Syntax](#key-code--syntax-2)
  - [Week 4: The Data Janitor (Cleaning Messy Data) - *Special Emphasis*](#week-4-the-data-janitor-cleaning-messy-data---special-emphasis)
    - [Core Concept: Deal, Drop, or Fill](#core-concept-deal-drop-or-fill)
    - [Key Code \& Syntax](#key-code--syntax-3)
  - [Week 5: The Alchemist \& Librarian (Creating \& Sorting)](#week-5-the-alchemist--librarian-creating--sorting)
    - [Core Concept: Enrich and Organize](#core-concept-enrich-and-organize)
    - [Key Code \& Syntax](#key-code--syntax-4)
  - [Week 6: The Grand Finale (Grouping \& Aggregating)](#week-6-the-grand-finale-grouping--aggregating)
    - [Core Concept: Split-Apply-Combine](#core-concept-split-apply-combine)
    - [Key Code \& Syntax](#key-code--syntax-5)

---

## Week 1: The Bedrock (From Lists to DataFrames)

### Core Concept: The Evolution of Data Structures

-   **Python List:** A flexible "shopping bag." Can hold different data types. Slow for math operations.
-   **NumPy Array:** A supercharged "egg carton." Holds items of the **same data type**. Incredibly fast for mathematical operations because of **vectorization** (applying an operation to all elements at once). This is the engine under the hood of Pandas.
-   **Pandas Series:** A single column in a DataFrame. It's like a NumPy array with a labeled **index**.
-   **Pandas DataFrame:** A "smart filing cabinet." A collection of Series (drawers) with shared indexes. Each column (drawer) has a label. It combines the speed of NumPy with intuitive, human-readable labels for rows and columns.

### Key Code & Syntax

```python
# --- Imports ---
import numpy as np
import pandas as pd

# --- NumPy Basics ---
my_list = [10, 20, 30]
my_array = np.array(my_list)
print(my_array.shape) # Output: (3,)
print(my_array.dtype) # Output: int64
print(my_array * 2)   # Vectorized math: [20, 40, 60]

# --- Pandas Basics: Creating ---
# From a dictionary (keys become column names)
data = {'col_A': [1, 2, 3], 'col_B': ['X', 'Y', 'Z']}
df = pd.DataFrame(data)

# From a CSV file (most common method)
df = pd.read_csv('your_file_name.csv')

# --- Pandas Basics: Inspecting ---
df.head()       # See the first 5 rows
df.head(10)     # See the first 10 rows
df.tail()       # See the last 5 rows
df.shape        # Get dimensions (rows, columns) as a tuple
df.info()       # THE MOST IMPORTANT! Get a full summary: index, columns, non-null counts, and data types (Dtype).
```

---

## Week 2: The Data Detective (Exploring Data)

### Core Concept: Asking Your Data Questions

Once data is loaded, we need to understand its *content*. We become detectives asking broad questions to get a feel for the "room."

-   **For Numbers:** "What's the average, min, max, and median?" -> `df.describe()`
-   **For Categories:** "How many of each type are there?" -> `series.value_counts()`
-   **For Categories:** "What are all the unique types?" -> `series.unique()`

### Key Code & Syntax

```python
# Let's assume 'df' is our loaded Titanic DataFrame

# --- Summarizing Numerical Data ---
# Get summary statistics for ALL numerical columns
df.describe()

# Get summary statistics for just ONE column
df['Age'].describe()

# --- Summarizing Categorical Data ---
# Select a single column (this returns a Series)
sex_col = df['Sex']

# Count occurrences of each unique value in the Series
df['Pclass'].value_counts()

# Get the same counts as percentages/proportions
df['Pclass'].value_counts(normalize=True)

# Get an array of all unique values in a column
df['Embarked'].unique()

# Get just the number of unique values
df['Embarked'].nunique()
```

---

## Week 3: The Forensic Expert (Selecting & Filtering)

### Core Concept: Slicing the Data Cake

This is about precision: getting the exact slice of data you need.

-   **Column Selection:** Vertical cuts in the cake (`df[['Col1', 'Col2']]`).
-   **Row Filtering:** Using a "cookie cutter" (`df[condition]`). The condition must produce a `True`/`False` Series. This is **Boolean Indexing**.

### Key Code & Syntax

```python
# --- Selecting Columns ---
# Select a single column (returns a Series)
df['Age']

# Select multiple columns (returns a DataFrame)
# NOTE THE DOUBLE BRACKETS: [['...']]
df[['Name', 'Age', 'Fare']]

# --- Filtering Rows (Boolean Indexing) ---
# 1. Create a boolean condition
is_child_condition = df['Age'] < 18

# 2. Use the condition as a "cookie cutter"
children = df[is_child_condition]

# --- Combining Conditions ---
# Use & for AND, | for OR. Each condition MUST be in its own parentheses.
young_females = df[(df['Age'] < 18) & (df['Sex'] == 'female')]
first_or_second_class = df[(df['Pclass'] == 1) | (df['Pclass'] == 2)]

# --- The BEST WAY: .loc for Precision ---
# .loc[row_condition, column_selection]
# Gets the 'Name' and 'Fare' for all 1st class passengers
report = df.loc[df['Pclass'] == 1, ['Name', 'Fare']]
```

---

## Week 4: The Data Janitor (Cleaning Messy Data) - *Special Emphasis*

### Core Concept: Deal, Drop, or Fill

Real-world data is messy. `NaN` (Not a Number) represents missing data. ML models can't handle `NaN`s. We have three strategies. This is the most critical step for preparing data for machine learning.

1.  **Find the Mess:** First, always run a diagnostic to see where the problems are.
2.  **Drop:** Discard data.
    -   **Drop Columns:** If a column is mostly empty or useless (`df.drop(axis=1)`).
    -   **Drop Rows:** If a row has a critical piece of data missing and you can afford to lose the whole row (`df.dropna(axis=0)`).
3.  **Fill (Impute):** Make an educated guess to fill the `NaN`. This is often the best approach.
    -   **For Numerical Data (`Age`, `Fare`):** Fill with the `mean()` or `median()`. Median is usually safer as it's not affected by extreme outliers.
    -   **For Categorical Data (`Embarked`, `Sex`):** Fill with the `mode()` (the most frequent value).

### Key Code & Syntax

```python
# --- 1. Find the Mess ---
# The single most important command to find missing data.
# It chains .isnull() (finds where it's null) with .sum() (counts the True values).
print(df.isnull().sum())

# --- 2. The "Drop" Strategy ---
# Make a copy to work on so the original is safe
df_clean = df.copy()

# Drop an entire column (e.g., 'Cabin' which is mostly null)
# axis=1 specifies that we are targeting a COLUMN.
df_clean = df_clean.drop('Cabin', axis=1)

# Drop rows where a specific column has a NaN (e.g., 'Age')
# axis=0 specifies that we are targeting ROWS.
# The 'subset' parameter is crucial for targeting specific columns.
df_age_known = df.dropna(subset=['Age'], axis=0)


# --- 3. The "Fill" (Impute) Strategy ---
# This is often done "inplace" to modify the DataFrame directly.

# -- For Numerical Data --
# First, calculate the value to fill with (e.g., median)
age_median = df_clean['Age'].median()
# Then, fill the NaNs with that value
df_clean['Age'] = df_clean['Age'].fillna(age_median)

# -- For Categorical Data --
# First, calculate the mode (most frequent value)
# .mode() returns a Series, so we take the first item [0]
embarked_mode = df_clean['Embarked'].mode()[0]
# Then, fill with the mode
df_clean['Embarked'].fillna(embarked_mode, inplace=True)


# --- 4. Fixing Data Types ---
# Sometimes a number column is read as text ('object'). We must fix it.
# Example: df['Price'] is '$5.99' (an object)
# df['Price'] = df['Price'].str.replace('$', '').astype(float)

# Or to convert a float to an integer
df_clean['Age'] = df_clean['Age'].astype(int)
```

---

## Week 5: The Alchemist & Librarian (Creating & Sorting)

### Core Concept: Enrich and Organize

-   **Enrich (The Alchemist):** Create new, more powerful columns from existing data. This is **Feature Engineering**.
-   **Organize (The Librarian):** Sort the data to make it easy to find "top 5s", "bottom 10s", and other ranked information.

### Key Code & Syntax

```python
# --- Creating New Columns ---
# Simple math
df_clean['FamilySize'] = df_clean['SibSp'] + df_clean['Parch'] + 1

# Conditional column creation using np.where
# np.where(condition, value_if_true, value_if_false)
df_clean['AgeCategory'] = np.where(df_clean['Age'] < 18, 'Child', 'Adult')

# --- Sorting Data ---
# Sort by a single column (e.g., find highest fares)
# ascending=False sorts from largest to smallest.
df_clean.sort_values(by='Fare', ascending=False)

# Sort by multiple columns
# This sorts by Pclass first (1, 2, 3), then by Age within each class.
df_clean.sort_values(by=['Pclass', 'Age'], ascending=[True, False])

# IMPORTANT: Sorting returns a NEW DataFrame. To save the result:
sorted_df = df_clean.sort_values(by='Fare', ascending=False)
# OR
df_clean.sort_values(by='Fare', ascending=False, inplace=True)
```

---

## Week 6: The Grand Finale (Grouping & Aggregating)

### Core Concept: Split-Apply-Combine

This is the most powerful tool for analysis. It lets you compare different segments of your data. Think of sorting laundry.

1.  **Split:** Split the data into "baskets" based on a category (`df.groupby('Sex')`).
2.  **Apply:** Apply a calculation to each basket (e.g., calculate the `.mean()` of the `Survived` column for the 'male' basket and the 'female' basket).
3.  **Combine:** Pandas automatically combines the results from each basket into a new summary table.

### Key Code & Syntax

```python
# --- Simple Grouping ---
# The fundamental pattern: df.groupby('CATEGORY_COLUMN')['VALUE_COLUMN'].aggregation()

# What was the mean survival rate for each sex?
# 1. Group by 'Sex'. 2. Select 'Survived' column. 3. Calculate the mean.
df_clean.groupby('Sex')['Survived'].mean()

# What was the median age for each passenger class?
df_clean.groupby('Pclass')['Age'].median()

# --- Multi-level Grouping ---
# Just pass a list of columns to groupby()
# Survival rate for each combination of Sex and Pclass
df_clean.groupby(['Pclass', 'Sex'])['Survived'].mean()

# --- The Powerful .agg() Method ---
# Apply DIFFERENT aggregations to DIFFERENT columns all at once.
# Creates a beautiful, custom summary DataFrame.
summary_report = df_clean.groupby('Pclass').agg(
    # NewColumnName = ('OriginalColumn', 'Function')
    Total_Passengers = ('PassengerId', 'count'),
    Total_Survivors = ('Survived', 'sum'),
    Median_Age = ('Age', 'median'),
    Max_Fare = ('Fare', 'max')
)
print(summary_report)
```