# currency-quote-wrapper: Complete solution for extracting currency pair quotes data

[![PyPI - Status](https://img.shields.io/pypi/status/currency-quote?style=for-the-badge&logo=pypi)](https://pypi.org/project/currency-quote/)

[![PyPI - Downloads](https://img.shields.io/pypi/dm/currency-quote?style=for-the-badge&logo=pypi)](https://pypi.org/project/currency-quote/)

[![PyPI - Version](https://img.shields.io/pypi/v/currency-quote?style=for-the-badge&logo=pypi)](https://pypi.org/project/currency-quote/#history)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/currency-quote?style=for-the-badge&logo=python)

[![CI](https://img.shields.io/github/actions/workflow/status/IvanildoBarauna/currency-quote-wrapper/CI.yaml?&style=for-the-badge&logo=githubactions&cacheSeconds=60&label=Tests+and+pre+build)](https://github.com/IvanildoBarauna/currency-quote-wrapper/actions/workflows/CI.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/IvanildoBarauna/currency-quote-wrapper/CD.yaml?&style=for-the-badge&logo=githubactions&cacheSeconds=60&event=release&label=Package+publication)](https://github.com/IvanildoBarauna/currency-quote-wrapper/actions/workflows/CD.yaml)

[![Codecov](https://img.shields.io/codecov/c/github/IvanildoBarauna/currency-quote-wrapper?style=for-the-badge&logo=codecov)](https://app.codecov.io/gh/IvanildoBarauna/currency-quote-wrapper)
## Project Stack

![Python](https://img.shields.io/badge/-Python-05122A?style=flat&logo=python)&nbsp;
![Docker](https://img.shields.io/badge/-Docker-05122A?style=flat&logo=docker)&nbsp;
![Poetry](https://img.shields.io/badge/-Poetry-05122A?style=flat&logo=poetry)&nbsp;
![GitHub Actions](https://img.shields.io/badge/-GitHub_Actions-05122A?style=flat&logo=githubactions)&nbsp; 
![CodeCov](https://img.shields.io/badge/-CodeCov-05122A?style=flat&logo=codecov)&nbsp;
![pypi](https://img.shields.io/badge/-pypi-05122A?style=flat&logo=pypi)&nbsp;
![pandas](https://img.shields.io/badge/-pandas-05122A?style=flat&logo=pandas)&nbsp;
![pytest](https://img.shields.io/badge/-pytest-05122A?style=flat&logo=pytest)&nbsp;


## Project description

* Complete solution for extracting currency pair quotes data

## Contributing

See the following docs:

- [Contributing Guide](https://github.com/IvanildoBarauna/currency-quote-wrapper/blob/main/CONTRIBUTING.md)
- [Code Of Conduct](https://github.com/IvanildoBarauna/currency-quote-wrapper/blob/main/CODE_OF_CONDUCT.md)

## Project Highlights:

- Comprehensive Testing: Development of tests to ensure the quality and robustness of the code

- Parameter Validation: Sending valid parameters based on the request data source itself, ensuring the integrity and accuracy of the information processed.

- Configuration Management: Use of a configuration module to manage endpoints, retry times and number of attempts, providing flexibility and ease of adjustment.

## How to use it

``` python
## Importing library
from currency_quote CurrencyQuote

# For get the last quote of one currency
client = CurrencyQuote(['USD-BRL'])
# or get quotes of multiple currencies
client = CurrencyQuote(['USD-BRL', 'EUR-BRL'])

# Get the last quote
last_quote = client.get_last_quote()
# Get history quote of currency
history_quote = client.get_history_quote(reference_date=20240626)

