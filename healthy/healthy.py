import requests
import datetime
import concurrent.futures
import json

MAX_WORKERS=4

res={}

def handlePackage(package):
    now=datetime.datetime.now()
    response = requests.get(f"https://registry.npmjs.org/{package}")
    if response.status_code != 200:
        print(response.text, response.status_code)
        exit(1)
    responseJson=response.json()
    name=responseJson['name']
    lastVersion=responseJson['dist-tags']['latest']
    lastVersionTime=responseJson['time'][lastVersion]
    packageAge=now-datetime.datetime.strptime(lastVersionTime,"%Y-%m-%dT%H:%M:%S.%fZ")
    numOfMaintainers=len(responseJson['maintainers'])
    repo=responseJson['versions'][lastVersion]['repository']['url']
    repoOwner=repo.split('/')[-2]
    repoName=repo.split('/')[-1].replace('.git', "")
    gitResponse = requests.get(f"https://api.github.com/repos/{repoOwner}/{repoName}/branches/master")
    if gitResponse.status_code != 200:
        print(gitResponse.text, gitResponse.status_code)
        exit(1)
    gitLastCommitAge=now-datetime.datetime.strptime(gitResponse.json()['commit']['commit']['committer']['date'],"%Y-%m-%dT%H:%M:%SZ")

    failed=False
    res.update({name: {"Last Version is maximum 30 days old": packageAge <= datetime.timedelta(days = 30)}})
    res[name].update({"Number of maintainers is at least 2": numOfMaintainers >= 2 })
    res[name].update({"Commit in the last 14 days": gitLastCommitAge < datetime.timedelta(days = 14) })

packages=["json", "express", "async", "lodash", "cloudinary", "axios", "karma"]


with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(handlePackage, repo) for repo in packages]
    concurrent.futures.wait(futures)

print(json.dumps(res, indent=4))