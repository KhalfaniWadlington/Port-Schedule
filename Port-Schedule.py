#!/usr/bin/python3
import datetime
from quickstart import get_service
import os
tomorrow=str(datetime.datetime.today()+datetime.timedelta(days=1)).split(" ")[0]
service=get_service()
current_directory=os.path.dirname(os.path.realpath(__file__))
def get_tasks():
    tasks= open(current_directory+'/Schedule.csv').readlines()
    x=tasks[2].split(",")[2]
    print(tasks[2],x,'"%s"' %x,x=="")
    Break=tasks[0].split(",")[-1]
    #print(Break)
    List=[]
    #the following will split the values and remove linebreaks 
    count=0
    for todo in [i.replace("\n","").split(",") for i in tasks[1:]]: #skip first line 
        #Action, Length,Start,End
        if todo[0] != "": #there must be an action
            action=todo[0]
            
            Length=todo[1]
            #Convert to 24 hour format
            
            Start=todo[2]
            End=todo[3]
         
            print(action+" "+Start+", "+End)
            if "Break" not in action:
                count+=1    #Keep track of the number of actions so I can reference them later
                create_event(str(count)+": "+action,Start,End)
            else:
                create_event(action,Start,End)
                
#time should be "XX:XX [AM or PM]" as per LibreOffice Calc Format
def convert_to_24h(time):
    timeparts=time.split(" ")
    hours,minutes=timeparts[0].split(":")
    if hours=="12":
        return "00:"+minutes if timeparts[1]=="AM" else "12:"+minutes
    if timeparts[1]=="AM":
        return hours+":"+minutes 
    if timeparts[1]=="PM":
        hours=str(int(hours)+12)
        return hours+":"+minutes 
    
def create_event(name,start,end,date=tomorrow):
    print(convert_to_24h(start),convert_to_24h(end))
    event = {
      'summary': name,
      
    #  'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': date+'T'+convert_to_24h(start)+":00",
        'timeZone': 'America/Chicago'
      },
      'end': {
        'dateTime':  date+'T'+convert_to_24h(end)+":00",
        'timeZone': 'America/Chicago'
      },
       'reminders': {#don't add any reminders
       'useDefault': False,
    
      }
    }
 
    event = service.events().insert(calendarId=get_schedule_calendar_id(), body=event).execute()#Tasks is not a calander everyone has
    print ('Event created: %s ' % (event.get('htmlLink')))
    #document id
    f=open(".createdevents","a") 
    f.write(event.get('id')+"\n")
    f.close()
def delete_created_events():
    tasks= open('/home/khalfani/Desktop/Schedules.csv').readlines()
    
    for createdevent in  tasks: #skip first line 
        service.events().delete(calendarId=get_schedule_calendar_id(), eventId=createdevent).execute()
def create_calendar(): 
    calendar = {
    'summary': 'Schedule List',
    'timeZone': 'America/Chicago',
    'description':'Automatically created calendar for scheduling your to-do list. This was created by Khalani\'s app'
    }

    created_calendar = service.calendars().insert(body=calendar).execute()
    with open('.ScheduleId',"w") as f:
        return f.write(created_calendar['id'])
def get_schedule_calendar_id():
    with open('.ScheduleId') as f:
        return f.read()
    
if __name__ == "__main__":
    if not os.path.exists('.ScheduleId'):
        print("creating calendar")
        create_calendar()
    get_tasks()
    
