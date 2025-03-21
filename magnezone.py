#!/usr/local/env python3

import sys, os
import json
import requests
import cherrypy

# load the config file
config = None
if os.path.exists("config.json"):
	with open("config.json", "r") as f:
		config = json.loads(f.read())
if not config:
	print("No config file found, see git repo for how to setup.")
	sys.exit(1)

purgeEndpoint = config.get("purgeEndpoint", "")
apiKey = config.get("apiKey", "")

primaryRepo = config.get("primaryRepo", "")
secondaryRepo = config.get("secondaryRepo", "")
mergedRepo = config.get("mergedRepo", "")

if not primaryRepo or not secondaryRepo or not mergedRepo:
	print("Some repo URLs are missing from the config file.")
	sys.exit(1)

def getRepo():
	# just directly return the contents of repo.json
	if not os.path.exists("repo.json"):
		refresh()
	with open("repo.json", "r") as f:
		return f.read()

def refresh():
	print("Refreshing repos...")
	# if one of our repo's doesn't exist, re-download it
	repoNames = ["primary", "secondary"]
	for idx, repo in enumerate([primaryRepo, secondaryRepo]):
		if not os.path.exists(f"{repoNames[idx]}.json"):
			print(f"Repo {repoNames[idx]} doesn't exist, re-downloading...")
			with open(f"{repoNames[idx]}.json", "w") as f:
				f.write(requests.get(repo + "/repo.json").text)
	# load up the package data from the first one
	data = {}
	with open("primary.json", "r") as f:
		data = json.loads(f.read())
	packageKeys = set()
	if "packages" in data:
		for package in data["packages"]:
			if "name" in package: # this field should be mandatory
				packageKeys.add(package["name"])
	else:
		print("No packages in primary.json")
		data["packages"] = []
	# now for the data in the second repo, do the same but skip any duplicates
	duplicates = set()
	with open("secondary.json", "r") as f:
		data2 = json.loads(f.read())
		if "packages" in data2:
			for package in data2["packages"]:
				if "name" in package:
					if package["name"] in packageKeys:
						duplicates.add(package["name"])
					else:
						data["packages"].append(package)
					
		else:
			print("No packages in secondary.json")
	# save the updated data
	with open("repo.json", "w") as f:
		f.write(json.dumps(data, indent=4))
	print("BZZZZT! Refresh complete, merged repo.json is ready")
	if len(duplicates) > 0:
		print(f"Excluded these duplicate packages from secondary: {duplicates}")
	
	# TODO: Clear cache on CDN

def clearURL(url):
	if not purgeEndpoint or not apiKey:
		print("No purgeEndpoint or apiKey found in config, skipping CDN cache clear.")
		return
	print(f"Clearing CDN cache for: {url}")
	res = requests.post(purgeEndpoint + f"?url={url}", headers={"AccessKey": apiKey})
	if res.status_code != 200:
		print(f"Failed to clear cache for {url}, status code: {res.status_code}")

def clearCDN(repo, packages):
	# purging main repo.json
	clearURL(repo + "/repo.json")
	# if any packages were specified, clear those too
	if packages:
		for package in packages.split(","):
			# clear packages and zips
			clearURL(repo + f"/zips/{package}.zip")
			clearURL(repo + f"/packages/{package}/*")

# start a web server to access /refresh
class Magnezone:
	@cherrypy.expose
	def refresh(self, **params):
		# validate auth header matches api key
		if cherrypy.request.headers.get("AccessKey", "") != apiKey:
			cherrypy.response.status = 401
			return "UNAUTHORIZED".encode("utf-8")

		# the command can specify if it's primary, secondary, or both
		target = params.get("repo", "both")
		packages = params.get("packages", "")
		repoNames = ["primary", "secondary"]
		for idx, repo in enumerate([primaryRepo, secondaryRepo]):
			path = repoNames[idx]
			if target == path or target == "both":
				# delete the local repo file
				if os.path.exists(f"{path}.json"):
					os.remove(f"{path}.json")
				clearCDN(repo, packages)

		# do the main refresh
		refresh()

		# and finally, clear our merged repo of the same files
		clearCDN(mergedRepo, packages)

		return "BZZZZT! Refresh complete!".encode('utf-8')
	
	@cherrypy.expose
	def repo_json(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return getRepo().encode('utf-8')

	@cherrypy.expose
	def index(self):
		return "BZZZZT! MAGNEZONE"

if len(sys.argv) > 1 and sys.argv[1] == "serve":
	cherrypy.quickstart(Magnezone())
else:
	print("Magnezone: Repo Merger v0.1")
	refresh()