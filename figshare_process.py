# virtualenv websites

## debug/design
def iterprint(thing, iterator, template=False):
    '''iterprint(response.json(), iter(response.json()), template)'''
    for k in iterator:
        if isinstance(thing, dict):
            entry = thing[k]
            if isinstance(entry, list):
                try:
                    new_iter = iter(entry)
                    iterprint(entry, new_iter, template)
                except:
                    continue
            if k in template.values() and k is not 'name':
                print(k, ":",  entry)
            elif k in template.values():
                print( entry)

        elif isinstance(thing, list):
            entry = k
            try:
                new_iter = iter(entry)
                iterprint(entry, new_iter, template)
            except:
                continue
        elif isinstance(thing, str):
            continue
    return None

def process_entry(entry, k, template, outdict, mypub=False):
    if k in template.values():
        if mypub:
            if k == template['Authors']:
                authors = ','.join(e['full_name'] for e in entry)
                outdict[template['Authors']] = authors

            elif k == template['Tags']:
                tags = ','.join(e['name'] for e in entry)
                outdict[template['Tags']] = tags
            else:
                outdict[k] = entry

        elif not mypub:
            if k == template['Authors']:
                authors = ','.join(e['author_name'] for e in entry)
                outdict[template['Authors']] = authors

            else:
                entry = entry.replace('http://dx.doi.org/', '') ## strip DOI prefix from everything
                outdict[k] = entry

    return outdict

def iterstore(thing, iterator, outdict, template=False, mypub=False):
    '''iterstore(response.json(), iter(response.json()), template)'''
    for k in iterator:
        if isinstance(thing, dict):
            entry = thing[k]
            if isinstance(entry, list):
                try:
                    new_iter = iter(entry)
                    iterstore(entry, new_iter, outdict, template)
                except:
                    continue
            outdict = process_entry(entry, k, template, outdict, mypub)
        elif isinstance(thing, list):
            entry = k
            try:
                new_iter = iter(entry)
                iterstore(entry, new_iter, outdict, template)
            except:
                continue
        elif isinstance(thing, str):
            continue
    return outdict
