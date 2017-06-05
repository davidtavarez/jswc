# JSWC
### Just a simple Web Crawler
```bash
usage: jswc.py [-h] -t TARGET [--tor-host TOR_HOST] [--tor-port TOR_PORT]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        The URL of the TARGET to scan.
  --tor-host TOR_HOST   Tor server.
  --tor-port TOR_PORT   Tor port server.
```
#### Installing JSWC
```bash
git clone git@github.com:davidtavarez/jswc.git
pip install -r requirements.txt
chmod +x jswc.py
./jswc.py
```
