SELinux Information Viewer (Ver.0.1.1)
===

This tool is for survey about SELinux.
SELinux Information Extract can extract SELinux information from a target machine.
SELinux Information Viewer can make a view from the data.


# Description
This tool is for survey effectively about SELinux, without complex commands.

This tool contains two parts; 1) Extracting tool for SELinux information; 2) Viewer for the extracted data on web browsers. 

Extracting tool is for such customer machines, which can not be take possession. You can survey on your own machine with extracted data. 

Viewer is the main tool. You can survey more easy about SELinux than CUI. 


# FEATURE
## File Contexts
You can search about file contexts related with processes. In addition, you can get file lists which be matched with patterns of file contexts.

Specify a process domain, which is a source domain on policy rules. Then, the system searches file contests related with the policy rule's target types.

If a file context's pattern is hyperlink, it indicates that there are file paths which are matched with the pattern. Click the pattern then the paths are listed up.

## Files
You can search about files and get file contexts which match the file. In addition, you can know permissions of domains to the file. 

## Others
You can know:
* Processes
* Connections
* Booleans
* Policy Rules
* Machine properties

# Requirements
## SELinux Information Extract
- policycoreutils-python
- python2

## SELinux Information Viewer
- python2
- Development Tools
- python-devel


# Usage
## Extracting SELinux Information
Run SELinux Information Extract on a target machine.
The result data is outputted into "result" directory.
```
sudo python selinux-info-extract.py
```

You can put options in config.ini.
* prune : Specify ignored direcotries for search.
* root-path: Specify a root directory for search. (DEFAULT: /)
* output-dif: Specify a output directory for result files. (DEFALT: ./result)

For instance, if you want to extract under /opt directory only, exclude /opt/tmp directory and output the result in /tmp directory, you can put:
```
[settings]
prune = /opt/tmp
root-path =  /opt
output-dir = /tmp/result
```

NOTICE: This program might have long time for some environments.

## Booting Viewer
1) Login with a normal user.
1) Deploy SELinux Information Viewer.
1) Run below command to download thirdparty tools.
    * ./install.sh
    * If you need to go beyond proxies, you should create ~/.curlrc file and write below information in the file.
        * proxy-user = "&lt;username&gt;:&lt;passwd&gt;"
        * proxy = "&lt;proxy-url&gt;"
1) Deploy "result" directory, which is outputted by SELinux Policy Extract, in SELinux Information Viewer home directory.
1) Run below command then a server is starting.
    * ./sh/start.sh
1) Access to http://&lt;ip-adress&gt;:8080 with your blowser.
1) Stop by Ctrl+c.

## Booting as Daemon
* start: Run ./sh/start_daemon.sh
* stop: Run ./sh/stop_daemon.sh

## Restructuring a database
1) Stop the server.
1) Run ./sh/destroy_db.sh
1) Start the server.

# Contributing
We are grateful for contributing bug reports, bugfixes and improvements.
## Bug Report
Please open a new issue.

## Bugfixes and Improvements
Please open a new pull request.


# License
Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.

Licensed under the MIT License.
You may obtain a copy of the License at

* https://opensource.org/licenses/MIT

This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OF ANY KIND.
