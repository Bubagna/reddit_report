from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
import re
import string
from webdriver_manager.chrome import ChromeDriverManager

#here is in italian, soon will be changed(maybe)
"""Questo programma ancora incompleto restituisce all'esecutore il karma, il cake day e il tuo commento con il maggior numero di likes.
    Potrebbe non funzionare se il tuo commento con più like ha più di 1.0k likes, ma per il momento sto cercando di risolver il problema
    
    La documentazione completa sarà disponibile sul mio proilo github entro gennaio 2019, per il momento gli aggiornamenti fatti più 
    importanti saranno presenti qui.
    
    Il codice usa selenium webdriver come base completa, usando i suoi script e i suoi find elements per trovare i singoli commenti
    Nel corso del codice vengono usati numerosi loops, perchè devo iterare tra i numerosi elementi che sono dati dai commenti.
    
    Alcune righe di codice sono state hastaggate(?), perchè non sono più in uso, ma presto potrebbero diventarlo.
    Le righe direttamente copiate da stack overflow o da altri siti web sono segnalate e comprendono il link per arrivare alla pagina
    dove sono state reperite.
    
    Se il codice, nel momento in cui sta venendo guardato sembra obsoleto o altro, tenete a mente che questo è il mio primo codice e progetto quasi completo
    e sto cercando di farlo il più veloce e bello possibile.
    
    L'interfaccia grafica non è ancora presente,  ma spero che entro la fine del progetto riuscirò a farne una buona.
    
    Niente, ora il codice, questo è l'index.html(!)"""


#Here i get the username


#option variable inizialised
option = Options()

#options copied from stack overflow, but they semm to work good
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")


# Pass the argument 1 to allow and 2 to block notifications
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})


#here I put the principal function access, not a class cause I'm not food at classes
def access(userName):
    #latest version of chromedriver
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #set window dimension
    driver.set_window_size(3600, 3200)

    #selenium documentation
    executor_url = driver.command_executor._url

    #session id, to get to the current robotized session
    session_id = driver.session_id

    #link where to send the browser
    link = f"""https://www.reddit.com/u/{userName}"""

    #get to the link, trough the driver variable
    driver.get(link)

    #scroll down the webpage to get the access to the most number of comments
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #sleep time to wait the scrolling to as bottom as possible

    #here I get the karma trough the element id, copied directly from the browser
    karma1 = driver.find_element_by_id("profile--id-card--highlight-tooltip--karma")
    
    #I have to get only the text of the element, so .text is the best option
    karma = karma1.text

    #same as karma
    cake1 = driver.find_element_by_id("profile--id-card--highlight-tooltip--cakeday")
    cake = cake1.text


    #this is the page source, now is not useful anymore, but I keep that to be ready for problems, so I can see directly the page src
    html = driver.page_source

    #here it starts getting confused. Texters is the strange name I used for my variable, where I keep all the elements of a div box
    #where inside of it there are all the elements contained in a single comment,
    #likes, date, username, comment, likes and more
    texters = []

    #I used a general xpath, created manually
    lists = driver.find_elements_by_xpath("//div[contains(@class, 'Comment')]")

    #I loop trough the elements of lists and i get only the text of the element
    for i in lists:
        texters.append(i.text)


    #Here I split the texters elements using the \n caracheters, that separates the single text of the divs
    texters =str(texters).split(r"\n")
    #print(texters)

   
    #Here I get the single usernames element trough the xpath
    user1 = driver.find_elements_by_xpath("//div[contains(@class, '_2mHuuvyV9doV3zwbZPtIPG')]")
    user2 = []
    for i in user1:
        user2.append(i.text)
    #print(user2)

    #unuseful thing to clear the usernames, this will stay here to look good
    """
    for i in user2:
        if i != userName or "u/" +  userName:
            user2.remove(i)

    user3 = []
    for i in user2:
        if i == userName or "u/" +  userName:
            user3.append(i)
    """
    

    #Now I get the points
    points1 = driver.find_elements_by_xpath("//span[contains(@class, '_2ETuFsVzMBxiHia6HfJCTQ _3_GZIIN1xcMEC5AVuv4kfa')]")
    points2 = []
    for i in points1:
        points2.append(i.text)

    #every single point is separted from the other from a "·", so here I split it, from the start
    for i in points2:
        if i == "·":
            points2.remove(i)    

    #and here from the end, cause I dont know why, but the "·" form the and are not all removed
    for i in reversed(points2):
        if i == "·":
            points2.remove(i)

    for i in points2:
        if i == "Score":
            points2.remove(i)
    
    #the point element is not just only the number, but is included the "point" or the "points" text, so here from every element of the list poins2 
    #I split it and I get the element with the index of 0(first element)
    points2 = [i.split()[0] for i in points2]
    #print(points2)

    
    #stack overflow, faccio diventare le string all'interno di points2 int, ora che non sono più presenti elementi non convertibili
    points2 = list(map(int, points2))
      

   

    #Here I get the comments by xpath, specified
    comment1 = driver.find_elements_by_class_name("_a5_x7qimk18YbGSwE8Fy")
    comment2 = []
    for i in comment1:
        comment2.append(i.text)

    #here I create  kind of dicitonary, with the points and the comments alternate
    testList = [None]*(len(points2) + len(comment2))
    testList[::2] = points2
    testList[1::2] = comment2

    
    #src: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    #newList = [testList[i * 2:(i + 1) * 2] for i in range((len(testList) + 2 - 1) // 2)]

    #here I get the number of likes that the higher comment did
    higherPoints = []
    
    for i in testList:
        if isinstance(i, int):
            higherPoints.append(i)
    
    higherPoint = max(higherPoints)
    

    #higherPoint for Bubagna = 19
    #ok, here I didnt use the dictionary couse there was a kind of probem that the key and the value stopped at 7 and they donyt finish every comment
    #so I get the higherpoint inside the testList and I get the next element inside that list with the next index, the corrisponding comment
    higherComment = ""
    for i in range(len(testList)):
        if testList[i] == higherPoint:
            higherComment = testList[i + 1]
        else:
            pass

    higherPoint = max(higherPoints)

                    
    #here there are the objects to return, all beutiful inside the cmd terminal.
    generaInformations = "Your karma is actually {} and your cake day is {}".format(karma, cake)
    finalObj = "The most recent comment you made that has made the highest number of like is {} and it made {} upvotes.".format(higherComment, higherPoint)

    return generaInformations, finalObj

print(access("Bubagna"))
