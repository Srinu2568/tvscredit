import database as db
l = db.fetch_all_users()
a = [x for x in l if 'car' in x['type_data'] and not x['isEval']]
# print(a[0]['form_data'][1])
# print(a[0]['key'])
k = [{l['name']:(l['form_data'], l['images'])} for l in a]
j = [list(x.keys())[0] for x in k]
print(j)