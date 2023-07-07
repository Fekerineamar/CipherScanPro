import argparse
import shodan
import os
import sys
from dotenv import load_dotenv


def logo():
    os.system("clear")
    print("""
       _______       __              _____                
      / ____(_)___  / /_  ___  _____/ ___/_________ _____ 
     / /   / / __ \/ __ \/ _ \/ ___/\__ \/ ___/ __ `/ __ \\
    / /___/ / /_/ / / / /  __/ /   ___/ / /__/ /_/ / / / /
    \____/_/ .___/_/ /_/\___/_/   /____/\___/\__,_/_/ /_/ 
          /_/                                             
                        ____           
                       / __ \_________ 
                      / /_/ / ___/ __ \\
                     / ____/ /  / /_/ /
                    /_/   /_/   \____/ 
                                                           
                                    By Cody4code v1.0.1
    """)

logo()
 

# API token environment variable
API_TOKEN_ENV_VAR = 'SHODAN_API_KEY'

# Initialize the Shodan API client
api = None

def save_api_token(api_token):
    with open('.env', 'w') as file:
        file.write('SHODAN_API_KEY={}'.format(api_token))

def load_api_token():
    load_dotenv('.env')
    return os.getenv(API_TOKEN_ENV_VAR)

def init_api_token(api_token):
    save_api_token(api_token)

def is_valid_api_key(api_token):
    try:
        api = shodan.Shodan(api_token)
        api.info()
        return True
    except shodan.APIError as e:
        if e.response.status_code == 403:
            print('Invalid Shodan API key. Please use a Shodan member account for access.')
        else:
            print('Error: {}'.format(e))
        return False

def clear_api_key():
    save_api_token('')


def search_ssl_info(domain, output_file=None):
    api_token = load_api_token()
    if not api_token:
        print('Please set your Shodan API key by running the script with the "--init" option.')
        return

    api = shodan.Shodan(api_token)

    try:
        # Perform a Shodan search for SSL information related to the domain
        query = 'ssl:"{}"'.format(domain)
        results = api.search(query)
    
        # Print the IP addresses
        for result in results['matches']:
            ip_address = result['ip_str']
            print(ip_address)

        # Write the IP addresses to the output file if specified
        if output_file:
            with open(output_file, 'w') as file:
                for result in results['matches']:
                    ip_address = result['ip_str']
                    file.write(ip_address + '\n')

    except shodan.APIError as e:
        if 'Invalid API key' in str(e):
            print('Invalid Shodan API key. Please set your valid API key by running the script with the "--init" option.')
            clear_api_key()
        elif str(e) == 'Access denied (403 Forbidden)':
            print('Invalid Shodan API key. Please ensure you have a Shodan API key with a membership')
        else:
            print('Error: {}'.format(e))
        return False


if __name__ == '__main__':
    # Check if the API key is already set in the environment
    if load_api_token() and not any(arg.startswith('--init') or arg == '--clear' for arg in sys.argv[1:]):
        if len(sys.argv) > 1 and sys.argv[1] == '-d':
            domain = sys.argv[2]
            output_file = None
            if '-o' in sys.argv:
                index = sys.argv.index('-o')
                if index + 1 < len(sys.argv):
                    output_file = sys.argv[index + 1]
            search_ssl_info(domain, output_file)
        else:
            print('Shodan API key is already set.')
            print('To search SSL information, use the following command:')
            print('python cipherscan.py -d <domain>')
        sys.exit(0)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Search SSL information using the Shodan API')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--domain', help='Single domain to search SSL information for')
    parser.add_argument('-o', '--output-file', help='Output file to save the results')
    parser.add_argument('--init', metavar='api_key', help='Initialize the Shodan API key')
    parser.add_argument('--clear', action='store_true', help='Clear the Shodan API key')

    # Show help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.init:
        api_token = args.init
        if is_valid_api_key(api_token):
            init_api_token(api_token)
            print('API key has been initialized and saved.')
            print('To search SSL information, use the following command:')
            print('python cipherscan.py -d <domain>')
            sys.exit(0)
        else:
            print('Invalid Shodan API key. Please set a valid API key.')
            sys.exit(1)
    elif args.clear:
        clear_api_key()
        print('API key has been cleared.')
        if len(sys.argv) > 1 and sys.argv[1] == '--clear':
            sys.exit(0)
    elif args.domain:
        search_ssl_info(args.domain, args.output_file)


