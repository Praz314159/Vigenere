@ echo off 
:A 
Cls
echo Messenger 
set /p n=User: 
set /p m=Message: 
net send %n% %m% 
Pause 
GoTo A 
