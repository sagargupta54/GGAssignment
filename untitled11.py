import json


'''
 Determine the number of sessions per user per 
 Determine the average session length per user per game
'''
def NumberofSessionsperUserperGame(log_dic,fw):
    errorC=0
    error=''
    
    print('\ngame_id','            ','User','                            ','No. of Sessions', '  ' ,'Average Session Length')
    fw.write('game_id            User                           No. of Sessions    Average Session Length\n')
    
    
    for game in log_dic:  #iterate on gameID
        for user in log_dic[game]: #for one game iterate on userID
            numberofSessions=0
            sessionLength=0
            array=log_dic[game][user]
            
            array.sort() #sorting events on time in increasing order
            #print(array)
            startList=[]
            
            
            '''
            logic:
            
            when a start time is found add it in to startList list.
            If one was already there it means it is non terminated session and we will ignore it.
            and add this new one but we will count is number of sessions.
            
            when a stop event is found, search for the corresponding start time in startList list(in list only zero or one entery is present only)
            If none is found, ignore that event because it is without start.             
            else calculate session length.
            
                    
            '''
            
            for time in array:
                if(time[-1]=='t'):
                    if(not startList):
                        startList.append(time[:-1])
                        #print("start",startList)
                    else:
                        errorC=errorC+1 #these are error entry which we ignored
                        numberofSessions=numberofSessions+1
                        error=error+game+'     '+user+'    '+'ggstart'+'    '+startList[0]+'\n'
                        startList.pop()
                        startList.append(time[:-1])
                else:
                    if(startList):
                        t1=startList[0]
                        t2=time[:-1]
                        duration=float(t2)-float(t1)#calculating session length
                        
                        numberofSessions=numberofSessions+1
                        sessionLength=sessionLength+duration
                        startList.pop()
                    else:
                        
                        errorC=errorC+1
                        error=error+game+'     '+user+'    '+'ggstop'+'    '+time[:-1]+'\n'
            if(startList):
              numberofSessions=numberofSessions+1
              errorC=errorC+1
                        
            #display data            
            if(numberofSessions>0):
                
                average=format(float(sessionLength/numberofSessions),'.4f')
                print(game,'      ',user,'             ',numberofSessions,'     ',(average))
                
                out=  game+'      '+user+'              '+str(numberofSessions)+'     '+str(average)+'\n'              
                fw.write(out)
            
            else:
                
                out=  game+'      '+user+'              '+str(numberofSessions)+'     '+str(0)+'\n'
                fw.write(out)
                print(game,'      ',user,'             ',numberofSessions,'       ',0)
   
    
    
    
    print('\n\nNumbers of logs to which no matching login information are found and are ignored are ',errorC)
    out='\n\nNumbers of logs to which no matching login information are found and are ignored are '+str(errorC)+'\n'
    fw.write(out)
    fw.write(error)
                
                
        
#give number of unique user per game

def numberofUsersperGame(log_dic,fw):
    
    print('gameID','     ','No. of Unique Users')
    fw.write('gameID     No. of Unique Users\n')
    for game in log_dic:
        print(game,'            ', len(log_dic[game]))
        out=game+'            '+str( len(log_dic[game]))+'\n'
        fw.write(out)
    fw.write('\n')
    
    





def main():
    log_dic={}
    try:
        with open('ggevent.log') as fp: 
            
        
            #print("Name of the file: ", fp.name)
            
            
            
            for line in fp:# read file line by line
                dic={} #initialize empty dictionary
                try:
                    '''
                    
                    every line present in log file is already in Dictionary format but as String type. Using JSON we will convert string
                    in to Dictionary type and assign it to dic.
                    
                    
                    '''
                    dic=json.loads(line)  #JSON convert the string in to dicionary format
                    '''
                    Now we can use 'ai5','event','game_id','timestamp' as key to dictionary 
                    to fetch userid,event,gameID,time respectively
                    
                    '''
                    gameID=dic['bottle']['game_id'] #give game unique id
                    userID=dic['headers']['ai5'] # give user unique id
                    eventName=dic['post']['event'][-1] # 'p' for ggstop and 't' for ggstart
                    
                    timeS=dic['bottle']['timestamp'] #give timestamp
                    
                    
                    '''
                    below we will find year month day hour minute second from timestamp
                    
                    '''
                    year=timeS[0:4]
                    month=timeS[5:7]
                    day=timeS[8:10]
                    hour=timeS[11:13]
                    min=timeS[14:16]
                    sec=timeS[17:]
                    
                    #converting timestamp in to seconds
                    timeS=float(year)*365*24*3600 + float(month)*30*24*3600 + float(day)*24*3600 + float(hour)*3600 + float(min)*60 + float(sec)
                    
                    #attahcing event to seconds to identify whether it is ggstart  time or ggstop  time
                    timeS=str(timeS)+eventName 
                    #print(timeS)
                    
                    '''
                    populating global dictionary(log_dic) from every line in file.
                    
                    log_dic will be of following format
                    
                    log_dic={game_id:{user_id:[list of events]}}
                    
                    
                    logic:
                    
                    Corresponding to one game_id we will have different users and
                    for every user we have list of events
                    
                    
                    using above logic we will populate log_dic from file
                    
                    '''
                    
                    
                    if gameID in log_dic:  #check if gameid is already present
                        if userID in log_dic[gameID]: #check user is present for particular game_id
                            log_dic[gameID][userID].append(timeS)
                        else:
                            log_dic[gameID][userID]=[timeS] #add user_id as key in inner dictionary
                      
                      
                      
                    else:  #game_id not present so add game_id, user_id for that game_id and list of events in Dictionary
                        log_dic[gameID]={}
                        log_dic[gameID][userID]=[]
                        log_dic[gameID][userID].append(timeS)
                        
                    
                    
                except Exception as e:
                    
                    print("Exceptions in Data ", str(e))
                    
            
            #print(log_dic)
            
            fw = open('result.txt','w')
                
            #calling of functions        
            numberofUsersperGame(log_dic,fw)
            NumberofSessionsperUserperGame(log_dic,fw)
            
    except Exception as e1:
        print("Exceptions in Data ",str(e1))
            
        
    finally:
        fp.close
        fw.close()
    
    
        
        

if __name__ == '__main__':
    
    main()
    