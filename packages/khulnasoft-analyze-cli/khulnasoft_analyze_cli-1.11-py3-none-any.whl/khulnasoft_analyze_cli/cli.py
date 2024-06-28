import logging
import os

import click
from khulnasoft_analyze_sdk import api
from khulnasoft_analyze_sdk import consts as sdk_consts
from khulnasoft_analyze_sdk import errors as sdk_errors
from khulnasoft_analyze_sdk.consts import CodeItemType

from khulnasoft_analyze_cli import __version__
from khulnasoft_analyze_cli import commands
from khulnasoft_analyze_cli import key_store
from khulnasoft_analyze_cli import utilities
from khulnasoft_analyze_cli.config import default_config

utilities.init_log('khulnasoft_cli', os.environ.get('KHULNASOFT_DEBUG') == '1')
logger = logging.getLogger('khulnasoft_cli')


def create_global_api():
    try:
        api_key = key_store.get_stored_api_key()
        api_url = key_store.get_stored_default_url()

        if not api_key:
            logger.exception('Cant find API key')
            click.echo('Cant find API key, please login')
            raise click.Abort()

        if api_url:
            default_config.api_url = api_url
            default_config.is_cloud = False

        api.set_global_api(api_key, default_config.api_version, default_config.api_url)
        sdk_consts.USER_AGENT += f'/CLI-{__version__}'

    except sdk_errors.InvalidApiKey:
        logger.exception('Invalid api key error')
        click.echo('Invalid API key error, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')
        raise click.Abort()


@click.group(context_settings=dict(help_option_names=['-h', '--help'], max_content_width=120),
             help=f'Khulnasoft Labs Ltd. Khulnasoft Analyze CLI {__version__}')
def main_cli():
    pass


@main_cli.command('login', short_help='Login to Khulnasoft Analyze')
@click.argument('api_key', type=click.UUID)
@click.argument('api_url', required=False, default=None, type=click.STRING)
def login(api_key: str, api_url: str):
    """Login to Khulnasoft Analyze to perform analyses.

    \b
    API_KEY: API key or invite code for Khulnasoft Analyze.

    \b
    API_URL: Khulnasoft Analyze URL in case you have on premise deployment.

    \b
    Example:
      $ khulnasoft-analyze login edb45d954da54e8e980078001d8921cc
    """
    try:
        if api_url:
            if api_url[-1] != '/':
                api_url += '/'
            if not api_url.endswith('/api/'):
                api_url += 'api/'
        commands.login(str(api_key), api_url)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('analyze', short_help='Send a file or a directory for analysis')
@click.option('--no-unpacking', is_flag=True, help='Should the analysis skip unpacking')
@click.option('--no-static-extraction', is_flag=True, help='Should the analysis skip static extraction')
@click.option('--code-item-type', type=click.Choice([c.value for c in CodeItemType]), default=None,
              help='The type of the binary file uploaded')
@click.option('--ignore-directory-count-limit',
              is_flag=True,
              help='ignore directory count limit ({} files)'.format(default_config.unusual_amount_in_dir))
@click.argument('path', type=click.Path(exists=True))
def analyze(path: str,
            no_unpacking: bool,
            no_static_extraction: bool,
            code_item_type: str,
            ignore_directory_count_limit: bool):
    """ Send a file or a directory for analysis in Khulnasoft Analyze.

    \b
    PATH: Path to file or directory to send the files inside for analysis.

    \b
    Examples:
      Send a single file for analysis:
      $ khulnasoft-analyze analyze ~/files/threat.exe.sample
      \b
      Send all files in directory for analysis:
      $ khulnasoft-analyze analyze ~/files/files-to-analyze
    """
    try:
        create_global_api()

        if not no_unpacking:
            no_unpacking = None
        if not no_static_extraction:
            no_static_extraction = None

        if os.path.isfile(path):
            commands.analyze_file_command(file_path=path,
                                          disable_dynamic_unpacking=no_unpacking,
                                          disable_static_unpacking=no_static_extraction,
                                          code_item_type=code_item_type)
        else:
            commands.analyze_directory_command(path=path,
                                               disable_dynamic_unpacking=no_unpacking,
                                               disable_static_unpacking=no_static_extraction,
                                               code_item_type=code_item_type,
                                               ignore_directory_count_limit=ignore_directory_count_limit)
    except click.Abort:
        raise
    except sdk_errors.InsufficientQuota:
        logger.exception('Insufficient quota')
        click.echo('Insufficient quota, please contact us at support@khulnasoft.com ')
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('analyze_by_list', short_help='Send a text file with list of hashes')
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
def analyze_by_list(path):
    """ Send a text file with hashes for analysis in Khulnasoft Analyze.

    \b
    PATH: Path to txt file.

    \b
    Examples:
      Send txt file with hashes for analysis:
      $ khulnasoft-analyze analyze_by_list ~/files/hashes.txt
    """
    try:
        create_global_api()

        commands.analyze_by_txt_file_command(path=path)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('index_by_list', short_help='Send a text file with list of hashes, verdict, family name if malicious')
@click.argument('path', type=click.Path(exists=True, dir_okay=False))
@click.option('--index-as', type=click.Choice(['malicious', 'trusted'], case_sensitive=True))
@click.argument('family_name', required=False, type=click.STRING, default=None)
def index_by_list(path: str, index_as: str, family_name: str):
    """
    Send a text file with hashes for indexing in Khulnasoft Analyze.

    \b
    PATH: Path to a txt file with hashes

    \b
    Examples:
      $ khulnasoft-analyze index_by_list ~/files/hashes.txt malicious family_name
      \b
    """
    try:
        index_type = sdk_consts.IndexType.from_str(index_as)

        if index_type == sdk_consts.IndexType.MALICIOUS and family_name is None:
            click.echo('family_name is mandatory if the index type is malicious')
            return

        create_global_api()

        commands.index_by_txt_file_command(path=path, index_as=index_as, family_name=family_name)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('index', short_help='index a file or a directory')
@click.argument('path', type=click.Path(exists=True))
@click.option('--index-as', type=click.Choice(['malicious', 'trusted'], case_sensitive=True))
@click.argument('family_name', required=False, type=click.STRING, default=None)
@click.option('--ignore-directory-count-limit',
              is_flag=True,
              help='ignore directory count limit ({} files)'.format(default_config.unusual_amount_in_dir))
def index(path: str, index_as: str, family_name: str, ignore_directory_count_limit: bool):
    """ Send a file or a directory for indexing

    \b
    PATH: Path to file or directory to index

    \b
    Examples:
      index a single file:
      $ khulnasoft-analyze index ~/files/threat.exe.sample malicious family_name
      \b
      index all files in directory:
      $ khulnasoft-analyze index ~/files/files-to-index trusted
    """
    try:
        index_type = sdk_consts.IndexType.from_str(index_as)

        if index_type == sdk_consts.IndexType.MALICIOUS and family_name is None:
            click.echo('family_name is mandatory if the index type is malicious')
            return

        create_global_api()

        if os.path.isfile(path):
            commands.index_file_command(file_path=path, index_as=index_as, family_name=family_name)
        else:
            commands.index_directory_command(directory_path=path,
                                             index_as=index_as,
                                             family_name=family_name,
                                             ignore_directory_count_limit=ignore_directory_count_limit)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('upload_endpoint_scan', short_help='upload a directory with offline endpoint scan results')
@click.argument('offline_scan_directory', type=click.Path(exists=True))
@click.option('--force', is_flag=True, default=False, help='Upload scan even if it was already uploaded')
@click.option('--max-concurrent', default=0, type=int, help='Maximum number of concurrent uploads.')
def upload_endpoint_scan(offline_scan_directory: str, force: bool, max_concurrent: int):
    """ Upload a directory with offline endpoint scan results


    OFFLINE_SCAN_DIRECTORY: Path to directory with offline endpoint scan results


    Examples:
      upload a directory with offline endpoint scan results:

      $ khulnasoft-analyze upload_endpoint_scan /path/to/endpoint_scan_results
    """
    try:
        create_global_api()
        commands.upload_offline_endpoint_scan(offline_scan_directory=offline_scan_directory,
                                              force=force,
                                              max_concurrent_uploads=max_concurrent)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('upload_endpoint_scans_in_directory',
                  short_help='upload all subdirectories with offline endpoint scan results')
@click.argument('offline_scans_root_directory', type=click.Path(exists=True))
@click.option('--force', is_flag=True, default=False, help='Upload scans even if they were already uploaded')
@click.option('--max-concurrent', default=0, type=int, help='Maximum number of concurrent uploads.')
def upload_endpoint_scans_in_directory(offline_scans_root_directory: str, force: bool = False, max_concurrent: int = 0):
    """ Upload all subdirectories with offline endpoint scan results


    OFFLINE_SCANS_ROOT_DIRECTORY: Path to root directory containing offline endpoint scan results


    Examples:
      upload a directory with offline endpoint scan results:

      $ khulnasoft-analyze upload_endpoint_scans_in_directory /path/to/endpoint_scan_results_root
    """
    try:
        create_global_api()
        commands.upload_multiple_offline_endpoint_scans(offline_scans_root_directory=offline_scans_root_directory,
                                                        force=force,
                                                        max_concurrent_uploads=max_concurrent)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


@main_cli.command('upload_emails_in_directory',
                  short_help='upload all subdirectories with .emal files')
@click.argument('emails_root_directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--ignore-directory-count-limit',
              is_flag=True,
              help='ignore directory count limit ({} files)'.format(default_config.unusual_amount_in_dir))
def upload_emails_in_directory(emails_root_directory: str, ignore_directory_count_limit: bool = False):
    """ Upload all subdirectories with .eml files to analyze


    UPLOAD_EMAILS_IN_DIRECTORY: Path to root directory containing the .eml fiels


    Examples:
      upload a directory with .eml files:

      $ khulnasoft-analyze upload_emails_in_directory /path/to/emails_root_directory
    """
    try:
        create_global_api()
        commands.send_phishing_emails_from_directory_command(path=emails_root_directory,
                                                             ignore_directory_count_limit=ignore_directory_count_limit)
    except click.Abort:
        raise
    except Exception:
        logger.exception('Unexpected error occurred')
        click.echo('Unexpected error occurred, please contact us at support@khulnasoft.com '
                   f'and attach the log file in {utilities.log_file_path}')


if __name__ == '__main__':
    try:
        main_cli()

    except Exception as e:
        logger.exception(f'Unexpected error occurred {e}')
        click.echo('Unexpected error occurred')
