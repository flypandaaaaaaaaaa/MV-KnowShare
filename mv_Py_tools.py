import os,sys
if sys.argv[1]=="start":
    os.system("python mvknow_app.py")
    os.system("python monitor_mission.py")
    print("启动成功")
elif sys.argv[1]=="stop":
    os.system("pkill python ")
    print("程序停止")
else:
    print("参数错误，请输入start或者stop")