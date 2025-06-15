try:
    import requests
    import bs4
    from bs4 import BeautifulSoup as bs
    from urllib.parse import urljoin, urlparse, parse_qs
    from pprint import pprint
    import argparse
    from concurrent.futures import ThreadPoolExecutor
    import sys
except ImportError as e:
    print(f"[!] Missing Required Library: {e}")
    print("[+] Installing Required Libraries...")

    required_libraries = [
        "sys",
        "pprint",
        "requests",
        "argparse",
        "urllib3",
        "beautifulsoup4",
        "concurrent.futures"
    ]
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", *required_libraries])
    print("[+] Libraries Installed Successfully!")

    import requests
    from bs4 import BeautifulSoup as bs
    from urllib.parse import urljoin, urlparse, parse_qs
    from pprint import pprint
    import argparse
    from concurrent.futures import ThreadPoolExecutor
    import sys

def print_banner():
    banner = """
    \033[1;31m███╗   ██╗\033[0m\033[1;32m██╗  ██╗\033[0m\033[1;33m ██████╗\033[0m
    \033[1;31m████╗  ██║\033[0m\033[1;32m╚██╗██╔╝\033[0m\033[1;33m██╔═══██╗\033[0m
    \033[1;31m██╔██╗ ██║\033[0m\033[1;32m ╚███╔╝\033[0m\033[1;33m ██║ 0 ██║\033[0m
    \033[1;31m██║╚██╗██║\033[0m\033[1;32m ██╔██╗\033[0m\033[1;33m ██║ 0 ██║\033[0m
    \033[1;31m██║ ╚████║\033[0m\033[1;32m██╔╝ ██╗\033[0m\033[1;33m╚██████╔╝\033[0m
    \033[1;31m╚═╝  ╚═══╝\033[0m\033[1;32m╚═╝  ╚═╝\033[0m\033[1;33m ╚═════╝\033[0m
    \033[1;37m╔═════════════════════════╗\033[0m
    \033[1;37m║\033[0m \033[1;31m Advanced\033[0m \033[1;32mXSS\033[0m \033[1;33mScanner\033[0m \033[1;37m  ║\033[0m
    \033[1;37m║\033[0m \033[1;36mDev By\033[0m \033[1;35mNANO\033[0m \033[1;34m&\033[0m \033[1;30mDr.FarFar\033[0m \033[1;37m║\033[0m
    \033[1;37m╚═════════════════════════╝\033[0m
"""
    print(banner)

def print_usage():
    usage = """
    \033[1;36mNXO - Advanced XSS Scanner With Crawl Option\033[0m
    \033[1;33mUsage:\033[0m \033[1;32mNXO.py\033[0m [\033[1;35m-a\033[0m] [\033[1;35m-ab\033[0m] [\033[1;35m-b\033[0m] [\033[1;35m-c\033[0m] [\033[1;35m-ck\033[0m] [\033[1;35m-cmn\033[0m] [\033[1;35m-cr\033[0m] [\033[1;35m-d\033[0m] [\033[1;35m-e\033[0m] [\033[1;35m-f\033[0m] [\033[1;35m-hd\033[0m] 
                  [\033[1;35m-i\033[0m] [\033[1;35m-j\033[0m] [\033[1;35m-l\033[0m] [\033[1;35m-m\033[0m] [\033[1;35m-o\033[0m] [\033[1;35m-p\033[0m] [\033[1;35m-q\033[0m] [\033[1;35m-r\033[0m] [\033[1;35m-s\033[0m] [\033[1;35m-sc\033[0m] [\033[1;35m-sp\033[0m] [\033[1;35m-t\033[0m]
                  [\033[1;35m-th\033[0m] [\033[1;35m-to\033[0m] [\033[1;35m-u\033[0m] [\033[1;35m-ua\033[0m] [\033[1;35m-v\033[0m] [\033[1;35m-vb\033[0m] [\033[1;35m-vs\033[0m] [\033[1;35m-w\033[0m] [\033[1;35m-x\033[0m] [\033[1;35m-y\033[0m]

• Options:
  \033[33m-a, --advanced\033[0m
  \033[32mPerform advanced XSS scan including URL parameters and headers\033[0m

  \033[33m-ab, --about\033[0m
  \033[32mDisplay developer information, version, social media accounts, email, and a list of contributors\033[0m

  \033[33m-b, --body\033[0m
  \033[32mScan and analyze the HTML body content for potential XSS injection points\033[0m

  \033[33m-c, --config\033[0m
  \033[32mLoad scanning configuration from a custom config file\033[0m

  \033[33m-ck, --cookie\033[0m
  \033[32mTest for XSS vulnerabilities in cookie values and cookie-based authentication\033[0m

  \033[33m-cmn, --comment\033[0m
  \033[32mScan HTML comments for potential XSS vulnerabilities\033[0m

  \033[33m-cr, --crawl\033[0m
  \033[32mCrawl the target website to discover and map all accessible URLs and endpoints\033[0m

  \033[33m-d, --detailed\033[0m
  \033[32mConduct in-depth XSS analysis including DOM-based vulnerabilities and client-side script injection\033[0m

  \033[33m-e, --element\033[0m
  \033[32mScan HTML elements and attributes for potential XSS injection vulnerabilities\033[0m

  \033[33m-f, --form\033[0m
  \033[32mTest all web forms for XSS vulnerabilities in input fields and form submissions\033[0m

  \033[33m-h, --help\033[0m
  \033[32mDisplay detailed help information and command usage instructions\033[0m

  \033[33m-hd, --header\033[0m
  \033[32mAnalyze HTTP response headers for potential XSS vulnerabilities and header injection\033[0m

  \033[33m-i, --input\033[0m
  \033[32mTest all input fields and parameters for XSS vulnerabilities\033[0m

  \033[33m-j, --json\033[0m
  \033[32mScan JSON responses and API endpoints for XSS vulnerabilities\033[0m

  \033[33m-l, --link\033[0m
  \033[32mAnalyze hyperlinks and URL parameters for potential XSS injection points\033[0m

  \033[33m-m, --method\033[0m
  \033[32mTest different HTTP methods (GET, POST, etc.) for XSS vulnerabilities\033[0m

  \033[33m-o, --output\033[0m
  \033[32mSpecify the output file path to save scan results (default: results.txt)\033[0m

  \033[33m-p, --payloads\033[0m
  \033[32mSpecify the path to the file containing XSS payloads for testing\033[0m

  \033[33m-q, --quiet\033[0m
  \033[32mRun the scanner in quiet mode with minimal console output\033[0m

  \033[33m-r, --recursive\033[0m
  \033[32mPerform recursive scanning of discovered URLs and endpoints\033[0m

  \033[33m-s, --save\033[0m
  \033[32mSave detailed scan results in multiple formats (JSON, XML, HTML)\033[0m

  \033[33m-sc, --scan\033[0m
  \033[32mExecute basic XSS vulnerability scanning on the target\033[0m

  \033[33m-sp, --script\033[0m
  \033[32mTest for XSS vulnerabilities in JavaScript code and script tags\033[0m

  \033[33m-t, --timeout\033[0m
  \033[32mSet custom timeout value for requests in seconds\033[0m

  \033[33m-th, --threads\033[0m
  \033[32mSpecify number of concurrent threads for scanning\033[0m

  \033[33m-to, --tor\033[0m
  \033[32mUse Tor network for anonymous scanning\033[0m

  \033[33m-u, --url\033[0m
  \033[32mSpecify the target URL to scan for XSS vulnerabilities\033[0m

  \033[33m-ua, --user-agents\033[0m
  \033[32mSpecify a custom user agents file for scanning\033[0m

  \033[33m-v, --validate\033[0m
  \033[32mValidate discovered vulnerabilities before reporting\033[0m

  \033[33m-vb, --verbose\033[0m
  \033[32mEnable verbose output with detailed scanning information\033[0m

  \033[33m-vs, --version\033[0m
  \033[32mDisplay the current version of the XSS scanner\033[0m

  \033[33m-w, --wordlist\033[0m
  \033[32mSpecify a custom wordlist file for crawling and scanning\033[0m

  \033[33m-x, --xml\033[0m
  \033[32mTest for XSS vulnerabilities in XML responses and XML parsing\033[0m

  \033[33m-y, --proxy\033[0m
  \033[32mUse a proxy server for scanning (format: http://host:port)\033[0m
"""
    print(usage)

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
        print(f"[+] Found {len(links)} Unique Links on {url}:")
        for link in links:
            print(link)
        return links
    except Exception as e:
        print(f"[!] Error Crawling The Site: {e}")
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
    print(f"[+] Found {len(forms)} Form(s) On {url}")
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
        print("[*] No XSS Vulnerabilities Detected.")
    return vulnerable

def load_user_agents(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def advanced_xss_scan(url, payloads, output_file):
    print("[+] Starting Advanced XSS Scan...")
    vulnerable = False

    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    for param, values in params.items():
        for value in values:
            for payload in payloads:
                test_url = url.replace(f"{param}={value}", f"{param}={payload}")
                try:
                    res = requests.get(test_url)
                    if payload in res.text:
                        print("\n[!] Reflected XSS Detected in URL Parameter!")
                        print(f"[*] Parameter: {param}")
                        print(f"[*] Payload: {payload}")
                        print(f"[*] Vulnerable URL: {test_url}")
                        save_result(output_file, test_url, payload, {"parameter": param})
                        vulnerable = True
                except Exception as e:
                    print(f"[!] Error Testing URL Parameter {param}: {e}")
    

    headers_to_test = ["User-Agent", "Referer", "Cookie"]
    for header in headers_to_test:
        for payload in payloads:
            try:
                res = requests.get(url, headers={header: payload})
                if payload in res.text:
                    print(f"\n[!] Reflected XSS Detected in {header} Header!")
                    print(f"[*] Payload: {payload}")
                    print(f"[*] Vulnerable URL: {url}")
                    save_result(output_file, url, payload, {"header": header})
                    vulnerable = True
            except Exception as e:
                print(f"[!] Error Testing Header {header}: {e}")
    

    user_agents = load_user_agents("user_agents.txt")
    for user_agent in user_agents:
        for payload in payloads:
            try:
                res = requests.get(url, headers={"User-Agent": user_agent})
                if payload in res.text:
                    print(f"\n[!] Reflected XSS Detected With User-Agent: {user_agent}!")
                    print(f"[*] Payload: {payload}")
                    print(f"[*] Vulnerable URL: {url}")
                    save_result(output_file, url, payload, {"user_agent": user_agent})
                    vulnerable = True
            except Exception as e:
                print(f"[!] Error Testing With User-Agent {user_agent}: {e}")
    
    if not vulnerable:
        print("[*] No advanced XSS Vulnerabilities Detected.")
    return vulnerable

def detailed_xss_scan(url, payloads, output_file):
    print("[+] Starting Detailed XSS Scan...")
    vulnerable = False

    try:
        res = requests.get(url)
        soup = bs(res.content, "html.parser")
        scripts = soup.find_all("script")
        for script in scripts:
            script_content = script.string
            if script_content:
                for payload in payloads:
                    if payload in script_content:
                        print("\n[!] DOM-based XSS Detected in Script!")
                        print(f"[*] Payload: {payload}")
                        print(f"[*] Vulnerable URL: {url}")
                        save_result(output_file, url, payload, {"script": script_content})
                        vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking For DOM-Based XSS: {e}")
    

    forms = get_forms(url)
    for form in forms:
        form_details = get_form_details(form)
        for input_field in form_details["inputs"]:
            if input_field["type"] in ["text", "search"]:
                for payload in payloads:
                    res = submit_form(form_details, url, payload)
                    if payload in res.text:
                        print("\n[!] XSS Detected in Input Field!")
                        print(f"[*] Input field: {input_field['name']}")
                        print(f"[*] Payload: {payload}")
                        print(f"[*] Vulnerable URL: {url}")
                        save_result(output_file, url, payload, {"input_field": input_field})
                        vulnerable = True
    
    if not vulnerable:
        print("[*] No detailed XSS Vulnerabilities Detected.")
    return vulnerable

def check_json_xss(url, payloads, output_file):
    print("[+] Checking For XSS in JSON Responses...")
    vulnerable = False
    try:
        res = requests.get(url)
        if res.headers.get('Content-Type', '').startswith('application/json'):
            json_data = res.json()
            for payload in payloads:
                if any(payload in str(value) for value in json_data.values()):
                    print("\n[!] XSS Detected in JSON Response!")
                    print(f"[*] Payload: {payload}")
                    print(f"[*] Vulnerable URL: {url}")
                    save_result(output_file, url, payload, {"json_data": json_data})
                    vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking JSON Response: {e}")
    return vulnerable

def check_cookie_xss(url, payloads, output_file):
    print("[+] Testing For XSS in Cookies...")
    vulnerable = False
    for payload in payloads:
        try:
            res = requests.get(url, cookies={"test_cookie": payload})
            if payload in res.text:
                print("\n[!] XSS Detected in Cookie!")
                print(f"[*] Payload: {payload}")
                print(f"[*] Vulnerable URL: {url}")
                save_result(output_file, url, payload, {"cookie": "test_cookie"})
                vulnerable = True
        except Exception as e:
            print(f"[!] Error Testing Cookie: {e}")
    return vulnerable

def check_xml_xss(url, payloads, output_file):
    print("[+] Checking For XSS in XML Responses...")
    vulnerable = False
    try:
        res = requests.get(url)
        if res.headers.get('Content-Type', '').startswith('application/xml'):
            xml_data = res.text
            for payload in payloads:
                if payload in xml_data:
                    print("\n[!] XSS Detected in XML Response!")
                    print(f"[*] Payload: {payload}")
                    print(f"[*] Vulnerable URL: {url}")
                    save_result(output_file, url, payload, {"xml_data": xml_data})
                    vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking XML Response: {e}")
    return vulnerable

def check_header_xss(url, payloads, output_file):
    print("[+] Testing For XSS in HTTP Response Headers...")
    vulnerable = False
    for payload in payloads:
        try:
            res = requests.get(url, headers={"X-Test-Header": payload})
            if payload in res.text:
                print("\n[!] XSS Detected in HTTP Response Header!")
                print(f"[*] Payload: {payload}")
                print(f"[*] Vulnerable URL: {url}")
                save_result(output_file, url, payload, {"header": "X-Test-Header"})
                vulnerable = True
        except Exception as e:
            print(f"[!] Error Testing HTTP Response Header: {e}")
    return vulnerable

def check_html_comment_xss(url, payloads, output_file):
    print("[+] Checking for XSS in HTML Comments...")
    vulnerable = False
    try:
        res = requests.get(url)
        soup = bs(res.content, "html.parser")
        comments = soup.find_all(string=lambda text: isinstance(text, bs.Comment))
        for comment in comments:
            for payload in payloads:
                if payload in comment:
                    print("\n[!] XSS Detected in HTML Comment!")
                    print(f"[*] Payload: {payload}")
                    print(f"[*] Vulnerable URL: {url}")
                    save_result(output_file, url, payload, {"comment": comment})
                    vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking HTML Comments: {e}")
    return vulnerable

def check_element_xss(url, payloads, output_file):
    print("[+] Checking For XSS in HTML Elements And Attributes...")
    vulnerable = False
    try:
        res = requests.get(url)
        soup = bs(res.content, "html.parser")
        for tag in soup.find_all():
            for attr in tag.attrs:
                if isinstance(tag[attr], str):
                    for payload in payloads:
                        if payload in tag[attr]:
                            print("\n[!] XSS Detected in HTML Elements And Attributes!")
                            print(f"[*] Element: {tag.name}")
                            print(f"[*] Attribute: {attr}")
                            print(f"[*] Payload: {payload}")
                            print(f"[*] Vulnerable URL: {url}")
                            save_result(output_file, url, payload, {"element": tag.name, "attribute": attr})
                            vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking HTML Elements And Attributes: {e}")
    return vulnerable

def check_body_xss(url, payloads, output_file):
    print("[+] Checking For XSS in HTML Body Content...")
    vulnerable = False
    try:
        res = requests.get(url)
        soup = bs(res.content, "html.parser")
        body_content = soup.body.get_text() if soup.body else ""
        for payload in payloads:
            if payload in body_content:
                print("\n[!] XSS detected in HTML body content!")
                print(f"[*] Payload: {payload}")
                print(f"[*] Vulnerable URL: {url}")
                save_result(output_file, url, payload, {"body_content": body_content})
                vulnerable = True
    except Exception as e:
        print(f"[!] Error Checking HTML Body Content: {e}")
    return vulnerable

def print_about():
    about_info = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  \033[1;31m███╗   ██╗\033[0m\033[1;32m██╗  ██╗\033[0m\033[1;33m ██████╗\033[0m     \033[1;36mAdvanced XSS Scanner With Crawl Option\033[0m     ║
║  \033[1;31m████╗  ██║\033[0m\033[1;32m╚██╗██╔╝\033[0m\033[1;33m██╔═══██╗\033[0m                                               ║
║  \033[1;31m██╔██╗ ██║\033[0m\033[1;32m ╚███╔╝\033[0m\033[1;33m ██║ 0 ██║\033[0m    \033[1;35mDeveloper:\033[0m \033[1;35mNANO\033[0m \033[1;34m&\033[0m \033[1;30mDr.FarFar\033[0m                ║
║  \033[1;31m██║╚██╗██║\033[0m\033[1;32m ██╔██╗\033[0m\033[1;33m ██║ 0 ██║\033[0m    \033[1;35mVersion:\033[0m \033[1;32m1.0.0\033[0m                             ║
║  \033[1;31m██║ ╚████║\033[0m\033[1;32m██╔╝ ██╗\033[0m\033[1;33m╚██████╔╝\033[0m    \033[1;35mEmail:\033[0m \033[1;36mNANO@NANO.COM\033[0m                       ║
║  \033[1;31m╚═╝  ╚═══╝\033[0m\033[1;32m╚═╝  ╚═╝\033[0m\033[1;33m ╚═════╝\033[0m     \033[1;35mEmail:\033[0m \033[1;36minFo@Dr-FarFar.CoM\033[0m                  ║
║                                                                            ║
║  \033[1;35mSocial Media:\033[0m                                                             ║
║  \033[1;33m•\033[0m \033[1;36mTwitter:\033[0m \033[1;32m@nano\033[0m \033[1;30m&\033[0m \033[1;32m@3XS0\033[0m                                                  ║
║  \033[1;33m•\033[0m \033[1;36mGitHub:\033[0m \033[1;32m/NANObyte0\033[0m \033[1;30m&\033[0m \033[1;32m/BlackHatLab-INC\033[0m                                   ║
║                                                                            ║
║  \033[1;35mContributors:\033[0m                                                             ║
║  \033[1;33m•\033[0m \033[1;32mDr.FarFar\033[0m                                                               ║
║  \033[1;33m•\033[0m \033[1;32m3XS0\033[0m                                                                    ║
║  \033[1;33m•\033[0m \033[1;32mNANO\033[0m                                                                    ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(about_info)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NXO - Advanced XSS Scanner With Crawl Option")
    parser.add_argument("-a", "--advanced", action="store_true", help="Perform advanced XSS scan including URL parameters and headers")
    parser.add_argument("-ab", "--about", action="store_true", help="Display developer information, version, social media accounts, email, and a list of contributors")
    parser.add_argument("-b", "--body", action="store_true", help="Perform XSS scan on body")
    parser.add_argument("-c", "--config", required=False, help="Load scanning configuration from a custom config file")
    parser.add_argument("-ck", "--cookie", action="store_true", help="Check for XSS in cookies")
    parser.add_argument("-cmn", "--comment", action="store_true", help="Scan HTML comments for potential XSS vulnerabilities")
    parser.add_argument("-cr", "--crawl", action="store_true", help="Only crawl the URL and get links")
    parser.add_argument("-d", "--detailed", action="store_true", help="Perform detailed XSS scan including DOM-based vulnerabilities")
    parser.add_argument("-e", "--element", action="store_true", help="Perform XSS scan on elements")
    parser.add_argument("-f", "--form", action="store_true", help="Perform XSS scan on forms")
    parser.add_argument("-hd", "--header", action="store_true", help="Check for XSS in HTTP response headers")
    parser.add_argument("-i", "--input", action="store_true", help="Perform XSS scan on input fields")
    parser.add_argument("-j", "--json", action="store_true", help="Check for XSS in JSON responses")
    parser.add_argument("-l", "--link", action="store_true", help="Perform XSS scan on links")
    parser.add_argument("-m", "--method", action="store_true", help="Perform XSS scan on methods")
    parser.add_argument("-o", "--output", default="results.txt", help="Output file to save results")
    parser.add_argument("-p", "--payloads", required=False, help="Payloads file path (required for scan)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet output")
    parser.add_argument("-r", "--recursive", action="store_true", help="Perform recursive XSS scan")
    parser.add_argument("-s", "--save", action="store_true", help="Save detailed scan results in multiple formats (JSON, XML, HTML)")
    parser.add_argument("-sc", "--scan", action="store_true", help="Perform basic XSS scan")
    parser.add_argument("-sp", "--script", action="store_true", help="Perform XSS scan on script")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Timeout for requests in seconds")
    parser.add_argument("-th", "--threads", type=int, default=10, help="Number of concurrent threads for scanning")
    parser.add_argument("-to", "--tor", action="store_true", help="Use Tor network for anonymous scanning")
    parser.add_argument("-u", "--url", required=False, help="Target URL to scan or crawl")
    parser.add_argument("-ua", "--user-agents", required=False, help="User agents file for scanning")
    parser.add_argument("-v", "--validate", action="store_true", help="Validate discovered vulnerabilities before reporting")
    parser.add_argument("-vb", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-vs", "--version", action="store_true", help="Show version information")
    parser.add_argument("-w", "--wordlist", required=False, help="Wordlist file for crawling and scanning")
    parser.add_argument("-x", "--xml", action="store_true", help="Check for XSS in XML responses")
    parser.add_argument("-y", "--proxy", required=False, help="Proxy server for scanning (format: http://host:port)")
    if len(sys.argv) == 1:
        print_banner()
        print_usage()
        sys.exit(1)
    args = parser.parse_args()
    if args.about:
        print_about()
        sys.exit(0)
    if not args.url:
        print("[!] Target URL (-u/--url) is Required For Scanning.")
        sys.exit(1)
    if args.crawl:
        crawl_links(args.url)
    else:
        if not args.payloads:
            print("[!] Payloads File is Required For Scanning.")
        else:
            payloads = load_payloads(args.payloads)
            scan_xss(args.url, payloads, args.output)
            if args.advanced:
                advanced_xss_scan(args.url, payloads, args.output)
                check_json_xss(args.url, payloads, args.output)
                check_cookie_xss(args.url, payloads, args.output)
                check_xml_xss(args.url, payloads, args.output)
                check_header_xss(args.url, payloads, args.output)
                check_html_comment_xss(args.url, payloads, args.output)
            if args.detailed:
                detailed_xss_scan(args.url, payloads, args.output)
            if args.element:
                check_element_xss(args.url, payloads, args.output)
            if args.body:
                check_body_xss(args.url, payloads, args.output)
            print(f"\n[+] Scan Complete. Results Saved To: {args.output}")

