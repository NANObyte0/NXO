import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import argparse
from concurrent.futures import ThreadPoolExecutor

print(r"""
https://github.com/NANObyte0

███╗   ██╗██╗  ██╗ ██████╗ 
████╗  ██║╚██╗██╔╝██╔═══██╗
██╔██╗ ██║ ╚███╔╝ ██║   ██║
██║╚██╗██║ ██╔██╗ ██║   ██║
██║ ╚████║██╔╝ ██╗╚██████╔╝
╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝   Created by NANO
""")


def print_banner():
    banner = """
NXO - XSS Scanner
Usage: NXO.py -u URL [-c CRWL] [-p PAYLOADS] [-o OUTPUT]

Options:
  -u URL       Target URL to scan or crawl
  -c CRWL      Crawl the URL and list links only
  -p PAYLOADS  Path to payloads file (required for scanning)
  -o OUTPUT    File to save scan results (default: results.txt)
"""
    print(banner)

def get_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, payload):
    target_url = urljoin(url, form_details["action"])
    data = {}

    for input in form_details["inputs"]:
        if input["type"] in ["text", "search"]:
            data[input["name"]] = payload
        else:
            data[input["name"]] = "test"

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def load_payloads(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def save_result(file_path, url, payload, form_details):
    with open(file_path, "a") as f:
        f.write("[XSS Detected]\n")
        f.write(f"URL: {url}\n")
        f.write(f"Payload: {payload}\n")
        f.write("Form Details:\n")
        for key, value in form_details.items():
            f.write(f"{key}: {value}\n")
        f.write("-" * 40 + "\n")

def crawl_links(url):
    try:
        res = requests.get(url)
        soup = bs(res.content, "html.parser")
        anchors = soup.find_all("a", href=True)
        links = set()
        for a in anchors:
            link = urljoin(url, a['href'])
            links.add(link)
        print(f"[+] Found {len(links)} unique links on {url}:")
        for link in links:
            print(link)
        return links
    except Exception as e:
        print(f"[!] Error crawling the site: {e}")
        return set()

def scan_single_payload(url, form, payload, output_file):
    form_details = get_form_details(form)
    res = submit_form(form_details, url, payload)
    if payload in res.text:
        print("\n[!] XSS Detected!")
        print(f"[*] Payload used: {payload}")
        print(f"[*] Vulnerable URL: {url}")
        print("[*] Vulnerable form:")
        pprint(form_details)
        save_result(output_file, url, payload, form_details)
        return True
    return False

def scan_xss(url, payloads, output_file="results.txt"):
    forms = get_forms(url)
    print(f"[+] Found {len(forms)} form(s) on {url}")
    vulnerable = False

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for form in forms:
            for payload in payloads:
                futures.append(executor.submit(scan_single_payload, url, form, payload, output_file))

        for future in futures:
            if future.result():
                vulnerable = True

    if not vulnerable:
        print("[*] No XSS vulnerabilities detected.")
    return vulnerable

if __name__ == "__main__":
    print_banner()
    parser = argparse.ArgumentParser(description="NXO - Basic XSS scanner with crawl option")
    parser.add_argument("-u", "--url", required=True, help="Target URL to scan or crawl")
    parser.add_argument("-p", "--payloads", required=False, help="Payloads file path (required for scan)")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file to save results")
    parser.add_argument("-c", "--crawl", action="store_true", help="Only crawl the URL and get links")

    args = parser.parse_args()

    if args.crawl:
        crawl_links(args.url)
    else:
        if not args.payloads:
            print("[!] Payloads file is required for scanning.")
        else:
            payloads = load_payloads(args.payloads)
            scan_xss(args.url, payloads, args.output)
            print(f"\n[+] Scan complete. Results saved to: {args.output}")
