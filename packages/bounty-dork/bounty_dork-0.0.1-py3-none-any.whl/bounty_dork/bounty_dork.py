# /usr/bin/python3
import argparse
import sys

# TO get stacktrace in case of segfault
# gdb pypy3; run bounty_drive.py
# import faulthandler
# faulthandler.enable(file=sys.stderr, all_threads=True)

import utils.logger
from utils.logger import *


from termcolor import cprint
import os
import csv
import concurrent.futures

from tqdm import tqdm

from dorks.search_engine_dorking import (
    google_search_with_proxy,
    launch_google_dorks_and_search_attack,
)

from dorks.github_dorking import *

from reporting.results_manager import (
    get_last_processed_ids,
    get_processed_dorks,
)
from vpn_proxies.proxies_manager import round_robin_proxies, setup_proxies
from vpn_proxies.vpn_manager import setup_vpn


from utils.banner import *
from utils.banner import load_animation


import configparser

os.system("clear")

#########################################################################################
# Main function
#########################################################################################


def create_argument_parser():
    """
    Creates an argument parser for command-line arguments.
    
    Returns:
    - parser: the argument parser
    """
    parser = argparse.ArgumentParser(description="Configuration and Argument Parser")

    parser.add_argument("--config", type=str, required=True, help="Path to the configuration file")

    # [Settings] section
    parser.add_argument("--extension", type=str, help="Extension")
    parser.add_argument("--subdomain", type=bool, help="Use subdomain")
    parser.add_argument("--do_web_scap", type=bool, help="Do web scraping")
    parser.add_argument("--target_file", type=str, help="Target file")
    parser.add_argument("--exclusion_file", type=str, help="Exclusion file")
    parser.add_argument("--target_login", type=str, nargs='*', help="Target login")
    parser.add_argument("--logging", type=str, help="Logging level")
    parser.add_argument("--max_thread", type=int, help="Maximum number of threads")
    parser.add_argument("--runtime_save", type=bool, help="Runtime save")
    parser.add_argument("--keyboard_interrupt_save", type=bool, help="Keyboard interrupt save")

    # [Bounty] section
    parser.add_argument("--need_specific_user_agent", type=bool, help="Need specific user agent")
    parser.add_argument("--target_user_agent", type=str, help="Target user agent")
    parser.add_argument("--hackerone_username", type=str, help="HackerOne username")

    # [GoogleDorking] section
    parser.add_argument("--do_dorking_google", type=bool, help="Do Google dorking")
    parser.add_argument("--total_output", type=int, help="Total output")
    parser.add_argument("--page_no", type=int, help="Page number")
    parser.add_argument("--default_total_output", type=int, help="Default total output")
    parser.add_argument("--default_page_no", type=int, help="Default page number")
    parser.add_argument("--lang", type=str, help="Language")
    parser.add_argument("--use_selenium", type=bool, help="Use Selenium")
    parser.add_argument("--do_xss", type=bool, help="Do XSS")
    parser.add_argument("--do_sqli", type=bool, help="Do SQLi")
    
    # [GithubDorking] section
    parser.add_argument("--do_dorking_github", type=bool, help="Do GitHub dorking")

    # [ShodanDorking] section
    parser.add_argument("--do_dorking_shodan", type=bool, help="Do Shodan dorking")

    # [Proxy] section
    parser.add_argument("--use_proxy", type=bool, help="Use proxy")
    parser.add_argument("--use_free_proxy_file", type=bool, help="Use free proxy file")
    parser.add_argument("--use_free_proxy", type=bool, help="Use free proxy")
    parser.add_argument("--use_nordvpn_proxy", type=bool, help="Use NordVPN proxy")
    parser.add_argument("--proxies", type=str, nargs='*', help="Proxies")
    parser.add_argument("--proxy_mean_delay", type=int, help="Proxy mean delay")
    parser.add_argument("--proxy_factor", type=int, help="Proxy factor")

    # [VPN] section
    parser.add_argument("--use_vpn", type=bool, help="Use VPN")
    parser.add_argument("--use_nordvpn", type=bool, help="Use NordVPN")
    parser.add_argument("--nord_vpn_login", type=str, nargs='*', help="NordVPN login")

    # [Tor] section
    parser.add_argument("--use_tor", type=bool, help="Use Tor")

    # [Delay] section
    parser.add_argument("--initial_delay", type=int, help="Initial delay")
    parser.add_argument("--delay_factor", type=int, help="Delay factor")
    parser.add_argument("--long_delay", type=int, help="Long delay")
    parser.add_argument("--max_delay", type=int, help="Max delay")
    parser.add_argument("--request_delay", type=int, help="Request delay")
    parser.add_argument("--waf_delay", type=int, help="WAF delay")

    # [Rate] section
    parser.add_argument("--rate_per_minute", type=int, help="Rate per minute")
    parser.add_argument("--current_delay", type=int, help="Current delay")

    return parser
    
def read_config(file_path):
    """
    Reads the configuration file and returns the settings as a dictionary.
    """
    config = configparser.ConfigParser()
    config.read(file_path)

    settings = {
        # Settings
        "extension": config["Settings"].get("extension"),
        "subdomain": config["Settings"].getboolean("subdomain"),
        "do_web_scrap": config["Settings"].getboolean("do_web_scrap"),
        "target_file": config["Settings"].get("target_file"),
        "max_thread": config["Settings"].getint("max_thread", 30),
        "logging": config["Settings"].get("logging", "DEBUG"),
        "runtime_save": config["Settings"].getboolean("runtime_save"),
        "keyboard_interrupt_save": config["Settings"].getboolean(
            "keyboard_interrupt_save"
        ),
        # Bounty
        "need_specific_user_agent": config["Bounty"].getboolean(
            "need_specific_user_agent"
        ),
        "target_user_agent": config["Bounty"].get("target_user_agent"),
        "hackerone_username": config["Bounty"].get("hackerone_username"),
        # Google Dorking
        "do_dorking_google": config["GoogleDorking"].getboolean("do_dorking_google"),
        "total_output": config["GoogleDorking"].getint("total_output"),
        "page_no": config["GoogleDorking"].getint("page_no"),
        "default_total_output": config["GoogleDorking"].getint("default_total_output"),
        "default_page_no": config["GoogleDorking"].getint("default_page_no"),
        "lang": config["GoogleDorking"].get("lang"),
        "use_selenium": config["GoogleDorking"].getboolean("use_selenium"),
        "do_xss": config["GoogleDorking"].getboolean("do_xss"),
        "do_sqli": config["GoogleDorking"].getboolean("do_sqli"),
        # Github Dorking
        "do_dorking_github": config["GithubDorking"].getboolean("do_dorking_github"),
        # Github Dorking
        "do_dorking_shodan": config["GithubDorking"].getboolean("do_dorking_github"),
        # Proxy
        "use_proxy": config["Proxy"].getboolean("use_proxy"),
        "use_free_proxy_file": config["Proxy"].getboolean("use_free_proxy_file"),
        "use_free_proxy": config["Proxy"].getboolean("use_free_proxy"),
        "use_nordvpn_proxy": config["Proxy"].getboolean("use_nordvpn_proxy"),
        "proxies": config["Proxy"].get("proxies"),
        "proxy_mean_delay": config["Proxy"].getint("proxy_mean_delay"),
        "proxy_factor": config["Proxy"].getint("proxy_factor"),
        # VPN
        "use_vpn": config["VPN"].getboolean("use_vpn"),
        "use_nordvpn": config["VPN"].getboolean("use_nordvpn"),
        "nord_vpn_login": config["VPN"].get("nord_vpn_login"),
        # Delay
        "initial_delay": config["Delay"].getint("initial_delay"),
        "delay_factor": config["Delay"].getint("delay_factor"),
        "long_delay": config["Delay"].getint("long_delay"),
        "max_delay": config["Delay"].getint("max_delay"),
        "request_delay": config["Delay"].getint("request_delay"),
        "waf_delay": config["Delay"].getint("waf_delay"),
        # Rate
        "rate_per_minute": config["Rate"].getint("rate_per_minute"),
        "current_delay": config["Rate"].getint("current_delay"),
    }

    return settings


def get_user_input(config_file="configs/config.ini"):
    """
    Collects user input from a configuration file.

    Args:
        config_file (str): Path to the configuration file. Default is "configs/config.ini".

    Returns:
        tuple: A tuple containing the following values:
            - config (dict): The configuration settings read from the file.
            - last_dork_id (int): The last processed dork ID.
            - last_link_id (int): The last processed link ID.
            - last_attack_id (int): The last processed attack ID.
            - categories (list): A list of categories.

    Raises:
        FileNotFoundError: If the specified configuration file does not exist.
    """
    config = {}
    if args.config:
        config = read_config(args.config)
    cli_args = vars(args)

    # Override config settings with command-line arguments if provided
    for key in cli_args:
        if cli_args[key] is not None:
            config[key] = cli_args[key]

    categories = []

    # Define headers based on enabled parameters
    setup_experiment_folder(config, categories)

    cprint(
        f"-Extension: {config['extension']}\n-Total Output: {config['total_output']}\n-Page No: {config['page_no']}\n-Do Google Dorking: {config['do_dorking_google']}\n-Do Github Dorking {config['do_dorking_github']}\n-Domain: {config['subdomain']}\n-Use Proxy: {config['use_proxy']}",
        "blue",
        file=sys.stderr,
    )

    if config["use_proxy"]:
        setup_proxies(config)

    if config["use_vpn"]:
        setup_vpn(config)

    last_dork_id, last_link_id, last_attack_id = get_last_processed_ids(config)

    if config["subdomain"]:
        proxies = config["proxies"]
        if config["use_proxy"] and len(proxies) == 0:
            cprint(
                f"Using proxies -> you should have at least one UP",
                "red",
                file=sys.stderr,
            )
            exit()

        if not config["use_proxy"]:
            proxies = [None]

        proxy_cycle = round_robin_proxies(proxies)

        saved_total_output = config["total_output"]
        current_total_output = 10
        config["total_output"] = current_total_output
        search_tasks_with_proxy = []

        number_of_worker = 30 
        cprint(f"Number of workers: {number_of_worker}", "blue", file=sys.stderr)

        with open(config["target_file"], "r") as file:
            subdomain_list = file.read().splitlines()
            if len(subdomain_list) >= last_dork_id:
                for domain in subdomain_list:
                    processed = False
                    for category in categories:
                        with open(config["dorking_csv"], mode="r", newline="") as file:
                            reader = csv.DictReader(file)
                            for row in reader:
                                if domain in row["dork"]:
                                    processed = True

                        if not processed:
                            proxy = next(proxy_cycle)
                            search_tasks_with_proxy.append(
                                {
                                    "dork": "",
                                    "proxy": proxy,
                                    "category": category,
                                    "domain": domain,
                                }
                            )
                            cprint(
                                f"Initial Dorking search for based targets {domain} - {category}",
                                "yellow",
                                file=sys.stderr,
                            )
                        else:
                            cprint(
                                f"Already initialized Dorking search for based targets {domain} - {category}",
                                color="cyan",
                                file=sys.stderr,
                            )

            processed_dorks = get_processed_dorks(config)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=number_of_worker
            ) as executor:
                future_to_search = {
                    executor.submit(
                        google_search_with_proxy,
                        task["dork"],
                        task["proxy"],
                        task["category"],
                        config,
                        task["domain"],
                        processed_dorks,
                    ): task
                    for task in search_tasks_with_proxy
                }
                for future in tqdm(
                    concurrent.futures.as_completed(future_to_search),
                    total=len(future_to_search),
                    desc="Initializing Dorking of targets",
                    unit="site",
                ):
                    task = future_to_search[future]
                    # try:
                    last_dork_id = future.result()

            config["subdomain"] = subdomain_list
    else:
        config["subdomain"] = [None]

    config["total_output"] = saved_total_output

    return config, last_dork_id, last_link_id, last_attack_id, categories


def setup_experiment_folder(config, categories):
    folder_name = os.path.join(
        "outputs/reports/", config["target_file"].split("_")[-1].replace(".txt", "")
    )
    config["experiment_folder"] = folder_name
    if not os.path.exists(folder_name):
        cprint(f"Creating folder {folder_name}", "blue", file=sys.stderr)
        os.makedirs(folder_name)
    setup_csv(config, categories, folder_name)


def setup_csv(config, categories, folder_name):
    """Set up the CSV file for storing experiment results.

    This function creates the necessary CSV file and writes the headers based on the provided configuration.

    Args:
        config (dict): A dictionary containing the configuration settings.
        categories (list): A list of categories to be included in the CSV headers.

    """
    csv_headers = [
        "dork_id",
        "link_id",
        "attack_id",
        "category",
        "url",
        "dork",
        "success",
        "payload",
    ]
    config["dorking_csv"] = os.path.join(
        folder_name, folder_name.split("/")[-1] + "_dorking.csv"
    )
    if config["do_dorking_github"]:
        csv_headers.append("github_success")
    if config["do_xss"]:
        categories.append("xss")
    if config["do_sqli"]:
        categories.append("sqli")
    if (
        not os.path.exists(config["dorking_csv"])
        or os.path.getsize(config["dorking_csv"]) == 0
    ):
        with open(config["dorking_csv"], mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


if __name__ == "__main__":
    try:
        load_animation()

        # TODO add worker/master processes to handle multiple tasks and be faster

        # Create argument parser
        parser = create_argument_parser()

        # Parse command-line arguments
        args = parser.parse_args()

        (
            config,
            last_dork_id,
            last_link_id,
            last_attack_id,
            categories,
        ) = get_user_input(args)
        

        if config["do_dorking_google"]:
            cprint(
                "\nStarting Google dorking scan phase...\n", "blue", file=sys.stderr
            )
            launch_google_dorks_and_search_attack(config, categories)

        if config["do_dorking_github"]:
            cprint(
                "\nStarting Github dorking scan phase...\n", "blue", file=sys.stderr
            )
            raise NotImplementedError("Github dorking scan phase not implemented yet")
            launch_github_dorks_and_search_attack(config, categories)

        if config["do_dorking_shodan"]:
            cprint(
                "\nStarting Shodan dorking scan phase...\n", "blue", file=sys.stderr
            )
            raise NotImplementedError("Shodan dorking scan phase not implemented yet")
            launch_shodan_dorks_and_search_attack(config, categories)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        cprint(f"{exc_type}, {fname}, {exc_tb.tb_lineno}", "red", file=sys.stderr)
        cprint(f"Error: {e}", "red", file=sys.stderr)
    except KeyboardInterrupt:
        cprint("Exiting...", "red", file=sys.stderr)
        # TODO save progress
    finally:
        sys.stderr = orig_stdout
        f.close()
