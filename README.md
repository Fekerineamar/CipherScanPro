![cipherlgo](https://github.com/Fekerineamar/Fekerineamar/blob/master/img/cipherlogo.png)


# Cipher Scan Pro

Cipher Scan Pro is a command-line tool that leverages the Shodan API to search for SSL information and perform cipher scans on domains. It provides a convenient way to gather SSL details, including IP addresses and other related information.

## Features

- Search SSL information using the Shodan API
- Perform cipher scans on domains
- Output results to a file or print them to the console

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up your Shodan API key by running the script with the `--init` option:

    ```
    python cipherscan.py --init <your_api_key>
    ```

   **Note:** Please ensure you have a Shodan API key with a membership.

   ![membership](https://github.com/Fekerineamar/Fekerineamar/blob/master/img/sh.png)
   
## Usage

The tool provides several options for searching SSL information:

- Single domain search:

    ```
    python cipherscan.py -d <domain>
    ```

- Multiple domain search using a file:

    ```
    python cipherscan.py -l <domains_file>
    ```

- Search SSL information for domains from stdin:

    ```
    cat <domains_file> | python cipherscan.py
    ```

Additional options:

- Initialize the Shodan API key:

    ```
    python cipherscan.py --init <your_api_key>
    ```

- Clear the Shodan API key:

    ```
    python cipherscan.py --clear
    ```

## Contact

For any questions or inquiries, please contact fekerineamar@gmail.com.


