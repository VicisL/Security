# Get-CISA-Vuln

## Description
This script will download the CISA Exploitable Vulnerabilities catalog and save it as either a JSON or a CSV file.

Practically speaking it would work best as part of another script which utlizes the CISA vulnerabilities for some other mystical purpose.

## Usage
Will run without any arguments and output the vulnerability list to the local directory as "cisa_vuln.csv".

Sample run:

 - get-cisa-vuln.py --help
 - get-cisa-vuln.py -outfile "C:/My/Path/file.json" --ssl False --verbose