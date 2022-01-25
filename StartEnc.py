import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import win32api
import os, sys

# ---------------------------------------------------------------------
# 這一支程式，主要的目的為調用外部的exe檔(名稱為enc.exe)，並使用它加密我們所
# 選擇的檔案，而調用的外部exe檔，同時會使用同資料夾內的jar檔。
# 寫出介面以及功能並不是問題，主要難處為我們要將這一份py檔，利用pyinstaller
# 打包為exe檔時。會發生外部exe檔一併複製到暫存位址，使得原py檔呼叫路徑不一致。
# 因此使用base_path函數，來將位址改為暫存位址。
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# 沒解決的問題：
# 1. 加密後的檔案，檔名為xxxx.TXT.enc，因有兩個副檔名，目前作者不知道怎麼呼叫
#    它，並將其由暫存資料夾複製到程式執行資料夾。
# (有使用shutil模組執行過，但因為檔名問題，程式判斷找不到該檔案)
# (其餘在暫存位址的檔案，都可以透過shutil成功複製)
# ---------------------------------------------------------------------


def SelectPath():
    # 設定存檔位置
    # 在此將Route變數，作為檔案路徑的值，並使用global，讓函數外可以呼叫到這一個值
    global Route
    # 使用tkinter模組功能
    Route = filedialog.askopenfilename()
    # 為避免原本待輸入欄位有數值，我們在植入資料前先將空格資料刪除
    entry_1.delete(0, 'end')
    entry_1.insert(0, Route)
    pass

def base_path(path):
    # 我們會將這隻程式打包，所調用的外部exe檔以及jar檔，會被同步複製到暫存空間，使得和原本程式寫的路徑不一樣
    # 因此我們使用這一個function，來取的這一個暫時的路徑
    # 此段引用自Python自學聖經(第二版)：從程式素人到開發強者的技術與實戰大全(電子書)
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)
    return os.path.join(basedir, path)

def Encrypt():
    # 調用外部exe檔，執行加密的function
    # Route_Divide將原本取得的檔案位址分割，我們只要檔名的部分，分割後取其最後一個值並命名為File_Name
    Route_Divide=Route.split('/',)
    File_Name=Route_Divide[-1]

    # 若沒有執行下方步驟變換路徑，則因為py檔打包為exe問題，會找不到調用的外部程式
    release_route = base_path('') # 這是解壓路徑
    current_route = os.getcwd() # 這是程序的所在路徑
    os.chdir(release_route) # 先把工作路徑變成解壓路徑

    # 使用win32api模組，請他執行外部程式參數位置及意義依序為
    # (父視窗控制代碼沒有則為0, 執行動作, 想執行的程式, 想用該程式開啟的檔案, 程式初始化目錄, 是否在前臺開起)
    # 我們使用下列函數，來調用外部「enc.exe」這個加密檔，並請他加密File_Name這一個檔案。
    win32api.ShellExecute(0, 'open', 'enc.exe', File_Name, '', 1)      # 前臺開啟

    # 加密完成，請系統打開加密完檔案的所在資料夾
    os.startfile(release_route)
    pass


# 使用TK模組，建立一個主要視窗，並設定標題、尺寸以及背景顏色
window = tk.Tk()
window.title('加密介面')
window.geometry('410x100')
window.configure(background='white')

# 在主視窗中，建立一個框架，每建立一個物件須使用pack、grid或place來放置完成
frame_1 = tk.Frame(window)
frame_1.pack(side=tk.TOP)

# 在我們建立的Frame中，將標題、輸入欄位及按鈕放置進去，並設置參數。
label_1 = tk.Label(frame_1, text='檔案位址：')
label_1.pack(side=tk.LEFT,padx=5,pady=30)   #padx為設置物件橫向間隔、pady為設置物件垂直間隔

entry_1 = tk.Entry(frame_1)
entry_1.pack(side=tk.LEFT,padx=5,pady=30)

# 設立第一個按鈕，點選後會自動執行「SelectPath」這一個function
Click__1 = tk.Button(
    frame_1, text="選擇檔案", fg="black", command=SelectPath)
Click__1.pack(side=tk.LEFT,padx=5,pady=30)

# 設立第二個按鈕，點選後會自動執行「Encrypt」這一個function
Click__2 = tk.Button(
    frame_1, text="開始加密", fg="black", command=Encrypt)
Click__2.pack(side=tk.LEFT,pady=5)

# 使視窗一直顯示，須加上這一段程式碼
window.mainloop()
