import requests
import logging as log
def get_cisa_exploited(verify_ssl=True):
    """Download the CISA Exploitable Vulnerabilities Catalog

    Args:
        verify_ssl (bool, optional): verify SSL certificate of the catalog. Defaults to True.

    Returns:
        obj: JSON containing the catalog items w/ the following keys: ['title','catalogVersion','dateReleased','count','vulnerabilities']
    """
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
    }
    try:
        log.info(f'Pulling CISA catalog. SSL verification enabled = {verify_ssl}')
        response = requests.get(url, headers=headers, verify=verify_ssl)
        response.raise_for_status()
        log.info(f'Successfully downloaded CISA exploitable vulnerability catalog.')
        return response.json()
    except:
        log.error(f'GET request failed: {response.status_code} -- {response.reason}')

if __name__ == "__main__":
    import pandas as pd
    import argparse
    import os

    ### Argument parsing -----------------------------------------------------------
    parser = argparse.ArgumentParser(
        prog='get-cisa-vuln',
        description='Download the CISA exploitable vulnerabilities catalog and save the output locally. Will save to "./cisa_vuln.csv" if no directory is specified.',
        epilog='Hope this helps -LK'
    )
    # Add args
    parser.add_argument('-o', '--outfile', default='cisa_vuln.csv', type=str, help='desired filename or full path - either JSON or CSV')
    parser.add_argument('-s', '--ssl', default=True, help='verify SSL certificate - True or False')
    parser.add_argument('-v', '--verbose', help='print progress', action='store_true')
    # Parse args
    args = parser.parse_args()   
    # Enable logging if verbose
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info('Verbose Output Enabled.')
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    # Ensure SSL is bool
    if args.ssl.lower() == 'true':
        args.ssl = True
    elif args.ssl.lower() == 'false':
        args.ssl = False
    else:
        log.warning(f"Invalid SSL setting, defaulting to True")
        args.ssl = True

    # Parse filename/path
    if ('\\' not in args.outfile and '/' not in args.outfile):
        out_path = './' + args.outfile
    elif os.path.isdir(os.path.dirname(args.outfile)):
        out_path = args.outfile
    else:
        log.warning(f"Output folder doesn't exist. Defaulting to './cisa_vuln.csv'")
        out_path = './cisa_vuln.csv'

    ### Execution  -----------------------------------------------------------------
    # Pull the exploited vuln list 
    response = get_cisa_exploited(args.ssl)
    log.info(f'CISA Catalog Version      : {response["catalogVersion"]}')
    log.info(f'CISA Catalog Release Date : {response["dateReleased"]}')
    log.info(f'CISA Catalog Vuln Count   : {response["count"]}')

    # Save the output
    log.info(f'Exporting CISA Catalog to: {args.outfile}')
    if out_path[-4:] == '.csv':
        t_df = pd.DataFrame(response['vulnerabilities'])
        t_df['Catalog Version'] = response["catalogVersion"]
        t_df['Catalog Date'] = response["dateReleased"]
        t_df.to_csv(out_path, index=False)
    elif out_path[-5:] == '.json':
        import json
        json_obj = json.dumps(response)
        with open(out_path, "w") as outfile:
            outfile.write(json_obj)
    else:
        log.warning(f'Invalid filetype. Defaulting to CSV')
        out_path = out_path + '.csv'