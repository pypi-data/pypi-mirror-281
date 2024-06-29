![DataDashr Logo](https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.svg)

## Description

Converse with Your Data Through Open Source AI.

Unleash the power of your data with natural language questions.  
Our open-source platform, built on Ollama, delivers powerful insights without the cost of APIs.

Integrate effortlessly with your existing infrastructure, connecting to various data sources including SQL, NoSQL, CSV, and XLS files.

Obtain in-depth analytics by aggregating data from multiple sources into a unified platform, providing a holistic view of your business.

Convert raw data into valuable insights, facilitating data-driven strategies and enhancing decision-making processes.

Design intuitive and interactive charts and visual representations to simplify the understanding and interpretation of your business metrics.

[![youtube_video](https://img.youtube.com/vi/En33l3SFe-s/0.jpg)](https://www.youtube.com/watch?v=En33l3SFe-s&ab_channel=datadashr)

## Installation

To install the package, run the following command:

```bash
pip install datadashr
```

## Requirements
Our goal is to have a system that works completely locally, to do this we use Ollama and Codestral as a model

**Download** Ollama from the following link: [https://ollama.com/download](https://ollama.com/download)

install the model by running the following command:

```bash
ollama pull codestral
```

## Starting the Interface

To start the user interface, run the following command:

```bash
datadashr
```

## Usage Example

```python
import pandas as pd
from pprint import pprint
from datadashr import DataDashr
from datadashr.core.llm import OllamaLLM

# Create DataFrame containing employee details
employees_df = pd.DataFrame({
    'employeeid': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['HR', 'IT', 'Finance']
})

# Create DataFrame containing salary information for employees
salaries_df = pd.DataFrame({
    'employeeid': [1, 2, 3],
    'salary': [50000, 60000, 70000]
})

# Create DataFrame containing department information and their managers
departments_df = pd.DataFrame({
    'department': ['HR', 'IT', 'Finance'],
    'manager': ['Dave', 'Eva', 'Frank']
})

# Create DataFrame containing project details and employee assignments
projects_df = pd.DataFrame({
    'projectid': [101, 102, 103],
    'projectname': ['Project A', 'Project B', 'Project C'],
    'employeeid': [1, 2, 3]
})

# Structure to import and map the data sources
import_data = {
    'sources': [
        {"source_name": "employees_df", "data": employees_df, "source_type": "pandas",
         "description": "Contains employee details including their department."},
        {"source_name": "salaries_df", "data": salaries_df, "source_type": "pandas",
         "description": "Contains salary information for employees."},
        {"source_name": "departments_df", "data": departments_df, "source_type": "pandas",
         "description": "Contains information about departments and their managers."},
        {"source_name": "projects_df", "data": projects_df, "source_type": "pandas",
         "description": "Contains information about projects and the employees assigned to them."},
    ],
    'mapping': {
        "employeeid": ['employees_df', 'salaries_df', 'projects_df'],  # Mapping employeeid across three DataFrames
        "department": ['employees_df', 'departments_df']  # Mapping department across two DataFrames
    }
}

# Initialize the LLM (Language Learning Model) instance with specific parameters
llm = OllamaLLM(model='codestral', params={"temperature": 0.0}, verbose=False)

# Initialize the DataDashr object with imported data and LLM instance
df = DataDashr(data=import_data, llm_instance=llm, verbose=False, enable_cache=True, format_type='data')

# Perform a query on the combined DataFrame to get the employee with the highest salary and their salary
result = df.chat('Show the employer with highest salary and the salary')

# Print the result
pprint(result)


```
