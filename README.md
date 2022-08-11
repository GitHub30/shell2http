# shell2http
HTTP-server to execute shell commands. Designed for development, prototyping or remote control. Settings through two command line arguments, path and shell command. By default bind to :8080.

# Usage

```bash
shell2http [options] ["shell command" for /] /path "shell command" /path2 "shell command2" ...
options:
    -p, --port NNNN : port for http server ( default 8080 )
```

# Install

```bash
pip install shell2http
```

# Examples

```bash
shell2http 'notify-send HelloRoot'
```


```bash
shell2http -p3000 'notify-send HelloRoot' /path 'canberra-gtk-play -i desktop-login'
```

```bash
shell2http -p3000 /path 'canberra-gtk-play -i desktop-login'
```
