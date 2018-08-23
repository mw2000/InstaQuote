from PIL import Image, ImageDraw, ImageFont
from InstagramAPI import InstagramAPI
import requests
import threading


def createImg(data):
    
    #Image size
    x1 = 612
    y1 = 612
    
    #My quote
    sentence = '"' + data['quote'] + '"' + ' -' + data['author']    
    
    #Font chosen - Garamond-Roman
    fnt = ImageFont.truetype('Garamond-Roman.ttf', 48)
    img = Image.new('RGB', (x1, y1), color = (255, 255, 255))
    d = ImageDraw.Draw(img)

    #find the average size of the letter
    sum = 0
    for letter in sentence:
        sum += d.textsize(letter, font=fnt)[0]
    average_length_of_letter = sum/len(sentence)

    #find the number of letters to be put on each line
    number_of_letters_for_each_line = (x1/1.618)/average_length_of_letter
    incrementer = 0
    fresh_sentence = ''

    #add some line breaks
    for letter in sentence:
        if(letter == '-'):
            fresh_sentence += '\n\n' + letter
        elif(incrementer < number_of_letters_for_each_line):
            fresh_sentence += letter
        else:
            if(letter == ' '):
                fresh_sentence += '\n'
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer+=1
    print (fresh_sentence)

    #render the text in the center of the box
    dim = d.textsize(fresh_sentence, font=fnt)
    x2 = dim[0]
    y2 = dim[1]
    qx = (x1/2 - x2/2)
    qy = (y1/2-y2/2)
    d.text((qx,qy), fresh_sentence ,align="center",  font=fnt, fill=(0,0,0))
    
    img.save('quote.jpg')


def postQuote(data):

    #Path and caption of image given
    photo_path = 'quote.jpg'
    caption = '"' + data['quote'] + '"' + ' -' + data['author'] + ' #quote #quotes #qotd #quoteoftheday'
    tags = data['tags'] 

    #Quote tags added as hashtags to caption
    for i in range(len(tags)):
        caption+=' #' + tags[i]
    InstagramApi.uploadPhoto(photo_path, caption=caption)


def getQuote():

    #Requesting qotd from quotes.rest api
    r = requests.get(url = "https://quotes.rest/qod.json")
    data = r.json()
    return data['contents']['quotes'][0]

def recurrer():

    #Enables python script to run automatically every 24 hrs
    threading.Timer(86400.0, recurrer).start()
    data = getQuote()
    createImg(data)
    postQuote(data)


InstagramApi = InstagramAPI("Your username", "Your password")
InstagramApi.login()  # login
recurrer()