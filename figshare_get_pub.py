# virtualenv websites
# pip install requests_oauthlib
# pip install PyYAML

import requests
from requests_oauthlib import OAuth1
import json, yaml # for reading conversion, reading template
from figshare_process import iterstore ##
from os import environ as e ## for my private credentials

def slugify_title(title, numwords=5):
    ''' given a title return a slug appropriate for titling md file'''
    for commonword in ['of', 'the', 'in', 'to', 'and', 'for', 'a', 'an', 'on', '-']:
        title = title.replace(' ' + commonword + ' ', ' ')
        title = title.replace(' ' + commonword.title() + ' ', ' ')

    title_list = title.split()
    return '-'.join(title_list[i] for i in range(numwords))

def get_results(query_string, client_key,
                client_secret, token_key, token_secret):
    '''helper function to get results given keys and tokens and retrieve results in json'''

    oauth = OAuth1(client_key=client_key, client_secret=client_secret,
                   resource_owner_key=token_key, resource_owner_secret=token_secret,
                   signature_type = 'auth_header')

    client = requests.session()

    ## below requires private key
    response = client.get(query_string, auth=oauth)

    return(json.loads(response.content.decode("utf-8"))) # response.json() does same thing ...

def write_pubs(results, template, mypub):
    '''helper to write figshare articles to md'''

    for record in results['items']:
        file_slug = slugify_title(record['title'])
        file_name = 'content/results/' + file_slug + '-' + str(record['defined_type']) + '.md' ## add article_id to make unique if dupe title and dupe media
        print(file_name)

        outdict = {}
        outdict = iterstore(record, iter(record), outdict, template, mypub=mypub)
        if not mypub:
            template['Tags'] = 'tags'
            outdict['tags'] = file_slug.replace('-', ',')

        with open(file_name, 'w') as out:
            out.write("Template: result" + "\n")  ## hardcoded template
            for k in sorted(template):
                if k == 'Body':
                    continue
                out.write(k + ": " + outdict[template[k]] + "\n") # print(k, ":", entry) print( entry)
            out.write("\n" + outdict[template['Body']] + "\n") # print(k, ":", entry) print( entry)
    return


## Retrieve private credentials (from environment) and get data
try:
    client_key = e.get('FIGSHARE_CLIENT_KEY')
    client_secret = e.get('FIGSHARE_CLIENT_SECRET')
    token_key = e.get('FIGSHARE_TOKEN_KEY')
    token_secret = e.get('FIGSHARE_TOKEN_SECRET')
except:
    ValueError("No key")

myresults = get_results("http://api.figshare.com/v1/my_data/articles",
                        client_key, client_secret, token_key, token_secret)

## Hardcode public api client and token credentials
client_key = '123456'
client_secret = '65xyAzi1'
token_key = 'n4oTQ22l4FxsuQlYZlhCFwYrrSgrlPn1lhIx32uzwzAwn4oTQ22l4FxsuQlYZlhC1F'
token_secret = '0MNOqkQncNHuKTi6fQ8MuA'

pubresults = get_results("http://api.figshare.com/v1/articles/search?search_for=Ashander&has_author=Jaime",
                         client_key, client_secret, token_key, token_secret)

## load templates
template_files = ['_convert/figshare.yaml', '_convert/figshare_mypub.yaml']

##write mypubs according to template
# order --mypubs after public -- matters as we overwite more datarich mypubs with public results otherwise
templates = [yaml.load(open(fname, 'r')) for fname in template_files]
results= [pubresults, myresults]
mypubs=[False, True]

for i in range(2):
    write_pubs(results=results[i], template=templates[i], mypub=mypubs[i])
