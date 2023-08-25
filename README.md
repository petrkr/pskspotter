# PSK Spotter

Utility to show MQTT data from PSK Repoter in table, filter what you hear and where you are heard.

Since it using MQTT it is very fast to show new data. And because it uses python, it will works on any platform, which supports python.


## Build and run in container
You can run this in container aswell

### Build container image
run `podman build -t pskspotter:latest .`

### Run
Since container already contains downloaded cty plist, you do not need specify or download extra. Just run it as `podman run -it --rm pskreporter:latest --call <YOUR CALL>`


## Install on local machine

Because modern linux does not allow to use system-wide pip, you need use virtual env. Fortunately any modern system already have python atleasy 3.6, so this should not be problem.

### Prepare virtual environment
 - python -m venv .venv
 - source .venv/bin/activate
 - pip install --upgrade pip
 - pip install -r requirements.txt


### Running
You need load that venv

- source .venv/bin/activate
- python --call <YOUR CALL>

Optionally you can download cty plist from https://www.country-files.com/cty/cty.plist and then select it by parameter `--cty-plist`
