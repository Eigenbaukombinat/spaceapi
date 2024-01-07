## Installation

```
git clone https://github.com/Eigenbaukombinat/spaceapi.git
cd spaceapi
python3 -m venv .
bin/pip install -r requirements.txt
```

## Running

To run via supervisor, create `/etc/supervisor/conf.d/spaceapi.conf` with this:

```
[program:spaceapi]
command = <home>/spaceapi/bin/python src/spaceapi.py
process_name = spaceapi
directory = <home>/spaceapi
priority = 10
user = <user>
autostart = true
startsecs = 10
startretries = 30
```
