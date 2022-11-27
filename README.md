[![Python](https://img.shields.io/pypi/pyversions/shell2http.svg)](https://badge.fury.io/py/shell2http)
[![PyPI](https://badge.fury.io/py/shell2http.svg)](https://badge.fury.io/py/shell2http)

# shell2http
HTTP-server to execute shell commands. Designed for development, prototyping or remote control. Settings through two command line arguments, path and shell command. By default bind to :8080. with [shell2udp](https://github.com/GitHub30/shell2udp) it runs with minimal latency.

# Usage

```bash
shell2http [-h] [-form] [-add-exit] [-output] [-sse] [-p PORT] ["shell command" for /] /path "shell command" /path2 "shell command2" ...

positional arguments:
  command

optional arguments:
  -h, --help            show this help message and exit
  -form                 parse query into environment vars
  -add-exit             add /exit command
  -output               send back output
  -sse                  use Server Sent Events
  -p PORT, --port PORT
```

# Install

```bash
pip install shell2http
```

# Examples

## Windows

```powershell
shell2http 'shutdown -s -t 0'
```

```powershell
shell2http 'shutdown -s -t 0' /beep 'echo ^G'
```

```powershell
shell2http --port 3306 /beep 'powershell -command [Console]::Beep(440,2000)'
```

## Linux

```bash
shell2http 'notify-send Hello root'
```


```bash
shell2http -p3000 'notify-send Hello root' /path 'canberra-gtk-play -i desktop-login'
```

```bash
shell2http -p3000 /path 'canberra-gtk-play -i desktop-login'
```

```bash
shell2http -output /info 'uname -a'
```

```bash
shell2http -output -sse /ping 'ping -c4 8.8.8.8'
```

```bash
shell2http -add-exit pwd
```

```bash
shell2http -output -form /form 'echo $v_from, $v_to'
```

# Acknowledgements

https://github.com/msoap/shell2http

https://github.com/eshaan7/Flask-Shell2HTTP
