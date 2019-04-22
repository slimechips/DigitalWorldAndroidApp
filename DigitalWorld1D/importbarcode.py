import barcode
import random
import os
from barcode.writer import ImageWriter
#from wand.image import Image
#from wand.display import display
from kivy.logger import Logger
from kivy.utils import platform

# stall dish user
stalls=['Chicken Rice','Japanese']
dishes=[1,2,3,4,5,6,7,8,9,10]
sn=0
barcodeno=0
def barcode_generator(stallind,dishind,userid,date,time):
	# stall ind, dish in, date, time, uid

	# barcodeno=int('1'+ str(stallind).zfill(2) + str(dishind).zfill(2)
	# 				  + str(date)+ str(time) + str(userid).zfill(4))

	useridno='00'+str(userid)
	dishidno='00'+str(dishind)
	stallidno='0'+str(stallind)
	generated=0

	if stallind==1 :
		if dishind==1:
			generated='2345'
		if dishind==2:
			generated='4845'
		if dishind==3:
			generated='4345'
		if dishind==4:
			generated='9823'
	elif stallind==2 :
		if dishind==1:
			generated='2343'
		if dishind==2:
			generated='4872'
		if dishind==3:
			generated='4312'
		if dishind==4:
			generated='9800'
	elif stallind==3 :
		if dishind==1:
			generated='1143'
		if dishind==2:
			generated='2272'
		if dishind==3:
			generated='3312'
		if dishind==4:
			generated='4500'
	elif stallind==4 :
		if dishind==1:
			generated='2343'
		if dishind==2:
			generated='4872'
		if dishind==3:
			generated='4312'
		if dishind==4:
			generated='1002'
		
		
	
	barcodeno=generated+useridno+stallidno+dishidno
	
	image = barcode.get_barcode_class('ean13')
	Logger.info(image)
	image_bar = image(u'{}'.format(barcodeno),writer=ImageWriter())
	if platform == "android":
		root = os.getenv('EXTERNAL_STORAGE') or os.path.expanduser("~")
		sub_folder_path = os.path.join(root, "ezeat")
		if not os.path.exists(sub_folder_path):
			os.makedirs(sub_folder_path)
		filePath = os.path.join(sub_folder_path, barcodeno + ".png")
	else:
		desktop = os.path.join(os.path.expanduser("~"), "Desktop")
		filePath = os.path.join(desktop, "test.png")
	f = open(filePath,'wb')
	image_bar.write(f)
	print(barcodeno)
	return barcodeno
	
	#add date time instead of the random numbers



