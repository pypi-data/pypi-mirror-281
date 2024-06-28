# khulnasoft-analyze

A cross-platform CLI tool which enables analyzing files with Khulnasoft Analyze.

# Prerequisites
Python 3.6 and above

Python and pip should be available in your path

# Installation
`pip install khulnasoft-analyze-cli`

# Usage

## Proxies
The CLI supports proxies. To use a proxy, set the environment variable `HTTP_PROXY` or `HTTPS_PROXY` to the proxy address.

## Login
To begin using the cli, first you should login with your API key:

`khulnasoft-analyze login <api_key>`

If you are running the CLI against an on premise deployment, enter the url:

`khulnasoft-analyze login <api_key> http://<address>/api`
 

## Analyze
Send a file or a directory for analysis in Khulnasoft Analyze.

### Usage
`khulnasoft-analyze analyze PATH`

### Parameters
PATH: Path to file or directory to send the files inside for analysis.

###  Examples:
Send a single file for analysis:

    $ khulnasoft-analyze analyze C:\threat.exe

Send all files in directory for analysis:

    $ khulnasoft-analyze analyze C:\files-to-analyze

For complete documentation please run `khulnasoft-analyze analyze --help`
 
## Analyze hashes file
Send a text file with list of hashes

### Usage
`khulnasoft-analyze analyze_by_list PATH`

### Parameters
PATH: Path to txt file.

### Example
Send txt file with hashes for analysis:

    $ khulnasoft-analyze analyze_by_list ~/files/hashes.txt

For complete documentation please run `khulnasoft-analyze analyze_by_list --help`

## Index
Send a file or a directory for indexing

### Usage
`khulnasoft-analyze index PATH INDEX_AS [FAMILY_NAME]`

### Parameters
PATH: Path to file or directory to index

INDEX_AS: `malicious` or `trusted`

FAMILY_NAME: The family name (optional)

### Example
index a single file:
    
    $ khulnasoft-analyze index ~/files/threat.exe.sample malicious family_name
    
index all files in directory:

    $ khulnasoft-analyze index ~/files/files-to-index trusted

For complete documentation please run `khulnasoft-analyze index --help`

## Index hashes file
Send a text file with list of hashes to index

### Usage 
`khulnasoft-analyze index_by_list PATH --index-as=INDEX [FAMILY_NAME]`

### Parameters
PATH: Path to txt file 

--index-as: `malicious` or `trusted`

FAMILY_NAME: The family name (optional)

### Example
Send a file with hashes and verdict for indexing:
 
    $ khulnasoft-analyze index_by_list ~/files/hashes.txt --index-as=malicious family_name

For complete documentation please run `khulnasoft-analyze index --help`

## Upload offline endpoint scan
Upload an offline scan created by running the Khulnasoft Endpoint Scanner with '-o' flag

### Usage
`khulnasoft-analyze upload_endpoint_scan OFFLINE_SCAN_DIRECTORY`

### Parameters
OFFLINE_SCAN_DIRECTORY: Path to directory with offline endpoint scan results

### Examples:
Upload a directory with offline endpoint scan results:
    
    $ khulnasoft-analyze upload_endpoint_scan /home/user/offline_scans/scan_MYPC_2019-01-01_00-00-00

For complete documentation plrase run `khulnasoft-analyze upload_endpoint_scan --help`

## Upload multiple offline endpoint scans
Upload multiple offline scans created by running the Khulnasoft Endpoint Scanner with '-o' flag

### Usage
`khulnasoft-analyze upload_endpoint_scans_in_directory OFFLINE_SCANS_ROOT_DIRECTORY`

### Parameters
OFFLINE_SCANS_ROOT_DIRECTORY: Path to root directory containing offline endpoint scan results

### Examples:
Upload a directory with offline endpoint scan results:
    
    $ khulnasoft-analyze upload_endpoint_scans /home/user/offline_scans

For complete documentation please run `khulnasoft-analyze upload_endpoint_scans_in_directory --help`

## Upload all subdirectories with .eml files to analyze
Upload a directory with .eml files

### Parameter
UPLOAD_EMAILS_IN_DIRECTORY: Path to root directory containing the .eml fiels

### Examples:
      $ khulnasoft-analyze upload_emails_in_directory /path/to/emails_root_directory

# Troubleshooting
The cli produce a log file named `khulnasoft-analyze-cli.log` in the current working directory.
To enable console output, set the environment variable `KHULNASOFT_DEBUG=1`.
