# Python Database Manipulation

This Python project provides a simple implementation of a database manipulation system using a custom `DB` class and a `Table` class. The code allows for basic operations such as inserting, updating, and querying data in a tabular format.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    # If using a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    
    # Install dependencies
    pip install -r requirements.txt
    ```

## Usage

The project consists of two main classes:

- `DB`: Represents a simple database that can store multiple tables.
- `Table`: Represents a table in the database with various methods for data manipulation.

Use the classes by importing them into your Python scripts:

```python
from data_processing import DB, Table

# Create a database
my_db = DB()

# Create a table
my_table = Table("example_table", [])

# Insert data into the table
my_table.insert_row({"column1": "value1", "column2": "value2"})

# Perform various operations on the table
# ...

# Insert the table into the database
my_db.insert(my_table)
```

## Examples

### Basic Operations

```python
# Create a table
my_table = Table("example_table", [])

# Insert a row
my_table.insert_row({"column1": "value1", "column2": "value2"})

# Update a row
my_table.update_row("column1", "value1", "column2", "new_value")

# Select specific attributes
selected_attributes = ["column1", "column2"]
selected_table = my_table.select(selected_attributes)
```

### Pivot Table and Join

```python
# Create two tables
table1 = Table("table1", [{"id": 1, "value": 10}, {"id": 2, "value": 20}])
table2 = Table("table2", [{"id": 1, "info": "info1"}, {"id": 2, "info": "info2"}])

# Join tables
joined_table = table1.join(table2, "id")

# Create a pivot table
pivot_result = joined_table.pivot_table(["id"], ["value"], [sum])

# Display pivot table
for row in pivot_result:
    print(row)
```