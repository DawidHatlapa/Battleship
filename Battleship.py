import sys, os, time, string, random
from random import randint

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            print('      Welcome To The Game\n\t⚓️BATTLESHIP⚓️\n')
            print("This is Player vs Player version\n")
            size = int(input("choose board size from 5 to 15:\n "))
            if size == 0 or size > 15 or size < 5:
                print("Please type from 5-15")
                continue
            else:
                return int(size)
        except ValueError:
            print("Please type from 5-15")


size = menu()
msize = 2*size+3

ABC = list(string.ascii_uppercase)
A1 = [str(i) for i in list(range(1,size+1))]
A2 = [str(i) for i in list(range(1,size+1))]

fleet_p1 = []
fleet_p2 = []
empty_mark = " "
s_mark = "O"
shot_mark = "X"
missfire_mark = "M"
b_mark = "."
hit_mark = "*" 
v4 = []

board1 = []
board2 = []
gap = []
gap2 = []
bufor_all = []

for i in range(0,size):
    for j in range(0,size):
        a = ([" "]*size)
        board1.append(a)

for i in range(0,size):
    for j in range(size+3,msize):
        a = ([" "]*size)
        board2.append(a)

len_board1 = len(board1)

#create two boards
def game_board(): 
    os.system('cls' if os.name == 'nt' else 'clear')
    result1 = " ".join('{:<3}'.format(A1[i]) for i in range(0,size))
    result2 = " ".join('{:<3}'.format(A2[i]) for i in range(0,size))

    print(" ","Player_1",(len(result1))*" ","Player_2","\n")
    print(4*" ",result1,10*" ",result2)
    print("  ","+---"*size,"          ","+---"*size)
    for i in range(size):
        print(ABC[i]," |"," | ".join(board1[i]),"|","      ",ABC[i]," |"," | ".join(board2[i]),"|")
        print("  "," ---"*size,"          "," ---"*size)
    print("\n")


def mark_the_spot(spot,mark,player): 
    x = spot[0]
    y = spot[1]
    if player == 1:
        board2[x][y] = mark
    else:
        board1[x][y] = mark
    game_board()


def mark_the_spot_from_list(spot,mark,player): 
    for i in spot:                     
        x = i[0]
        y = i[1]
        if player == 1:
            board1[x][y] = mark
        else:
            board2[x][y] = mark
    game_board()

#assig coords
def assign(row, column): 

    row = row.upper()
    if row in ABC:
        if int(column) <= size:
            return (ABC.index(row), A1.index(column))
        else:
            return False
    else:
        return False
 
#a - coords, t - size / create ship
def create_vessel_horizontal(a,t): 
    tmp_list = []
    for i in a:
        x = int(i[0])
        y = int(i[1])
        for i in range(y,y+t):
            tmp_list.append((x,i))
        if check_range_error(tmp_list,size) == False:
            print("ship out of board or some posiotion(s) occupied")
            return v4
        else:
            for i in tmp_list:
                v4.append(i)
            return v4

# a - coords, t - size create ship
def create_vessel_vertical(a,t): 
    tmp_list = []
    for i in a:
        x = int(i[0])
        y = int(i[1])
        for i in range(x,x+t):
            tmp_list.append((i,y))
        if check_range_error(tmp_list,size) == False:
            continue
        else:
            for i in tmp_list:
                v4.append(i)                    
            return v4
        break

# check board
def check_range_error(g,size): 
    for i in g:
        x = int(i[0])
        y = int(i[1])          
    if (x not in range(0,size)) or (y not in range(0,size)):
        print("false")
        return False
    elif i in v4:
        print(i,"position occupied already")
        return False
    else:
        print("true")
        return True

# return length of list shots for check win, if 0 is return = no ships
def winners_check(in_list,shots):
    for i in in_list:
        if i in shots:
            shots.remove(i)
        else:
            continue    
    return (len(shots))

# create bufor
def ship_bufor_vertical(ship): 
    bufor = []
    while True:
        for i in ship:
            x = i[0] 
            y = i[1]
            if (x not in range(0,size)) or (y not in range(0,msize)):
                continue
            else:                    
                for i in range(x-1,x+2): 
                    bufor.append((i,y-1))        
                    bufor.append((i,y))
                    bufor.append((i, y+1))
            bufor = set(bufor)
            bufor = list(bufor)
            for i in ship:
                if i in bufor:
                    bufor.remove(i)
            bufor.sort()

            
        return bufor


def ship_bufor_horizontal(ship): 
    bufor = []
    while True:
        for i in ship:
            x = i[0] 
            y = i[1]
            if (x not in range(0,size)) or (y not in range(0,size)):
                continue
            else:
                for i in range(y-1,y+2): 
                    bufor.append((x-1,i))        
                    bufor.append((x,i))
                    bufor.append((x+1,i))
            bufor = set(bufor)
            bufor = list(bufor)
            for i in ship:
                if i in bufor:
                    bufor.remove(i)
            bufor.sort()        
        return bufor

# match bufor
def bufor_cut(bufor,board_size,fleet): 
    tmp =[]
    for i in bufor:
        if (i[0] > board_size-1 or i[0] < 0) or (i[1] > size or i[1] < 0):
            tmp.append(i)
    for i in bufor:
        if i in gap:
            bufor.remove(i)
    for i in bufor:
        if i in gap2:
            bufor.remove(i)
    for i in bufor:
        if i in v4:
            tmp.remove(i)
    for i in tmp:
        if i in bufor:
            bufor.remove(i)        
        else:
            continue
    for i in bufor:
        bufor_all.append(i)
    return bufor

def play():
    in_list_p1 = []
    in_list_p2 = []
    current_fleet = []

    counter = 0

    while True:
        current_list = []
        if counter % 2 == 0:
            player = 1
            current_fleet = fleet_p2
            print("Player 1 turn")
            print("Player 1 in_list: ",in_list_p1)
            current_list = in_list_p1
        else:
            player = 2
            current_fleet = fleet_p1
            print("Player 2 turn")
            print("Player 2 in_list: ",in_list_p2)
            current_list = in_list_p2        
        
        print("Shoot player",player)
        
        coords = input()

        if len(coords) < 2:
                continue
        elif assign(coords[0],coords[1:]) == False:
            print("uncorrect shot / position out of board")
            continue
        elif int(coords[1:]) > size:
            continue
        else:
            place = assign(coords[0],coords[1:])
            if place in current_list:
                print("Already choosen")
                continue
            elif place in gap:
                print("gap")
                continue
            else:
                current_list.append(place)
            
            counter += 1
            
            if place in current_fleet:
                mark_the_spot(place,hit_mark,player)
                left_lives = winners_check(current_list,current_fleet)
            else:
                mark_the_spot(place,missfire_mark,player)
                left_lives = winners_check(current_list,current_fleet)

            if left_lives == 0:
                print("game_over")
                print("The winner is Player",player)
                input()
                break
            else:
                continue


def create():
    current_ves = []
    for i in range(1,3):
        player = i
        print("Player", i, "turn")
        v_no = int(input(" how many ship you wont create:\n"))

        for i in range(0,v_no):
            current_ves.clear()
            vorient = input("choose ship orientation vertical or horizontal v or h: \n")
            if vorient == "v":
                coords = input("type top/left ship coord:\n")
                vsize = int(input("type size of your ship\n"))

                current_ves.append(assign(coords[0],coords[1:]))
                cvv = create_vessel_vertical(current_ves,vsize)
                check_range_error(cvv,size)
                mark_the_spot_from_list(cvv,s_mark,player)
                sbv = ship_bufor_vertical(cvv)
                bcv = bufor_cut(sbv,size,v4)
                bcv = mark_the_spot_from_list(bcv,b_mark,player)
                
                for i in v4:
                    if player == 1:
                        fleet_p1.append(i)
                    else:
                        fleet_p2.append(i)
                
                v4.clear()

            elif vorient == "h":
                coords = input("type top/left ship coord:\n")
                vsize = int(input("type size of your ship\n"))
                
                current_ves.append(assign(coords[0],coords[1:]))

                print(current_ves)
                print(type(current_ves))
                cvh = create_vessel_horizontal(current_ves,vsize)
                check_range_error(cvh,size)
                mark_the_spot_from_list(cvh,s_mark,player)
                sbh = ship_bufor_horizontal(cvh)
                bc = bufor_cut(sbh,size,v4)
                bc = mark_the_spot_from_list(bc,b_mark,player)
            
                for i in v4:
                    if player == 1:
                        fleet_p1.append(i)
                    else:
                        fleet_p2.append(i)
                
                v4.clear()

        input("Hit enter to clear board")
        mark_the_spot_from_list(fleet_p1,empty_mark,player)
        mark_the_spot_from_list(fleet_p2,empty_mark,player)
        mark_the_spot_from_list(bufor_all,empty_mark,player)


game_board()
create()
play()


