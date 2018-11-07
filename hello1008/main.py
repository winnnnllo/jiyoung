from flask import Flask, render_template, request, url_for
from flask import jsonify
from sklearn.externals import joblib
import pandas as pd

#☆
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
#☆


app = Flask(__name__)
 

def trans(x):
    dic = {}
    dic['북']=360
    dic['북북동']=20
    dic['북동']=50
    dic['동북동']=70
    dic['동']=90
    dic['동남동']=110
    dic['남동']=140
    dic['남남동']=160
    dic['남']=180
    dic['남남서']=200
    dic['남서']=230
    dic['서남서']=250
    dic['서']=270
    dic['서북서']=290
    dic['북서']=320
    dic['북북서']=340
    return dic[x]  
    
    
def webscroll(cc):
   
    options = Options()
    options.add_argument('--kiosk')

    driver = webdriver.Chrome('C:/Users/hjo22/driver/chromedriver.exe', chrome_options=options)
    driver.get("http://www.weather.go.kr/mini/marine/marine_buoy.jsp?type=table&stn=0")

    xpath_b = """//*[@id="observation_select2"]"""
    bu_list_raw = driver.find_element_by_xpath(xpath_b)
    
    bu_list = bu_list_raw.find_elements_by_tag_name("option")
    
    bu_names = [option.text for option in bu_list]
   
    element = driver.find_element_by_id("observation_select2")
    
    for i in range(0, len(bu_names)):
        if bu_names[i] == cc:
                element.send_keys(bu_names[i])

    driver.find_element_by_class_name("btn").click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    tbody_soup = soup.find('tbody')
    tr_soup = tbody_soup.find('tr')
    
    [s.extract() for s in tr_soup('script')]
    
    hello = tr_soup.get_text()
    hello2 = re.split(('\n'), hello)

    test =hello2[1:10]
    test.append(hello2[12])
    test.append(hello2[13])

    count = 0
    for i in test:
        if (i == '\xa0')|(i==""):
            count +=1
        
        
    if count == 0:
        t1 = trans(test[1])
        t2 = trans(test[10])
        test[1] = t1
        test[10] = t2
        driver.close()
             
    else:
        for i in range(1, 11):
            if test[i] == '\xa0':
                test[i]=0
            elif test[i]== '':
                test[i]=0
        driver.close()
        
    return test
    
    
    
    
    
    
    
    
    
@app.route('/')
def exam_2():
    return render_template('index.html')

@app.route('/elements', )
def exam_3():
    return render_template('elements.html')

@app.route('/generic',)
def exam_4():
    return render_template('generic.html')






#landing 페이지랑 연관됨
@app.route('/check',)
def check():         
    return render_template('check.html')
    

#데이터 웹스크롤링 페이지
@app.route('/landing',methods=['POST'])
def exam_5():
    
    c = request.form['c2']
    list = webscroll(c)
    
    sea_data = [list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10]]
    sea_data2 = [[float(x) for x in sea_data]] 
    rdc = joblib.load('randomforest_calssifier_종설.pkl')
    pred = rdc.predict_proba(sea_data2)
    t  = pred[0][1]

    return render_template('landing.html',p = c , list = list, t=t)






@app.route('/deg',)
def exam_7():
    return render_template('deg.html')


@app.route('/landing_3',)
def exam_8():
    return render_template('landing_3.html')





@app.route('/landing_4',)
def exam_9():
    return render_template('landing_4.html')

@app.route('/action4', methods=['POST'])
def action4():
    
    c = request.form['c2']
    list = webscroll(c)
  
    sea_data = [list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10]]
    sea_data2 = [[float(x) for x in sea_data]]
    lda = joblib.load('lda_calssifier_동해.pkl')
    pred = lda.predict_proba(sea_data2)
    t  = pred[0][1]
    
    
    return render_template('action4.html', p = c , list = list, t=t)





@app.route('/landing_5',)
def exam_10():
    return render_template('landing_5.html')


@app.route('/action5', methods=['POST'])
def action5():
    
    c = request.form['c2']
    list = webscroll(c)
    
    sea_data = [list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10]]
    sea_data2 = [[float(x) for x in sea_data]] 
    rdc = joblib.load('randomforest_calssifier_서해.pkl')
    pred = rdc.predict_proba(sea_data2)
    t  = pred[0][1]
    
    
    return render_template('action5.html',  p = c , list = list, t=t)





@app.route('/landing_6',)
def exam_11():
    return render_template('landing_6.html')

@app.route('/action6', methods=['POST'])
def action6():
    
    c = request.form['c2']
    list = webscroll(c)
    
    sea_data = [list[1],list[2],list[3],list[4],list[5],list[6],list[7],list[8],list[9],list[10]]
    sea_data2 = [[float(x) for x in sea_data]] 
    rdc = joblib.load('randomforest_calssifier_남해.pkl')
    pred = rdc.predict_proba(sea_data2)
    t  = pred[0][1]
    
    
    return render_template('action6.html',  p = c , list = list, t=t)






#실제 데이터 처리하는 페이지 (데이터 입력)
@app.route('/landing_2',)
def exam_6():   
    return render_template('landing_2.html')


#form action
@app.route('/form_action', methods=['POST'] )
def action():
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    text4 = request.form['text4']
    text5 = request.form['text5']
    text6 = request.form['text6']
    text7 = request.form['text7']
    text8 = request.form['text8']
    text9 = request.form['text9']
    text10 = request.form['text10']
    
    list = [[text1,text2,text3,text4,text5,text6,text7,text8,text9,text10]] 
    
    rdc = joblib.load('randomforest_calssifier_종설.pkl')
    pred = rdc.predict_proba(list)
    p  = pred[0][1]

    return render_template('form_action.html', list = list, p=p)





# host = 0.0.0.0으로 설정함으로써 같은 ip를 공유하고있는 컴퓨터에서는 접속이 가능    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
