**NXO - XSS Scanner 🚨**

Powered by NANO & DR.FARFAR

**Features**

- Scans for reflected XSS in form inputs
- Crawls web pages and lists all discovered links
- Supports custom payload files
- Saves results to a file
- Fast payload testing with threading
- Simple CLI interface

---

**Usage**

python3 NXO.py -u <TARGET_URL> -p <PAYLOADS_FILE> [-o OUTPUT_FILE] 📄 Description A lightweight XSS scanner built with Python to detect Cross-Site Scripting (XSS) vulnerabilities in forms. It also supports crawling websites and testing custom payloads provided via file.

💡 Example

python3 NXO.py -u [https://example.com](https://example.com/) -p payloads.txt -o results.txt This command scans [https://example.com](https://example.com/) for XSS vulnerabilities using payloads from payloads.txt and saves results in results.txt.

⚠️ Notes You need to provide a payloads file when scanning.

Use the -c option to only crawl and list links:

python3 NXO.py -u [https://example.com](https://example.com/) -c

📬 Contact If you have questions or suggestions, reach out via Discord: nano_302

https://github.com/NANObyte0

https://guns.lol/nano_0
