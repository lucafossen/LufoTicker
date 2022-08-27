import pygame
import json
import datetime
from widgets import *
from currency import *
from graph import *

#Main function
def main():
    
    #init font
    pair_font = pygame.font.SysFont("Verdana", 20)
    price_font = pygame.font.SysFont("Verdana", 40)
    buttonfont = pygame.font.SysFont("Verdana", 13)
    price_context_font = pygame.font.SysFont("Verdana", 15)
    contextcolor = (255, 255, 255)

    def load_settings():
        #load settings
        global settings
        with open("settings.json") as f:
            settings = json.load(f)
    load_settings()

    timeframe = "1hr"
    
    def convert_points_to_bounds(rect, points):
        global maxx, maxy, minx, miny
        maxx, minx, maxy, miny = None, None, None, None

        xvalues = []
        yvalues = []
        for i in points:
            xvalues.append(i[0])
            yvalues.append(i[1])
        
        # maximum and minimum x (time) and y (price) values
        maxx = max(xvalues)
        minx = min(xvalues)
        maxy = max(yvalues)
        miny = min(yvalues)

        # Get x and y ranges
        x_range = maxx - minx
        y_range = maxy - miny

        returnlist = [] # This will be populated with coordinate potisions

        # Translate values to pygame bounds
        for value in points:
            #Get width of the rectangle
            width = rect[2]
            height = rect[3]

            #Convert from values to points
            x = (value[0]-minx)/(x_range)*width
            #invert y values because pygame y coordinates go positively downwards
            y = height-((value[1]-miny)/(y_range)*height)
            #final point
            returnlist.append((x+rect[0], y+rect[1]))

        return returnlist

    def update_price(dest, graphrect):
        global pairsurface, pricesurface
        global graph_points
        global maxxfont, maxyfont, minxfont, minyfont

        pairsurface = pair_font.render(f'{settings["base"]}/{settings["quote"]}', True, (20, 230, 15))
        pricesurface = price_font.render(Pair(settings["base"], settings["quote"]).get_qprice(), True, (255, 200, 0))
        graph_points = convert_points_to_bounds(graphrect, Pair(settings["base"], settings["quote"]).get_historical_price(timeframe))

        maxxfont = price_context_font.render(str(datetime.datetime.fromtimestamp(maxx).strftime('%Y-%m-%d %H:%M')), True, contextcolor)
        maxyfont = price_context_font.render(str(maxy), True, contextcolor)
        minxfont = price_context_font.render(str(datetime.datetime.fromtimestamp(maxx).strftime('%Y-%m-%d')), True, contextcolor)
        minyfont = price_context_font.render(str(miny), True, contextcolor)
        
        
    #settings for large windows
    largewidth = 600
    largeheight = 450

    #settings for small window
    miniwidth = 350
    miniheight = 70

    #apply settings
    base = settings["base"]
    quote = settings["quote"]
    minimode = settings["minimode"]
    fresh_mode_change = True
    #If minimode is set to True, the screen will only show the price and nothing more
    if minimode:
        width, height = miniwidth, miniheight
    else:
        width, height = largewidth, largeheight

    #init pygame stuff
    pygame.init()
    favicon = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(favicon)
    pygame.display.set_caption("Price ticker")
    screen = pygame.display.set_mode(size=(width, height))

    # default sizes for buttons
    buttonx = 60
    buttony = 25
    buttoncolor = (100, 100, 255)
    buttontextcolor = (255, 255, 255)

    bg_color = (54, 57, 63)
    

    minimode_button = PushButton((0, 0, 80, 25), buttoncolor, buttontextcolor, buttonfont, "Minimode", screen)

    button0 = PushButton((20+0, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '1 hour', screen)
    button0.state = "1hr"
    button0.active = True
    
    button1 = PushButton((20+61, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '1 day', screen)
    button1.state = "1d"
    button2 = PushButton((20+122, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '1 week', screen)
    button2.state = "1w"
    button3 = PushButton((20+183, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '1 month', screen)
    button3.state = "1mo"
    button4 = PushButton((20+244, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '3 month', screen)
    button4.state = "3mo"
    button5 = PushButton((20+305, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '1 year', screen)
    button5.state = "1y"
    button6 = PushButton((20+366, 410, buttonx, buttony), buttoncolor, buttontextcolor, buttonfont, '3 year', screen)
    button6.state = "3y"

    timescalebuttons = (button0, button1, button2, button3, button4, button5, button6)
    graphrect = (30, 80, 400, 300)
    graph_surface = pygame.Surface((400, 300))
    graph_pos = (30, 80)
    graphbg = (230, 230, 230)

    graph_line_color = (1, 134, 243)

    # TODO: implement caching so that API calls are not made frivolously
    # #price cache
    # _1hrls = []
    # _1dls = []
    # _1wls = []
    # _1mols = []
    # _3mols = []
    # _1yls = []
    # _3yls = []

    #variables for game logic
    updaterate = 2500
    updatetime = pygame.time.get_ticks() + updaterate
    fresh_update_time = True
    update_price(screen, graphrect)

    running = True
    while running:
        #EVENTS
        for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If minimode is deactivated
                    if minimode_button.rect.collidepoint(pygame.mouse.get_pos()) and minimode_button.active:
                        minimode_button.toggle()
                        screen = pygame.display.set_mode(size=(width, height))
                    #If minimode is activated
                    elif minimode_button.rect.collidepoint(pygame.mouse.get_pos()) and not minimode_button.active:
                        minimode_button.toggle()
                        screen = pygame.display.set_mode(size=(miniwidth, miniheight))
                    #For all the timescale buttons
                    for button in timescalebuttons:
                        #If a certain timescalebutton is pressed
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            if not button.active:
                                #if button.text == "1 hour":
                                #    print("1 hour")
                                updatetime = pygame.time.get_ticks()
                                button.select(timescalebuttons)
                            

                            
        
        #GAME LOGIC
        # if minimode_button.active and fresh_mode_change:
            
        #     fresh_mode_change = False
        # if not minimode_button.active and fresh_mode_change:
        #     screen = pygame.display.set_mode(size=(width, height))
        if pygame.time.get_ticks() > updatetime and fresh_update_time == True:
            fresh_update_time = False
            updatetime += 2500
            update_price(screen, graphrect)
        else:
            fresh_update_time = True
        
        for button in timescalebuttons:
            if button.active:
                timeframe = button.state
                
        #BLITS
        screen.fill((bg_color))

        screen.blit(pairsurface, (90, 0))
        screen.blit(pricesurface, (30, 20))

        minimode_button.draw()
        if not minimode_button.active:
            for button in timescalebuttons:
                button.draw()
            graph_surface.fill(graphbg)
            screen.blit(graph_surface, graph_pos)
            pygame.draw.lines(screen, graph_line_color, False, graph_points, 2)
            screen.blit(maxxfont, (350, 380))
            screen.blit(minxfont, (30, 380))
            screen.blit(maxyfont, (435, 80))
            screen.blit(minyfont, (435, 360))

        pygame.display.flip()

#call main if not imported
if __name__ == '__main__':
    main()