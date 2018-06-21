# IPS Patcher

IPS Patcher is a small script for applying valid IPS patches to binary files. 

### Usage

Using this tool is very simple:


  `patcher.py [-vh] <patch> <file> <output>`


Optional arguments include -v and -h for verbosity and help respectively.

### Information

- The way this program is coded, the original binary file is preserved and an entirely new patched file is created. In the future, there will be an option to disable this though.
- Unfortunately for the time being, this tool doesn't create IPS patches. This will likely be added in the future though.
- This tool doesn't support the UPS format, only IPS.
