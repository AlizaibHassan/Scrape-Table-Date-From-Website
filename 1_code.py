import requests
from bs4 import BeautifulSoup
import csv
import os

paths = r"C:\\Users\\AZ\\Desktop\\zablez\\"
os.chdir(paths)

f = open('1_list.txt')
line = f.readline()
cnt=0
while line:

    line=line.replace("\n","")
    url= line
    
    response = requests.get(url)
    html_page = response.text

    soup = BeautifulSoup(html_page, 'html.parser')
    #find <table>
    tables = soup.find_all("table")
    if tables != None:
        print(f"Total {len(tables)} Table(s)Found on page {url}")
        
        title = soup.find("title").text
        print(title)
        os.makedirs(str(cnt))
        cnt2=0    
        for index, table in enumerate(tables):
            cnt2+=1
            print(f"\n-----------------------Table{index+1}-----------------------------------------\n")
            
            #find <tr>
            table_rows = table.find_all("tr")
            
            #open csv file in write mode
            loc = paths+''+str(cnt)+"\\"
            
            if cnt2==1:
                file1 = open(f"{loc}{title}{index+1}.txt","w",encoding="utf-8")
                data=url+'\n'+title
                file1.write(data)
                file1.close()    
            cnt2+=1
            with open(f"{loc}{title}{index+1}.csv", "w", newline="",encoding="utf-8") as file:
            
                #initialize csv writer object
                writer = csv.writer(file)

                for row in table_rows:
                    row_data= []

                    #<th> data
                    if row.find_all("th"):
                        table_headings = row.find_all("th")
                        for th in table_headings:
                            row_data.append(th.text.strip())
                    #<td> data
                    else:
                        table_data = row.find_all("td")
                        for td in table_data:
                            row_data.append(td.text.strip())
                    #write data in csv file
                    writer.writerow(row_data)
                    print(",".join(row_data))
            print("--------------------------------------------------------\n")
        cnt+=1
        line = f.readline()