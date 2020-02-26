rem %1 should contain the value from vs build event macro $(SolutionDir) 
rem %2 should contain the value from vs build event macro $(ConfigurationName) 
rem %3 should contain the value from vs build event macro $(TargetDir) 
rem %4 should contain the value from vs build event macro $(ProjectName) 

echo variables:
echo SolutionDir: %1
echo ConfigurationName: %2
echo TargetDir: %3
echo ProjectName: %4

rem "copy to geometry friends build folder"
echo "start 1"
if exist "%1GeometryFriends\bin\%2\Agents\" copy /y "%3%4*" "%1GeometryFriends\bin\%2\Agents\"
echo "start 2"
if exist "%1GeometryFriends\bin\%2\Content\Agents\%2\" copy /y "%3%4*" "%1GeometryFriends\bin\%2\Content\Agents\%2\"
rem "copy to geometry friends project content folder"
echo "start 3"
if exist "%1GeometryFriends\Content\Agents\%2\" copy /y "%3%4*" "%1GeometryFriends\Content\Agents\%2\"
rem "cleanup unnecessary geometryfriends files"
echo "start 4"
cd %3%
echo "start 5"
del /s /q "FarseerPhysics*" "FarseerPhysics*" "GeometryFriends*" "OpenTK*" "Wii*"
echo "start 6"
rd /s /q "Content"