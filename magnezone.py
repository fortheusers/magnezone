#!/usr/local/env python3

import sys, os
import json
import requests
import cherrypy

REPO1 = "https://switch2.cdn.fortheusers.org/repo.json" # "2nd" repo, primary
REPO2 = "https://switch1.cdn.fortheusers.org/repo.json" # "1st" repo, the fallback

def getRepo():
	# just directly return the contents of repo.json
	if not os.path.exists("repo.json"):
		refresh()
	with open("repo.json", "r") as f:
		return f.read()

def refresh():
	print("Refreshing repos...")
	# if one of our repo's doesn't exist, re-download it
	for idx, repo in enumerate([REPO1, REPO2]):
		if not os.path.exists(f"repo{idx + 1}.json"):
			print(f"Repo {idx + 1} doesn't exist, re-downloading...")
			with open(f"repo{idx + 1}.json", "w") as f:
				f.write(requests.get(repo).text)
	# load up the package data from the first one
	data = {}
	with open("repo1.json", "r") as f:
		data = json.loads(f.read())
	packageKeys = set()
	if "packages" in data:
		for package in data["packages"]:
			if "name" in package: # this field should be mandatory
				packageKeys.add(package["name"])
	else:
		print("No packages in repo1.json")
		data["packages"] = []
	# now for the data in the second repo, do the same but skip any duplicates
	duplicates = set()
	with open("repo2.json", "r") as f:
		data2 = json.loads(f.read())
		if "packages" in data2:
			for package in data2["packages"]:
				if "name" in package:
					if package["name"] in packageKeys:
						duplicates.add(package["name"])
					else:
						data["packages"].append(package)
					
		else:
			print("No packages in repo2.json")
	# save the updated data
	with open("repo.json", "w") as f:
		f.write(json.dumps(data, indent=4))
	print("BZZZZT! Refresh complete, merged repo.json is ready")
	if len(duplicates) > 0:
		print(f"Excluded these duplicate packages from repo2: {duplicates}")
	
	# TODO: Clear cache on CDN

# start a web server to access /refresh
class Magnezone:
	@cherrypy.expose
	def refresh(self, **params):
		# the command can specify if it's repo1, repo2, or both
		target = params.get("repo", "both")
		for idx in range(2):
			path = f"repo{idx + 1}"
			if target == path or target == "both":
				# delete the repo file
				if os.path.exists(f"{path}.json"):
					os.remove(f"{path}.json")
		# do the main refresh
		refresh()
	
	@cherrypy.expose
	def repo_json(self):
		return getRepo()

	@cherrypy.expose
	def index(self):
		return "BZZZZT! MAGNEZONE"

if len(sys.argv) > 1 and sys.argv[1] == "serve":
	cherrypy.quickstart(Magnezone())
else:
	print("Magnezone: Repo Merger v0.1")
	# TODO: add commands to clear repo1/repo2/both
	refresh()