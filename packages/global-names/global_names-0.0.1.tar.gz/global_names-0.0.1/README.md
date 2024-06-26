NamesData
=============

## Overview

This repository contains a collection of name datasets gathered from multiple sources, including government records, historical documents, and public databases. The data has been cleaned, standardized, and organized to facilitate easy use in data science projects, demographic studies, and name-related research.

## Features

- **Extensive Name Collection**: A wide range of first and last names from multiple countries and cultures.
- **Python Tools**: Utilities and scripts to efficiently work with the name datasets.
- **Easy Integration**: Simple and intuitive integration with your Python projects.
- **Open Source**: Released under the MIT License, allowing for free use and distribution.

## Installation

To use NameDatabases in your project, you can clone the repository and install the necessary dependencies.

```bash
git clone https://github.com/DecisionNerd/NameDatabases.git
cd NameDatabases
pip install -r requirements.txt
```

## Usage

### Loading the Datasets

You can easily load the name datasets using the provided Python tools. Below is an example of how to load and use the data.

```python
import pandas as pd

# Load last names from a specific country
last_names_df = pd.read_csv('data/last_names/usa.csv')

# Display the first few entries
print(last_names_df.head())
```

### Searching for a Name

The tools provided also include functionality to search for specific names within the datasets.

```python
from tools import name_search

# Search for a specific last name
results = name_search.search_last_name('Smith', 'usa')
print(results)
```

### Generating Random Names

You can also generate random names using the datasets for purposes such as testing or anonymizing data.

```python
from tools import name_generator

# Generate a random full name
random_name = name_generator.generate_random_name('usa')
print(random_name)
```

## Contributing

We welcome contributions from the community! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

A big thank you to Matthew Hager [smashew](https://github.com/smashew) for his original work on the text databases of last names. This project builds upon the foundation he created.

A thank you to Philippe Rémy [philipperemy](https://github.com/philipperemy) for posting the username dataset.  While Philippe's work is not integrated into this project, his data preparation has greatly accelerated our work on NamesData.

## Contact

For any questions or suggestions, feel free to open an issue or start a discussion thread or contact us at hello@frontieranalytica.com.
