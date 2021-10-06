'''application version 4'''
import sys
import os
import glob
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
from PyQt5 import QtGui, QtWidgets
from main_ui import Ui_MainWindow
import logic

#create folders
cwd = os.getcwd()

#creating folder for new pictures
direct = os.path.join(cwd,"nor")

if not os.path.exists(direct):
    os.mkdir(direct)

#creating folder for output excel files
direct1 = os.path.join(cwd,"output excel files")

if not os.path.exists(direct1):
    os.mkdir(direct1)

#creating folder for input excel files
direct2 = os.path.join(cwd,"input excel files")

if not os.path.exists(direct2):
    os.mkdir(direct2)

#init
app = QtWidgets.QApplication(sys.argv)

class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):
    '''init of ui'''
    def __init__(self, *args, **kwargs):
        super(MainUi, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('data.png'))

#showing window
ui = MainUi()
ui.show()

#creating save.txt file or reading from it
try:
    if os.stat("saves.txt").st_size != 0:
        save_file = open("saves.txt", "r")
        file1 = save_file.readlines()
        ui.base.setText(file1[0][:-1])
        ui.img_base.setText(file1[1][:-1])
        save_file.close()
except FileNotFoundError:
    save_file = open("saves.txt", "w+")
    save_file.write("֊ ֊ -  ընտրեք ապրանքների բազան  ֊ ֊ ֊" + "\n" +
    "- ֊ ֊  ընտրեք նկարների բազան  ֊ ֊ ֊")
    save_file.close()

#creating alert
alert = QtWidgets.QMessageBox()
alert.setStyleSheet("QLabel{min-width: 300px; min-height: 200px;"
            + " font-size: 16px;qproperty-alignment: AlignCenter;}")

cwd = os.path.join(cwd,"output excel files")

#logic
def start_btn_clicked():
    '''start btn clicked'''

    #read paths
    base_df_read_path = ui.base.text()
    new_file_read_path = ui.new_file.text()
    image_base_read_path = ui.img_base.text()

    #checking paths are they empty or no
    if checking_if_lable_is_empty(base_df_read_path, new_file_read_path, image_base_read_path) != 0:
        return 0

    image_base_read_path += '/*'

    if ui.new_pictures.isChecked():
        #checking selected paths are they usefull or no
        if checking_selected_paths(base_df_read_path, new_file_read_path):
            base_df = pd.read_excel(base_df_read_path, usecols=['id', 'name', 'full_name'])
            new_file_df = pd.read_excel(new_file_read_path, usecols= ['id', 'full_name','price'])

        else:
            return 0

        #getting base and new file dict
        base_dict = logic.from_df_to_dict(base_df)
        new_file_dict = logic.from_df_to_dict(new_file_df)

        #file names
        file_names = glob.glob(image_base_read_path)

        #iamge ids and formats
        image_ids, image_formats = logic.getting_image_ids_and_formats(file_names)

        #are in base and arent in base
        are_in_base, arent_in_base = logic.geting_elements_that_are_and_arent_in_base(base_dict, new_file_dict)

        #output new elements that are not in base
        if arent_in_base:
            list_1 = logic.from_dict_to_list(arent_in_base)
            df_1 = pd.DataFrame(list_1, columns=['id', 'full_name', 'price'])
            direct_1 = os.path.join(cwd,'apranqner_vornq_bazayum_chkan.xlsx')
            df_1.to_excel(direct_1)

        else:
            #delete excel file
            direct_1 = os.path.join(cwd,'apranqner_vornq_bazayum_chkan.xlsx')

            if os.path.exists(direct_1):
                os.remove(direct_1)

        #image id mapping
        image_id_mapping = logic.from_base_and_are_dict_get_dict(base_dict, are_in_base)

        #logic
        progress = 0
        lent2 = len(image_id_mapping)
        list_2 = []
        text = ["1", "2", "3"]
        lent = len(file_names)

        for i in range(lent):
            if image_ids[i] in image_id_mapping:
                #opening image adding rectangle
                img = Image.open(file_names[i])
                wid, heig = img.size
                heig_delta = 140 + 10*int((wid-400)/100)
                img_2 = Image.new("RGB", (wid, heig+heig_delta))
                draw = ImageDraw.Draw(img_2)
                draw.rectangle([(0,0), (wid, heig_delta)], fill ="white")
                img_2.paste(img,(0,heig_delta))

                #text for drawing
                k = 0
                for j in image_id_mapping[image_ids[i]]:
                    text[k] = str(j)
                    k += 1

                #font and wid and height of text
                font_size = 20 + 4*int((wid-400)/100)
                font_1 = ImageFont.truetype('Arial.TTF', font_size)
                wid_of_text, heig_of_text = font_1.getsize(text[1])

                #checking text if it fits in width of picture
                if wid_of_text > wid:
                    ind = int(len(text[1])*wid/wid_of_text)
                    ind_2 = text[1].rfind(' ', 0, ind)
                    text[1] = text[1][:ind_2] + "\n" + text[1][ind_2 + 1:]

                #drawing text
                draw.text((0, 0), text[0], (0, 0, 0), font=font_1)
                draw.text((0, heig_delta/2 - heig_of_text), text[1], (0, 0, 0), font = font_1)
                draw.text((0, heig_delta - heig_of_text), text[2], (0, 0, 0),  font = font_1)

                #save image
                path_3 = direct + "/{img_id}{img_form}".format(img_id = image_ids[i], img_form = image_formats[i])
                img_2.save(path_3)
                image_id_mapping.pop(image_ids[i])

                #progressbar
                progress += 1
                progress_in_percent = int(progress/lent2*100)
                ui.progressBar.setValue(progress_in_percent)

            else:
                #pictures that arent in base
                list_2.append(image_ids[i])

        #output pictures that are not in base
        if list_2:
            df_2 = pd.DataFrame(list_2, columns=['nkarner voronq bazayum chkan'])
            direct_2 = os.path.join(cwd,'nkarner_voronq_bazayum_chkan.xlsx')
            df_2.to_excel(direct_2)

        else:
            #delete excel file
            direct_2 = os.path.join(cwd,'nkarner_voronq_bazayum_chkan.xlsx')

            if os.path.exists(direct_2):
                os.remove(direct_2)

        #output items that have no pictures
        if image_id_mapping:
            list_3 = logic.from_dict_to_list(image_id_mapping)
            df_3 = pd.DataFrame(list_3, columns=['name', 'id', 'full_name', 'price'])
            direct_3 = os.path.join(cwd, 'ays_apranqneri_nkarnery_chka.xlsx')
            df_3.to_excel(direct_3)

        else:
            #delete excel file
            direct_3 = os.path.join(cwd, 'ays_apranqneri_nkarnery_chka.xlsx')

            if os.path.exists(direct_3):
                os.remove(direct_3)
        ui.progressBar.setValue(100)
        #alert of finish
        alert.setWindowTitle("Program Finished")
        alert.setText("Ավարտված")
        alert.exec_()

    elif ui.base_update.isChecked():
        #this function is not supported yet
        alert.setWindowTitle("THIS FUNCTION IS`NT YET ALLOWED")
        alert.setText("Կներեք այս ֆունկցիան \n դեռ պատրաստ չէ")
        alert.exec_()

    else:
        #if something gone wrong
        alert.setWindowTitle("WRONG THING")
        alert.setText("Ընտրեք գործողություններից մեկը այնուհետև սեղմեք START կոճակին")
        alert.exec_()


def checking_selected_paths(base_df_read_path, new_file_read_path):
    """checking selected paths getting 2 paths"""

    #checking base read path
    try:
        pd.read_excel(base_df_read_path, usecols=['id', 'name', 'full_name'])
    except ValueError as err:
        err = str(err)
        ind = err.rfind(":")
        alert.setWindowTitle("Something wrong with excel")
        alert.setText("Սխալ կա բազայի excel֊ի մեջ, սունյակի վեռնագիրը պետք է լինի id, full_name, price!!!" + err[ind + 4:-2])
        alert.exec_()
        return 0

    #checking new file read path
    try:
        pd.read_excel(new_file_read_path, usecols= ['id', 'full_name','price'])
    except ValueError as err:
        err = str(err)
        ind = err.rfind(":")
        alert.setWindowTitle("Something wrong with excel")
        alert.setText("Սխալ կա նոր ֆայլի excel֊ի մեջ, սունյակի վեռնագիրը պետք է լինի id,"
        + "full_name, price!!!\n " + "Նոր ֆայլում բացակայում է "
        + err[ind + 4:-2] + " վեռնագրով սունյակը!!!!")
        alert.exec_()
        return 0

    return 1


def checking_if_lable_is_empty(text1, text2, text3):
    """getting 3 texts and cheking if labels are empty or no"""

    res = 0

    #checking base lable
    if text1 == "֊ ֊ -  ընտրեք ապրանքների բազան  ֊ ֊ ֊":
        res += 1
        ui.base.setStyleSheet("color: rgb(255,0,0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(255,0,0);")

    #checking new file lable
    if text2 == "֊ ֊ ֊  ընտրեք նոր ֆայլը  ֊ ֊ ֊":
        res += 1
        ui.new_file.setStyleSheet("color: rgb(255,0,0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(255,0,0);")

    #checking base of pictures lable
    if text3 == "- ֊ ֊  ընտրեք նկարների բազան  ֊ ֊ ֊":
        res += 1
        ui.img_base.setStyleSheet("color: rgb(255,0,0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(255,0,0);")

    return res


#connection functions
def browse1_btn_clicked():
    '''browse button click'''

    file_filter  = "Excel File (*xlsx *xls)"
    path = QtWidgets.QFileDialog.getOpenFileName(filter = file_filter)

    #new base is selected
    if path[0]:
        ui.base.setText(path[0])
        save_file1 = open("saves.txt", "r")
        list_of_lines = save_file1.readlines()
        list_of_lines[0] = str(path[0]) + '\n'
        save_file1.close()
        save_file1 = open("saves.txt", "w")
        save_file1.writelines(list_of_lines)
        save_file1.close()

    else:
        #new base is not selected
        save_file1 = open("saves.txt", "r")
        list_of_lines = save_file1.readlines()
        list_of_lines[0] = "֊ ֊ -  ընտրեք ապրանքների բազան  ֊ ֊ ֊" + '\n'
        save_file1.close()
        save_file1 = open("saves.txt", "w")
        save_file1.writelines(list_of_lines)
        save_file1.close()
        ui.base.setText("֊ ֊ -  ընտրեք ապրանքների բազան  ֊ ֊ ֊")
        ui.base.setStyleSheet("color: rgb(150, 150, 150);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


def browse2_btn_clicked():
    '''browse button click'''

    file_filter  = "Image File (*jpg *png *jpeg)"
    path = QtWidgets.QFileDialog.getOpenFileName(filter = file_filter)
    img_path = path[0]

    #new image path is selected
    if path[0]:
        index_of = img_path.rfind('/')
        img_path = img_path[:index_of]
        ui.img_base.setText(img_path)
        save_file1 = open("saves.txt", "r")
        list_of_lines = save_file1.readlines()
        list_of_lines[1] = str(img_path) + '\n'
        save_file1.close()
        save_file1 = open("saves.txt", "w")
        save_file1.writelines(list_of_lines)
        save_file1.close()

    else:
        #new image path is not selcted
        save_file1 = open("saves.txt", "r")
        list_of_lines = save_file.readlines()
        list_of_lines[1] = "- ֊ ֊  ընտրեք նկարների բազան  ֊ ֊ ֊" + '\n'
        save_file1.close()
        save_file1 = open("saves.txt", "w")
        save_file1.writelines(list_of_lines)
        save_file1.close()
        ui.img_base.setText("- ֊ ֊  ընտրեք նկարների բազան  ֊ ֊ ֊")
        ui.img_base.setStyleSheet("color: rgb(150, 150, 150);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


def browse3_btn_clicked():
    '''browse button click'''

    file_filter  = "Excel File (*xlsx *xls)"
    path = QtWidgets.QFileDialog.getOpenFileName(filter = file_filter)

    #new file is selected
    if path[0]:
        ui.new_file.setText(path[0])

    else:
        #new file is not selected
        ui.new_file.setText("֊ ֊ ֊  ընտրեք նոր ֆայլը  ֊ ֊ ֊")
        ui.new_file.setStyleSheet("color: rgb(150, 150, 150);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


def img_base_chng():
    '''img base chng'''

    ui.img_base.setStyleSheet("color: rgb(0, 0, 0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


def base_chng():
    '''base chng'''

    ui.base.setStyleSheet("color: rgb(0, 0, 0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


def new_file_chng():
    '''new file chng'''

    ui.new_file.setStyleSheet("color: rgb(0, 0, 0);\n"
"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: rgb(0, 206, 0);")


#connections
ui.Browse1.clicked.connect(browse1_btn_clicked)
ui.Browse2.clicked.connect(browse2_btn_clicked)
ui.Browse3.clicked.connect(browse3_btn_clicked)
ui.img_base.textChanged.connect(img_base_chng)
ui.base.textChanged.connect(base_chng)
ui.new_file.textChanged.connect(new_file_chng)
ui.btn_start.clicked.connect(start_btn_clicked)


#exit
sys.exit(app.exec_())
