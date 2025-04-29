@echo off
echo Loading ferry system sample data...
python manage.py shell < ferry_system/sample_data.py
echo Done!
pause
