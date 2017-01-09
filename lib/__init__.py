import sys
base_dir = sys.path[0][0:-4]
for dir in ('lib', 'case'):
    try:
        sys.path.index(base_dir + '/' + dir)
    except Exception, e:
        sys.path.append(base_dir + '/' + dir)