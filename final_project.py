import pygame
# pygame setup
import json
import random as rand
import time
#key = "JQ41Br3htHozufmTzpS5kXIvWUJiW8Rpih821lTH"

#url = "https://countryapi.io/api/all"

#payload={}
#header = {
    #'Authorization' : f'Bearer {key}',
#}

#print(response.text)
#f = open("apiresponse.txt", "a")
#f.write(response.text)
#f.close()
countrynames = []
countrydata = {}
with  open("apiresponse.txt") as f:
    data = json.load(f)

for item in data:
    name = data[item]['name']
    countrynames.append(name)
    countrydata[name] = {'region': data[item]['region'], 'subregion': data[item]['subregion'], 
'population': data[item]['population'], 'area' : data[item]['area'], 'borders':data[item]['borders'],
'altnames' : [data[item]['alpha2Code'], data[item]['alpha3Code'], data[item]['cioc']]}


myscountry = rand.choice(countrynames)
mysdata = countrydata[myscountry]


def guessing(guessname):
    guessname = guessname.title().strip()
    if guessname not in countrynames:
        print('not in country list')
        return False
    guessdata = countrydata[guessname]
    retdict = {}
    if guessdata['region'] == mysdata['region']:
        retdict['region'] = guessdata['region']
        if guessdata['subregion'] == mysdata['subregion']:
            retdict['subregion'] = guessdata['subregion']
        else:
            retdict['subregion'] = False
    else:
        retdict['region'] = False
        retdict['subregion'] = False
    if guessdata['population'] == mysdata['population']:
        retdict['population'] = (0,0)
    elif guessdata['population'] != mysdata['population']:
        retdict['population'] = (guessdata['population'], mysdata['population'] - guessdata['population'])
    if guessdata['area'] == mysdata['area']:
        retdict['area'] = (0,0)
    elif guessdata['area'] != mysdata['area']:
        retdict['area'] = (guessdata['area'], mysdata['area'] - guessdata['area'])
    retdict['borders'] = False
    for item in guessdata['borders']:
        if item in mysdata['altnames']:
            retdict['borders'] = True
        
    return retdict

#area/region, population
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True 
screenWidth, screenHeight = pygame.display.get_window_size()
dt = 0 
base_font = pygame.font.Font(None, 80)
ret_font = pygame.font.Font(None, 30)
guess_font = pygame.font.Font(None, 50)
subtext_font = pygame.font.Font(None, 40)
user_text = '' 
input_rect = pygame.Rect(((screenWidth/2-50), 75) , (100, 75))
color_active = 'lightskyblue'
color_passive = 'white'
color = color_passive
active = False
winfont = pygame.font.Font(None, 200)
wintext = winfont.render('You Win!', True, 'white')
winrect = wintext.get_rect(center = (screenWidth/2, screenHeight/2))
game_text2 = subtext_font.render('Press enter to guess!', True, 'white')
game_text = base_font.render('Guess the country!', True, 'white' )
extext= subtext_font.render('your closest guesses:', True, 'white')
textrect1 = game_text.get_rect( center= ((screenWidth/2-10),25))
textrect2 = game_text2.get_rect(center=((screenWidth/2-10),200))
textrect3 = extext.get_rect(center= ((screenWidth/2 - 10), 468))
flag = False
countrynames = [name.title() for name in countrynames]

responserect = pygame.Rect((screenWidth/2-250), 250, 500 , 200)
rattributerect1 = pygame.Rect((screenWidth/2 - 240),255, 225, 90)
#355 y value for next
rattributerect2 = pygame.Rect((screenWidth/2 + 15), 255 , 225, 90)
rattributerect3 = pygame.Rect((screenWidth/2 -240), 355, 225, 90)
rattributerect4 = pygame.Rect((screenWidth/2 + 15), 355 , 225, 90)
finalrect = pygame.Rect((screenWidth/2 - 250), 490, 500, 200)
fattributerect1 = pygame.Rect((screenWidth/2 - 240), 495, 225, 90)
fattributerect2 = pygame.Rect((screenWidth/2 + 15), 495, 225, 90)
fattributerect3 = pygame.Rect((screenWidth/2 - 240), 595, 225, 90)
fattributerect4 = pygame.Rect((screenWidth/2 + 15), 595, 225, 90)
utext = ''
finaldict = {}
win = False
while running:
    gss = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if input_rect.collidepoint(event.pos): 
                active = True
            else: 
                active = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_BACKSPACE: 
                user_text = user_text[:-1]  
            elif event.key == pygame.K_RETURN:
                active = False
                gss = user_text
                user_text = ''
            else: 
                user_text += event.unicode
    screen.fill(color = 'blue4')

    if active: 
        color = color_active 
    else: 
        color = color_passive 
    
    pygame.draw.rect(screen, 'gray16', responserect)
    pygame.draw.rect(screen, 'gray10', rattributerect1)
    pygame.draw.rect(screen, 'gray16', finalrect)
    pygame.draw.rect(screen, 'gray10', rattributerect2)
    pygame.draw.rect(screen, 'gray10', rattributerect3)
    pygame.draw.rect(screen, 'gray10', rattributerect4)
    pygame.draw.rect(screen, 'gray10', fattributerect1)
    pygame.draw.rect(screen, 'gray10', fattributerect2)
    pygame.draw.rect(screen, 'gray10', fattributerect3)
    pygame.draw.rect(screen, 'gray10', fattributerect4)
    pygame.draw.rect(screen, color, input_rect)
    if gss:
        flag = True
        rdict = guessing(gss)
        if gss.title().strip() == myscountry:
            screen.fill('green')       
            screen.blit(wintext, winrect)
            win = True
        if rdict:
            if rdict['region']:
                rattributetext1 = ret_font.render(f"Region: {rdict['region']}", True, 'yellow')
                if rdict['subregion']:
                    rattributetext1 = ret_font.render(f"Region: {rdict['subregion']}", True, 'green')
            else:
                rattributetext1 = ret_font.render('Wrong Region!', True, 'red')
            rtextrect1 = rattributetext1.get_rect( center = rattributerect1.center)
            popdiff = rdict['population'][1]
            if popdiff > 0:
                rattributetext2 = ret_font.render('Population: Higher', True, 'yellow')
                if popdiff > 5000000:
                    rattributetext2 = ret_font.render('Population: Higher', True, 'red')
            if popdiff < 0:
                rattributetext2 = ret_font.render('Population: Lower', True, 'yellow')
                if popdiff < -5000000:
                    rattributetext2 = ret_font.render('Population: Lower', True, 'red')
            rtextrect2 = rattributetext2.get_rect(center = rattributerect2.center)
            areadiff = rdict['area'][1]
            if areadiff > 0:
                rattributetext3 = ret_font.render('Area: Higher', True, 'yellow')
                if areadiff > 100000:
                    rattributetext3 = ret_font.render('Area: Higher', True, 'red')
            if areadiff < 0:
                rattributetext3 = ret_font.render('Area: Lower', True, 'yellow')
                if areadiff < -100000:
                    rattributetext3 = ret_font.render('area: Lower', True, 'red')
            rtextrect3 = rattributetext3.get_rect(center = rattributerect3.center)
            
            if rdict['borders']:
                rattributetext4 = ret_font.render('borders: True', True, 'green')
            else:
                rattributetext4 = ret_font.render('borders: False', True, 'red')
            rtextrect4 = rattributetext4.get_rect(center = rattributerect4.center)
            if finaldict.get('region', False):
                if not finaldict.get('subregion', False):
                    if rdict.get('subregion', False):
                        finaldict['subregion'] = rdict['subregion']
            else:
                if rdict.get('region', False):
                    finaldict['region'] = rdict['region']
            if finaldict.get('populationdiff', False):
                if abs(finaldict['populationdiff']) > abs(popdiff):
                    finaldict['populationdiff'] = popdiff
                    finaldict['population'] = gss
            else:
                finaldict['populationdiff'] =  popdiff
                finaldict['population'] = gss

            if finaldict.get('areadiff', False):
                if abs(finaldict['areadiff']) > abs(areadiff):
                    finaldict['areadiff'] = areadiff
                    finaldict['area'] = gss
            else:
                finaldict['areadiff'] =  areadiff
                finaldict['area'] = gss
            if finaldict.get('borders', False):
                if rdict['borders']:
                    finaldict['borders'].append(gss)
            else:
                if rdict['borders']:
                    finaldict['borders'] = [gss]
            if finaldict.get('region', False):
                if finaldict.get('subregion', False):
                    finaltext1= ret_font.render(f"region: {finaldict['subregion']}", True, 'green')
                else:
                    finaltext1= ret_font.render(f"region: {finaldict['region']}", True, 'yellow')
            else:
                finaltext1= ret_font.render(f"region: Unkown", True, 'red')
            ftextrect1 = finaltext1.get_rect(center = fattributerect1.center)
            finaltext2 = ret_font.render(f'closest in population:  {finaldict["population"]}', True, 'yellow')
            ftextrect2 = finaltext2.get_rect(center = (fattributerect2.centerx, fattributerect2.centery - 20) )
            finaltext3 = ret_font.render(f'closest in area:  {finaldict["area"]}', True, 'yellow')
            ftextrect3 = finaltext3.get_rect(center = fattributerect3.center)
            if finaldict.get('borders', False):
                finaltext4 = ret_font.render(f'borders with {finaldict}', True, 'green')
            else:
                finaltext4= ret_font.render('no borders found', True, 'red')
            ftextrect4 = finaltext4.get_rect(center = (fattributerect4.centerx, fattributerect4.centery - 20))
            




    if flag:
        screen.blit(rattributetext1, rtextrect1)
        screen.blit(rattributetext2, rtextrect2)
        screen.blit(rattributetext3, rtextrect3)
        screen.blit(rattributetext4, rtextrect4)
        screen.blit(finaltext1, ftextrect1)
        screen.blit(finaltext2, ftextrect2)
        screen.blit(finaltext3, ftextrect3)
        screen.blit(finaltext4, ftextrect4)

    text_surface = guess_font.render(user_text, True, (255, 255, 255)) 
    screen.blit(game_text, textrect1)
    screen.blit(game_text2, textrect2) 
    screen.blit(extext, textrect3)
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

    if win:
        screen.fill('green')       
        screen.blit(wintext, winrect)
    input_rect.w = max(100, text_surface.get_width()+10)  
    pygame.display.flip()
    dt = clock.tick(60) / 1000