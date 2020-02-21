
def query(region):
    header = {'User-Agent': 'Opera/8.0 (Windows NT 5.1; U; en)'}
    url = 'http://apis.map.qq.com/jsapi?'
    data = {
        'qt': 'poi',
        'wd': region,
        'pn': 0,
        'rn': 10,
        'rich_source': 'qipao',
        'rich': 'web',
        'nj': 0,
        'c': 1,
        'key': 'FBOBZ-VODWU-C7SVF-B2BDI-UK3JE-YBFUS',
        'output': 'jsonp',
        'pf': 'jsapi',
        'ref': 'jsapi',
        'cb': 'qq.maps._svcb3.search_service_0'}
    coordinate_url = url + parse.urlencode(data)
    r = requests.get(coordinate_url, headers=header)
    print(r.text)
    longitude = re.findall('"pointx": \s*(.+?),', r.text)[1]
    latitude = re.findall('"pointy": \s*(.+?),', r.text)[1]
    print([region, longitude, latitude])
    time.sleep(1)
    return ([region, longitude, latitude])
