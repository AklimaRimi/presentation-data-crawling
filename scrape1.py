import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import pandas as pd
import multiprocessing as mp


    
    

driver = webdriver.Chrome()
driver.maximize_window()
def get_links():
    
    driver.get(f'https://www.abstractsonline.com/pp8/#!/20272/presentations/@sessiontype=Poster%20Session/1')
    time.sleep(5)
    driver.refresh()
    time.sleep(5)
    for page in range(1,661):
        print(page)
        links = []
        ids =driver.find_elements(By.XPATH,"//h1[@class='name']")
        time.sleep(1)
        for id in ids:
            links.append(id.get_attribute('data-id'))
            
        df = pd.DataFrame(links)
        df.to_csv('ids.csv',mode='a',header=False,index=False)
        print(len(links))
        try:
            action = ActionChains(driver)
            button  = driver.find_element(By.XPATH,'//*[@id="paginator"]/div/ul/li[8]/span/i')
            action.click(button).perform()
            time.sleep(4)
        except:
            print('')
    driver.close()
    links = pd.read_csv('ids.csv')['IDs'].values.tolist()
    return links
    
        
def download(li):   
    for link in li:
        try:
            x = f'https://www.abstractsonline.com/pp8/#!/20272/presentation/{link}'
            driver.get(x)
            time.sleep(3)
            driver.refresh()
            time.sleep(10)
            
            name = driver.find_element(By.XPATH,'//*[@id="body"]/div/div[1]/div/div[3]/div[1]/h1').text
            date = driver.find_element(By.XPATH,'//*[@id="body"]/div/div[1]/div/table/tbody/tr/td[1]/span').text
            location = driver.find_element(By.XPATH,'//*[@id="body"]/div/div[1]/div/table/tbody/tr/td[2]/span').text
            presenter = driver.find_element(By.XPATH,'//*[@id="body"]/div/div[2]/div/dl/dd[1]').text

            disclosure = driver.find_elements(By.XPATH,'//*[@id="body"]/div/div[2]/div/dl/dd[2]/b')
            disclosures = []
            for dis in disclosure:
                disclosures.append(dis.text)
            descriptions = driver.find_element(By.XPATH,'//*[@id="body"]/div/div[2]/div/dl/dd[3]').text
            # print(name,date, location,presenter,disclosures,descriptions)
            lis = [[x,name,date, location,presenter,disclosures,descriptions]]
            df = pd.DataFrame(lis)
            df.to_csv('presentations.csv',header=False,mode='a',index=False)
        except:
            print(' ')
            
    driver.close()
    
    
if __name__ == '__main__':
    if os.path.exists('presentations.csv') == False:
        df = pd.DataFrame(columns=['Links','Name','Date','location','Presenter','Disclosures','Descriptions'])
        df.to_csv('presentations.csv',index = False)
    if os.path.exists('ids.csv') == False:
        df = pd.DataFrame(columns=['IDs'])
        df.to_csv('ids.csv',index = False)
        links = get_links()
    else:
        links = pd.read_csv('ids.csv')['IDs'].values.tolist()
        
    print(len(links))
    cpu  =  3
    li = []
    x = len(links) //cpu
    for i in range(cpu):
        s = i*x
        e = s+x

        li.append(links[s:e])


    pool = mp.Pool(cpu)
    pool.map(download,li)