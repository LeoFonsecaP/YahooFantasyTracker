import os
import time

os.system('git checkout main')
exec(open("./fantasy_stats.py").read())
time.sleep(3)
os.chdir('./fantasytracker')
os.system('npm run build')
time.sleep(3)
os.chdir('..')
os.system('git add ./fantasytracker/src/Components/Data')
os.system('git add ./fantasytracker/build')
os.system('git commit -m "Automatic update on data"')
os.system('git push -u origin main')
time.sleep(3)
exec(open("./TwitterBot.py").read())


