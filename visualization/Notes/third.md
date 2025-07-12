
---

# Data Visualization Playbook: Note 3 of 5

## Topic: Mastering Comparisons and Compositions

This note details the best practices for two fundamental analytical tasks: **(1) Comparing magnitudes across discrete categories** and **(2) Showing part-to-whole relationships.** We will master the bar chart and its variations, and establish a clear framework for choosing effective alternatives to the pie chart.

---

### **Part 1: The Art of the Comparison - Using Bar Charts Effectively**

**The Core Question:** "Which category is biggest?" "How does value X compare for group A vs. group B?"

#### **Tool 1: The Bar Chart (`sns.barplot`)**

-   **What it is:** The undisputed champion for comparing a single numerical value across different categories.
-   **Why it Works:** The human eye is incredibly good at comparing lengths on a common baseline. This makes it easy to see both large and subtle differences in magnitude.
-   **The Golden Rule:** Your value axis **must start at zero**. Starting the axis higher is a common data visualization lie used to exaggerate differences. Seaborn does this correctly by default.

-   **The Syntax:** `sns.barplot` is a powerful function. It takes a categorical variable for one axis and a numerical variable for the other, and by default, it **automatically calculates and plots the mean** of the numerical variable for each category.
    ```python
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.barplot(
        data=diamonds, 
        x='cut', 
        y='price', 
        ax=ax
    )
    
    ax.set_title('Average Diamond Price by Cut Quality')
    plt.show()
    ```

#### **Pro-Tip #1: The Power of Ordering**

An unordered bar chart forces your audience to work hard, scanning back and forth to find the highest and lowest values. You can make your plot instantly more effective by ordering the bars.

-   **How to do it:**
    1.  In Pandas, calculate the metric you want to sort by (e.g., the mean price for each cut).
    2.  Use `.sort_values()` to get the correct order.
    3.  Extract the `.index` (which contains the category names in the new order).
    4.  Pass this list of names to the `order=` parameter in your Seaborn plot.

-   **The Syntax:**
    ```python
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Step 1, 2, 3: Calculate the order in a single line
    cut_order = diamonds.groupby('cut')['price'].mean().sort_values(ascending=False).index
    
    # Step 4: Pass the order to the plot
    sns.barplot(data=diamonds, x='cut', y='price', ax=ax, order=cut_order)
    
    ax.set_title('Average Diamond Price by Cut Quality (Ordered)')
    plt.show()
    ```
    Notice how much easier it is to read and draw conclusions from the ordered version.

#### **Tool 2: The Count Plot (`sns.countplot`)**

-   **What it is:** A specialized bar chart that does one simple thing: it counts the number of occurrences of each category.
-   **When to use it:** When your question is "How many of each category are there?"
-   **The Syntax:** You only provide an `x` (or `y`) variable. The count is calculated automatically.
    ```python
    fig, ax = plt.subplots(figsize=(10, 6))

    # Count the number of diamonds for each 'clarity' level
    sns.countplot(data=diamonds, x='clarity', ax=ax)
    
    ax.set_title('Count of Diamonds by Clarity')
    plt.show()
    ```
-   **Bar Chart vs. Histogram:** Remember, a bar chart has **gaps** between the bars because the categories are discrete. A histogram's bars touch because it represents a continuous numerical range.

---

### **Part 2: The Art of Composition - Alternatives to the Pie Chart**

**The Core Question:** "How is this total value broken down into its parts?" "What is the percentage share of each component?"

#### **Why We Avoid Pie Charts**

While ubiquitous, pie charts are a poor choice for most data visualization tasks.
1.  **Difficulty in Comparison:** The human eye is terrible at accurately judging angles and areas. It's hard to tell if a 25% slice is bigger than a 23% slice without explicit labels.
2.  **Limited Categories:** They become an unreadable mess with more than 4-5 categories.
3.  **Misleading in 3D:** 3D pie charts use perspective to distort proportions, which is another data visualization lie.

#### **Alternative 1: The Stacked Bar Chart**

-   **What it is:** A bar chart where the bars are segmented to show the composition of each category.
-   **Best for:** Showing part-to-whole relationships, especially when you want to **compare compositions across different groups.** For example, "What was the gender composition *within each passenger class* on the Titanic?"
-   **The Syntax (The Pandas `pivot_table` + `.plot()` method):** Seaborn doesn't have a direct function for this, but Pandas makes it easy.
    1.  **Reshape the data:** You need a table where your main categories are the index, the sub-categories are the columns, and the values are the counts. `pivot_table` is perfect for this.
    2.  **Plot:** Use the `.plot()` method directly on the reshaped DataFrame.

-   **The Syntax:**
    ```python
    # To show the composition of diamond COLOR within each CUT quality
    # Step 1: Create a pivot table to get the composition
    composition_df = diamonds.pivot_table(index='cut', columns='color', aggfunc='size', fill_value=0)
    
    # Optional: Convert to percentages for easier comparison
    composition_percent_df = composition_df.div(composition_df.sum(axis=1), axis=0) * 100
    
    # Step 2: Plot directly from the pivoted DataFrame
    fig, ax = plt.subplots(figsize=(12, 7))
    composition_percent_df.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        colormap='viridis' 
    )
    
    ax.set_title('Color Composition (in %) within Each Cut Quality')
    ax.set_ylabel('Percentage (%)')
    plt.show()
    ```

#### **Alternative 2: The Treemap (`squarify` library)**

-   **What it is:** A visualization that uses nested rectangles where the area of each rectangle is proportional to its value.
-   **Best for:** Showing the composition of a **single whole** when you have many categories. It's more space-efficient and often clearer than a long bar chart or a cluttered pie chart.
-   **The Syntax:**
    ```python
    import squarify
    import matplotlib.pyplot as plt

    # Step 1: Prepare the data (a list of values and a list of labels)
    cut_counts = diamonds['cut'].value_counts()
    labels = [f'{label}\n({count})' for label, count in cut_counts.items()] # e.g., "Ideal\n(21551)"
    sizes = cut_counts.values
    
    # Step 2: Plot
    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(
        sizes=sizes,
        label=labels,
        alpha=0.8,
        ax=ax,
        text_kwargs={'fontsize': 10}
    )
    
    ax.set_title('Treemap of Diamond Cut Composition')
    plt.axis('off')
    plt.show()
    ```

---

### **Summary of Note 3**

-   **Comparisons:** Use a `barplot` (to compare means/sums) or a `countplot` (to compare raw counts). **Always order the bars** to make your point clearly.
-   **Compositions:** **Avoid pie charts.** Use a `stacked bar chart` to compare compositions across groups. Use a `treemap` to show the composition of a single whole, especially with many categories.