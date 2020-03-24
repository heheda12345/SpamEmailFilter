import json

f = open("../dataset/label/index")
items = []
cnt = 0
for st in f.readlines():
    harm, path = st.strip().split(" ")
    path = '../dataset' + path[2:]
    print(len(items), harm, path)
    ff = open(path)
    try:
        article=ff.read()
    except:
        cnt += 1
        continue
    paragraphs = article.split("\n\n")
    items.append({
        'path': path,
        'spam': harm == 'spam',
        'meta': paragraphs[0],
        'content': "\n\n".join(paragraphs[1:])
    })
print("LOAD END, valid = {}, invalid = {}".format(len(items), cnt))
with open('../log/raw.dump', 'w') as f:
    json.dump(items, f)