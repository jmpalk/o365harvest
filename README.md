# o365harvest
A tool for enumerating the email accounts of Office365 users. This is an update of [o365creeper](https://github.com/LMGsec/o365creeper) using [Python 3](https://python.org) and adding [fireprox](https://github.com/ustayready/fireprox) compatibility. As noted in the description for o365creeper, repeated attempts to validate email addresses coming from a single host may draw Microsoft's attention, at which point they may start injecting false positives into the responses. Using fireprox to direct requests through an AWS API Gateway and rotate IP addresses, can avoid this.



## Usage
	jmpalk@kali-e:~/o365harvest$ ./o365harvest.py -h
	usage: o365harvest.py [-h] [-d DOMAIN] [-l USER_LIST] [-u URL] [-w WAIT] [-v] [-vv] [-D] [-o OUTPUT_FILE]

	Enumerate users against Office365

	optional arguments:
  	-h, --help            show this help message and exit
  	-v, --verbose
  	-vv, --more-verbose
  	-D, --debug
  	-o OUTPUT_FILE, --output OUTPUT_FILE
    	                    Output file for results (txt). Default is spray_results.txt

	Attack Target:
  	-d DOMAIN             Target domain - required
  	-l USER_LIST          File with list of target usernames (without domain)
  	-u URL, --url URL     Target URL if using something like fireprox; otherwise will directly call the O365 login endpoint
  	-w WAIT, --wait WAIT  Number of seconds to sleep between individual user attempts

