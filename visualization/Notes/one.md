

---

# Data Visualization Playbook: Note 1 of 5

## Topic: The Foundation - Gaining Control & Choosing with Purpose

This note covers the two most important, non-negotiable principles of professional data visualization in Python: **(1) how to gain absolute control over every element of your plot** and **(2) how to develop the intuition to choose the right plot for any analytical question.** Mastering these fundamentals is the prerequisite for everything that follows.

---

### **Part 1: The "Architect" Mindset - Mastering the Matplotlib Object-Oriented API**

#### **The Core Philosophy: You Control the Plot**

The biggest mistake beginners make is using "magic" one-liner commands like `data.plot()` or `plt.title()`. These commands are simple but unpredictable, as they rely on a hidden "active" plot state. This approach fails the moment you need to create more than one plot or a custom layout.

**Our Golden Rule:** We will *always* work like an architect. We first create a blueprint (`Figure` and `Axes`), and then we explicitly tell our plotting functions *where* to build.

#### **The Anatomy of a Figure: Your Key Vocabulary**

To control something, you must first know its components.

-   **`Figure` (`fig`):** This is the entire canvas, the top-level window. It's the plot of land you own. All your plots live within the Figure. You use the `fig` object for high-level actions like saving the entire image (`fig.savefig()`) or adding an overarching title (`fig.suptitle()`).
-   **`Axes` (`ax`):** This is the actual plot itself—the area with the x-axis, y-axis, and the data. It's the house you build on your plot of land. A Figure can have one or many `Axes`. **The `ax` object is your primary workspace.**

![Anatomy of a Figure](https://matplotlib.org/stable/_images/sphx_glr_anatomy_001.png)

#### **The Foundational Code Snippet: `fig, ax = plt.subplots()`**

This is the single most important line of code. It is the starting point for **every** professional plot.

**Why we use it:**
This function does two things at once:
1.  It creates a `Figure` object (our canvas).
2.  It creates one or more `Axes` objects on that figure and returns them.

By capturing these objects in variables (`fig`, `ax`), we gain explicit handles to control them.

**The Syntax:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create a Figure and a single Axes object on it.
# figsize=(width, height) is in inches. (10, 6) is a good starting point.
fig, ax = plt.subplots(figsize=(10, 6))

# --- Now, all our plotting and customization commands will use 'ax' ---

# Example: Tell Seaborn to draw a scatterplot ON this specific 'ax'.
sns.scatterplot(data=df, x='column_a', y='column_b', ax=ax)

# Example: Customize THIS 'ax' using its methods.
ax.set_title("A Clear and Specific Title")
ax.set_xlabel("X-Axis Label (with units)")
ax.set_ylabel("Y-Axis Label (with units)")

# Show the final product
plt.show()
```
**The key takeaway is the `ax=ax` argument in the Seaborn function.** You are explicitly telling Seaborn, "Don't make your own plot; draw your visual on the `Axes` I've already created and named `ax`."

---

### **Part 2: The "Detective" Mindset - Choosing the Right Plot for the Question**

Before you write a single line of plotting code, you must act like a detective and ask: **"What is the question I am trying to answer?"** The question dictates the visualization, not the other way around.

Most analytical questions fall into one of four categories.

#### **Category 1: Visualizing RELATIONSHIPS**

-   **The Question:** "How does variable A change as variable B changes?" "Are these two things related?"
-   **Your Data:** Typically two numerical variables.
-   **Your Go-To Plot:** **Scatter Plot** (`sns.scatterplot`)
-   **Why it Works:** It shows every data point as a dot, making it easy to see trends (positive, negative, none), strength of the relationship (tight cluster vs. wide cloud), and outliers.
-   **The Syntax:**
    ```python
    # To see the relationship between carat and price
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=diamonds, x='carat', y='price', ax=ax, alpha=0.5) # alpha handles overplotting
    ax.set_title("Relationship between Diamond Carat and Price")
    plt.show()
    ```
-   **Pro-Tool:** For linear relationships, use `sns.regplot()` to automatically add a trend line.

#### **Category 2: Visualizing DISTRIBUTIONS**

-   **The Question:** "What is the shape of this variable?" "What are the most common values?" "Are there outliers?"
-   **Your Data:** Typically one numerical variable.
-   **Your Go-To Plot:** **Histogram** (`sns.histplot`)
-   **Why it Works:** It groups data into bins and uses bars to show the frequency of each bin, giving an immediate sense of the data's shape (e.g., normal/bell-curve, skewed).
-   **The Syntax:**
    ```python
    # To see the distribution of diamond prices
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=diamonds, x='price', kde=True, ax=ax) # kde=True adds a smooth line
    ax.set_title("Distribution of Diamond Prices")
    plt.show()
    ```
-   **Pro-Tool:** To *compare distributions* across categories (e.g., price distribution for each `cut`), a **Box Plot** (`sns.boxplot`) or **Violin Plot** (`sns.violinplot`) is superior.

#### **Category 3: Visualizing COMPARISONS**

-   **The Question:** "How do these different groups compare?" "Which category is bigger/smaller?"
-   **Your Data:** Typically one categorical variable and one numerical variable.
-   **Your Go-To Plot:** **Bar Chart** (`sns.barplot`)
-   **Why it Works:** The human eye is excellent at comparing lengths, making bar charts the clearest way to show differences in magnitude between discrete groups.
-   **The Syntax:**
    ```python
    # To compare the average price for each diamond cut
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=diamonds, x='cut', y='price', ax=ax)
    ax.set_title("Average Price by Diamond Cut Quality")
    plt.show()
    ```
-   **Pro-Tool:** If you just want to count the number of items in each category, use `sns.countplot()`. **Crucial Tip:** Always order the bars of a bar chart logically (e.g., highest to lowest) to make it more insightful.

#### **Category 4: Visualizing COMPOSITIONS**

-   **The Question:** "How is this whole thing made up of its parts?" "What is the percentage share of each category?"
-   **Your Data:** A variable that represents a whole and another that represents its parts.
-   **Your Go-To Plot:** **AVOID Pie Charts.** Use a **Treemap** or a **Stacked Bar Chart** instead.
-   **Why it Works:** The eye struggles to compare angles in a pie chart. It's much better at comparing area (Treemap) or length (Bar Chart).
-   **The Syntax (Treemap using the `squarify` library):**
    ```python
    import squarify

    # First, get the data ready (e.g., count of each 'cut' type)
    cut_counts = diamonds['cut'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    squarify.plot(sizes=cut_counts.values, 
                  label=cut_counts.index, 
                  alpha=0.8, ax=ax)
    ax.set_title("Composition of Diamond Cuts in the Dataset")
    plt.axis('off') # Turn off axis for a cleaner look
    plt.show()
    ```

---

### **Summary of Note 1**

-   **Control:** Every plot begins with `fig, ax = plt.subplots()`. This gives you explicit control and is the foundation of all advanced work.
-   **Purpose:** Before coding, identify your goal: are you showing a **Relationship**, **Distribution**, **Comparison**, or **Composition**?
-   **Execution:** Use the "Go-To Plot" for that goal as your starting point. Use the `ax=ax` argument to direct the plot onto your canvas.

By internalizing this two-part framework of "Control" and "Purpose," you have built the essential foundation needed to tackle any visualization task that comes your way.