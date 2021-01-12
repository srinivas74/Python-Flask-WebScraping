from flask import Flask,render_template,request
import numpy
import pandas as pd
import re
from bs4 import BeautifulSoup
import csv
app = Flask(__name__)


@app.route('/')
def index():
   return render_template('search.html')
@app.route('/search',methods=['GET','POST'])
def index1():
    if request.method=="POST":
        x=request.form.get("search", False)
    else:
      pass
    soup = BeautifulSoup(open("C:\\Users\\850557\\Documents\\Flask\\sample\\templates\\43rd-congress.html"), features="lxml")

    fd=open('innovators.csv', 'w', newline='')
    f= csv.writer(fd)
    f.writerow(["Name", "Years", "Position", "Party", "State", "Congress", "Link"])
    pattern=x
    names = []
    years = []
    positions = []
    parties = []
    states = []
    congress = []

    links = []  
 
    trs = soup.find_all('tr') 
    for tr in trs:
        for link in tr.find_all('a'):
          links.append(link.get ('href'))
        tds = tr.find_all("td")

        try: 
            names.append(str(tds[0].get_text())) 
            years.append(str(tds[1].get_text()))
            positions.append(str(tds[2].get_text()))
            parties.append(str(tds[3].get_text()))
            states.append(str(tds[4].get_text()))
            congress.append(str(tds[5].get_text()))

        except:
            print("bad tr string: {}".format(tds))
            continue 
    for i in range(len(links)):
      try:
        match=re.search(pattern,names[i],re.IGNORECASE)
        match1=re.search(pattern,years[i],re.IGNORECASE)
        match2=re.search(pattern,positions[i],re.IGNORECASE)
        match3=re.search(pattern,parties[i],re.IGNORECASE)
        match4=re.search(pattern,states[i],re.IGNORECASE)
        match5=re.search(pattern,congress[i],re.IGNORECASE)
        match6=re.search(pattern,links[i],re.IGNORECASE)
        
        if(match or match1 or match2 or match3 or match4 or match5 or match6):
            f.writerow([names[i], years[i], positions[i], parties[i], states[i], congress[i], links[i]])
      except:
        pass
    fd.flush()
    fd.close()
    b="cnu"
    df = pd.read_csv('innovators.csv',encoding= 'unicode_escape')
    return render_template('search.html',Names=df['Name'],years=df['Years'],positions=df['Position'],parties=df['Party'],state=df['State'],congress=df['Congress'],link=df['Link'])



if __name__ == '__main__':
   app.run(port=5001,debug = True)
