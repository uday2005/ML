

## Part 1: The Foundation

### Module 1: Gaining Full Control: The Matplotlib API

**Core Philosophy:** Do not let the library control you. You control the library. The key to this is the **Object-Oriented (OO) API**.

**The Golden Rule:** Always start your plot with `fig, ax = plt.subplots()`.
- **`fig`**: The entire canvas/figure. You use it for overall actions like `fig.suptitle()` or `fig.savefig()`.
- **`ax`**: A single plot (an `Axes` object). This is your main workspace. 90% of your commands will start with `ax.`.

**Anatomy of a Figure:**
- `ax.set_title()`: Sets the title for that specific subplot.
- `ax.set_xlabel()`, `ax.set_ylabel()`: Sets the labels for the axes. **Always include units** (e.g., "$", "mm", "(g)").
- `ax.plot()`, `ax.scatter()`, `ax.bar()`: The commands to draw data onto the `ax`.
- `ax.spines[...]`: The lines that form the box around the plot. A key professional touch is to remove clutter: `ax.spines[['top', 'right']].set_visible(False)`.
- `ax.text()`, `ax.annotate()`: For placing text and arrows to guide the viewer's eye.
- `ax.legend()`: Displays the legend for plots created with a `label`.

### Module 2: Choosing the Right Plot for the Question

Before writing code, answer two questions:
1.  **What is my primary goal?** (Relationship, Comparison, Distribution, or Composition)
2.  **What is my data?** (Number of variables and their type: Numerical or Categorical)

This leads to the **Chart-Choosing Flowchart**:

| **My Goal Is...** | **And My Variables Are...** | **My Go-To Plot Is...** | **Seaborn Axes-Level Function** |
| :--- | :--- | :--- | :--- |
| **Relationship** | 2 Numerical | Scatter Plot | `sns.scatterplot()` or `sns.regplot()` |
| **Relationship** | 1 Numerical over Time | Line Plot | `sns.lineplot()` |
| **Distribution** | 1 Numerical | Histogram | `sns.histplot()` |
| **Distribution** | 1 Numerical + 1 Categorical | Box Plot / Violin Plot | `sns.boxplot()` / `sns.violinplot()` |
| **Comparison** | 1 Numerical + 1 Categorical | Bar Chart | `sns.barplot()` |
| **Comparison** | Counting items in 1 Category | Count Plot | `sns.countplot()` |
| **Composition** | Parts of a whole | Stacked Bar / Treemap | `df.plot(kind='bar', stacked=True)` / `squarify.plot()` |

## Part 2: The Core Visualizations in Detail

### Module 3: Visualizing Distributions (The Shape of Data)

**Primary Question:** "What does the spread of my data look like? What are the common values and are there outliers?"

| Plot Type | When to Use It | Pro-Tip for Polishing |
| :--- | :--- | :--- |
| **Histogram** (`histplot`) | The default choice for seeing the shape of a single numerical variable. Great for understanding frequency and modality. | Always experiment with the `bins` parameter. Overlaying a KDE (`kde=True`) can help clarify the shape. |
| **Box Plot** (`boxplot`) | Best for **comparing distributions across many categories**. It's a compact summary of min, max, median, and quartiles. | Excellent for identifying outliers. Use it when the overall shape isn't as important as comparing the central tendencies and spreads. |
| **Violin Plot** (`violinplot`)| A hybrid of a box plot and a KDE. Use it when you want to compare distributions across categories **AND** you care about the specific shape of each distribution (e.g., to see if one is bimodal). | Use the `inner='quartile'` argument to draw lines for the quartiles inside the violin for a more precise summary. |

---

### Module 4: Visualizing Relationships (Uncovering Connections)

**Primary Question:** "How do variables A and B change with respect to each other?"

| Plot Type | When to Use It | Pro-Tip for Polishing |
| :--- | :--- | :--- |
| **Scatter Plot** (`scatterplot`) | The champion for showing the relationship between **two numerical variables**. | The `hue` parameter is your superpower. Use it to add a third, categorical dimension to your plot. Also, use `alpha < 1` to handle overplotting. |
| **Line Plot** (`lineplot`) | When your x-axis is **time** or another sequential variable. Connects the dots to show a trend. | Seaborn's `lineplot` automatically shows a confidence interval when you have multiple data points per time period. This is a powerful statistical summary. |
| **Regression Plot** (`regplot`, `lmplot`) | When you want to explicitly model a **linear relationship** between two numerical variables. | `lmplot` is a Figure-level function perfect for quickly splitting the relationship by a category (`hue`). Use `regplot` for more control over a single `ax`. |

**Key Distinction: `regplot` vs. `lmplot`**

- Use `regplot` (Axes-level) when you need to place a single regression line on a complex, multi-plot grid you've created with `plt.subplots()`.
- Use `lmplot` (Figure-level) when your main goal is to quickly create a plot (or a grid of plots) that compares regression lines across different categories (`hue`, `col`). It's a convenient shortcut that creates its own figure.

---

### Module 5: Visualizing Comparisons & Compositions (Magnitudes and Proportions)

**Primary Question:** "How do these groups compare?" or "How is this whole broken down?"

| Plot Type | When to Use It | Pro-Tip for Polishing |
| :--- | :--- | :--- |
| **Bar Chart** (`barplot`) | The best tool for comparing a numerical value across **discrete categories**. | **ALWAYS order your bars** (e.g., highest to lowest). This dramatically improves readability. Add data labels using a `for p in ax.patches:` loop for clarity. |
| **Count Plot** (`countplot`)| A specialized bar chart that simply counts the number of occurrences in each category. A histogram for categorical data. | Great for quick frequency checks of categorical variables. |
| **Stacked Bar Chart** | A powerful alternative to a pie chart for showing **composition**. Good for showing part-to-a-whole relationships, especially when comparing compositions across different groups. | Use `df.pivot_table()` to get your data into the right shape, then `.plot(kind='bar', stacked=True)`. |
| **Treemap** (`squarify`) | Another excellent pie chart alternative, especially if you have many categories. Uses area to represent proportion. | Turn off the axes (`ax.axis('off')`) for a clean, modern look. Use labels that show both the category and its value. |

**Key Distinction: Bar Chart vs. Histogram**

- **Bar Chart:** Compares values across **CATEGORIES** (x-axis has discrete labels).
- **Histogram:** Shows the distribution of a **NUMERICAL** variable (x-axis is a continuous number line broken into bins).


Understood. You want a more detailed, practical, and code-centric reference guide. Let's build a definitive version of the notes, focusing on Modules 4 and 5 as requested, with clear syntax examples and deeper strategic advice.

Save this as `data_viz_playbook_v2.md`. This is the kind of document a data science team would build internally.

---

# Data Visualization Playbook v2

This playbook provides practical guidance and code recipes for creating high-impact visualizations. It focuses on the "when" and "why" of chart selection, supported by ready-to-use syntax.

## Core Philosophy: The `fig, ax` Paradigm

All examples follow the Object-Oriented paradigm. This is non-negotiable for professional work.

**The Foundational Snippet:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create the canvas (Figure) and the plotting area (Axes)
fig, ax = plt.subplots(figsize=(10, 6))

# --- Your plotting commands using 'ax' go here ---
# Example: sns.scatterplot(..., ax=ax)
# Example: ax.set_title(...)

# Show the plot
plt.show()
```

---

## Module 4 (Deep Dive): Visualizing Relationships

**Primary Goal:** To understand how two or more variables interact, correlate, and change with respect to one another.

### **Tool 1: The Scatter Plot (`sns.scatterplot`)**

- **When to Use It:** The absolute best choice for visualizing the relationship between **two numerical (continuous) variables**.
- **Questions It Answers:**
    - Is there a relationship? (Are the points a random cloud or in a pattern?)
    - What is the direction? (Positive: bottom-left to top-right. Negative: top-left to bottom-right.)
    - How strong is it? (Are the points tightly packed or widely dispersed?)
    - Are there outliers? (Points that deviate from the main pattern.)

- **Core Syntax:**
    ```python
    # Basic 2D scatter plot
    sns.scatterplot(data=df, x='numerical_col_1', y='numerical_col_2', ax=ax)
    ```

- **The Superpower: Adding Dimensions with `hue`, `size`, and `style`**
    This is how you tell a multi-faceted story in a single chart. It's the most important technique in this module.

    - **`hue`**: Maps a **categorical** variable to **color**. The most effective way to add a dimension.
    - **`size`**: Maps a **numerical** variable to the **area** of the points.
    - **`style`**: Maps a **categorical** variable to the **marker shape** (o, X, s, +).

- **"Hero-Level" Syntax (4D Plot):**
    ```python
    # This single plot shows the relationship between X and Y,
    # split by category_A (color), with point area determined by numerical_B.
    sns.scatterplot(
        data=df,
        x='flipper_length_mm',   # Dimension 1 (Numerical)
        y='bill_length_mm',      # Dimension 2 (Numerical)
        hue='species',           # Dimension 3 (Categorical) -> Color
        size='body_mass_g',      # Dimension 4 (Numerical) -> Size
        sizes=(20, 200),         # Control the min/max dot size for readability
        alpha=0.7,               # Add transparency to see overlapping points
        ax=ax
    )
    ax.set_title('Multiple Dimensions in One View')
    ax.legend(title='Legend Title') # Control the legend
    ```

### **Tool 2: The Regression Plot (`sns.regplot` / `sns.lmplot`)**

- **When to Use It:** When you want to go beyond just showing the relationship and explicitly **model a linear trend** within it.
- **Questions It Answers:**
    - Is the linear trend positive or negative?
    - How confident are we in this trend line? (The shaded area is the confidence interval.)
    - Does the trend differ between groups? (`lmplot` with `hue` is perfect for this).

- **`regplot` (The Flexible Worker - Axes-level):**
    - **Syntax:**
      ```python
      # Draws a single regression line on an existing Axes
      sns.regplot(data=df, x='total_bill', y='tip', ax=ax,
                  scatter_kws={'alpha': 0.4}, # Pass args to the scatter component
                  line_kws={'color': 'red'})     # Pass args to the line component
      ax.set_title('Regression on a specific Axes')
      ```
    - **Pro-Tip:** To show multiple regression lines (e.g., by category), you must use a `for` loop. This gives you ultimate control but is more verbose.

- **`lmplot` (The Smart Manager - Figure-level):**
    - **Syntax:**
      ```python
      # lmplot creates its OWN figure. It does not use 'ax='.
      # Its superpower is handling `hue` and `col`/`row` automatically.
      sns.lmplot(
          data=tips,
          x='total_bill', y='tip',
          hue='smoker',      # Automatically create separate lines and colors
          col='day',         # Automatically create separate plots for each day
          col_wrap=2,        # Wrap the columns after 2 plots
          height=5           # Control the size of each plot
      )
      plt.suptitle('Linear Model Plot: The Smart Way to Compare Trends', y=1.02)
      ```
- **Strategic Choice:**
    - Use `lmplot` for fast, powerful exploration when the relationship is the main story.
    - Use `regplot` when the regression is one component of a larger, custom dashboard you are building with `plt.subplots()`.

---

## Module 5 (Deep Dive): Visualizing Comparisons & Compositions

**Primary Goal:** To compare magnitudes across discrete groups or show how a whole is broken into its constituent parts.

### **Tool 1: The Bar Chart (`sns.barplot` / `sns.countplot`)**

- **When to Use It:** The gold standard for comparing a numerical value across different categories.
- **Critical Distinction:**
    - **`barplot`**: Takes an `x` (categorical) and a `y` (numerical). It calculates the **mean** of `y` for each `x` category by default.
    - **`countplot`**: Takes only an `x` (categorical). It simply **counts** the number of occurrences of each category.
- **The Most Important Pro-Tip: ORDERING!**
    An unordered bar chart is a missed opportunity. Always order your bars to reveal insights instantly.

- **"Hero-Level" Syntax (Ordered Bar Chart with Labels):**
    ```python
    fig, ax = plt.subplots(figsize=(12, 7))

    # Step 1: Calculate the order in Pandas
    order = df.groupby('category_col')['value_col'].mean().sort_values(ascending=False).index

    # Step 2: Plot with the 'order' parameter
    bar_plot = sns.barplot(data=df, x='category_col', y='value_col', order=order, ax=ax)

    ax.set_title('A Clearly Ordered Comparison', fontsize=16, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False) # Clean the canvas

    # Step 3: Add data labels with a loop
    for p in bar_plot.patches:
        height = p.get_height()
        ax.text(
            x=p.get_x() + p.get_width() / 2, # Center the text horizontally
            y=height + 0.5,                  # Position text just above the bar
            s=f'{height:.2f}',               # The text to display, formatted to 2 decimal places
            ha='center'                      # Horizontal alignment
        )
    ```

### **Tool 2: Alternatives to the Pie Chart (Showing Composition)**

- **Why Avoid Pie Charts?** Humans are bad at comparing angles. Pie charts are low-density information displays and become unreadable with more than 3-4 slices. We can do better.

#### **Alternative A: The Stacked Bar Chart**

- **When to Use It:** To show how a whole is composed of parts, especially when you want to **compare compositions across different groups**.
- **Questions It Answers:**
    - What is the total size of each main category? (The total height of the bar)
    - What is the proportional makeup of each category? (The size of the colored segments)
- **Syntax (The Pandas `pivot_table` + `.plot` Method):**
    ```python
    # Step 1: Reshape data with pivot_table. We need counts of a sub-category within a main category.
    # Example: Count 'sex' within each 'pclass' on the Titanic
    composition_df = df.pivot_table(index='pclass', columns='sex', aggfunc='size')

    # Step 2: Plot directly from the pivoted DataFrame
    fig, ax = plt.subplots(figsize=(10, 7))
    composition_df.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        colormap='viridis' # Choose a nice colormap
    )
    ax.set_title('Composition Comparison with a Stacked Bar Chart')
    ax.tick_params(axis='x', rotation=0) # Keep x-labels horizontal
    ```

#### **Alternative B: The Treemap (`squarify`)**

- **When to Use It:** To show the composition of a **single whole** when you have many parts. It uses area effectively to represent proportion.
- **Questions It Answers:**
    - Which components make up the largest/smallest share of the total?
- **Syntax:**
    ```python
    import squarify

    # Step 1: Prepare the data - you need a list of values and corresponding labels.
    # Example: Party size counts for a single day
    counts = df['size'].value_counts()
    sizes = counts.values
    labels = [f'{size}\n({count} tables)' for size, count in zip(counts.index, counts.values)]

    # Step 2: Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(
        sizes=sizes,
        label=labels,
        color=sns.color_palette("coolwarm", len(sizes)),
        alpha=0.8,
        ax=ax
    )
    ax.set_title('Composition with a Treemap')
    ax.axis('off') # Treemaps look best with axes turned off
    ```