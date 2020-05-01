with open("Safari Bookmarks.html", encoding='utf8') as f:
    L = f.read().splitlines()
    for i in range(len(l)):
        L[i] = L[i].strip()

def change_folder(self):
    # change the folder reference to the last folder in path
    self.folder = self.tree[self.path[-1]]


for l in L:
    if l[1:3] == "DT" and l[5] == "A":
        name = re.findall('(?<=>).*?(?=<)', l)[1]
        href = re.search('(?<=HREF=").*?(?=")', l).group()
        print(name)
        print(href)


from bs4 import BeautifulSoup
import time
        

f = open('Safari Bookmarks.html','r')
soup = BeautifulSoup(f.read())
f.close()

dt=[]
for d in soup.findAll('dt'):
  dt.append(d)

for i in range(len(dt)):
  if dt[i].contents[0].has_key('href') and dt[i].contents[0].has_key('add_date'):
    uri =  dt[i].contents[0]['href']
    title = dt[i].contents[0].contents[0]
    add_date = time.ctime(int(dt[i].contents[0]['add_date']))
    last_modified = time.ctime(int(dt[i].contents[0]['last_modified']))
