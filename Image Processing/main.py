from tkinter import *
import scipy.misc as sm
import cv2
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from Susan import Susan
from Fourier import Fourier
from contraste import  *
from skimage import data
from skimage.color import rgb2gray


class MainWindow():
    def __init__(self, main):
        # first Frame
        main.config(background="#F3C007")
        main.geometry('700x600')
        self.menubar = Menu(main)
        main.config(menu=self.menubar)
        frame_left = Frame(width=100, height=300, relief=SOLID,bd=3)
        frame_right = Frame(relief=SOLID,bd=3)
        top_frame = Frame(frame_left)

        label = Label(top_frame, text="Contrast")
        label.grid(row = 0, column = 0, sticky = W, pady = 2)

        self.w2 = Scale(top_frame, name="contrast",from_=0, to=255, length=300, tickinterval=20, orient=HORIZONTAL )
        self.w2.set(23)
        self.w2.grid(row = 0, column = 1,)

        label = Label(top_frame, text="brightness")
        label.grid(row = 1, column = 0, sticky = W, )

        self.w1 = Scale(top_frame, name="brightness", from_=0, to=255*2, length=300,  tickinterval=40, orient=HORIZONTAL)
        self.w1.set(23)
        self.w1.grid(row = 1, column = 1, sticky = W, pady = 2)

        Button(top_frame, text='Show',width=20, height=1, bg='black' ,fg='white',activebackground='#345',activeforeground='white', padx=5, pady=5,command=self.show_values).grid(row=2,column=1)

        top_frame.pack(side=TOP, anchor=NW,padx=50, pady=0)
        # canvas for image left image
        self.widthLeftFrame=500
        self.heightLeftFrame=450
        self.input_left = Label(frame_left, text="input image", font=("Helvetica", 12))
        self.canvas = Canvas(frame_left, width=self.widthLeftFrame, height=self.heightLeftFrame)
        self.canvas.pack()

        
        self.image = ""

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image((self.widthLeftFrame / 2), (self.heightLeftFrame / 2), anchor=CENTER, image=self.image)

        # button to change image right
        self.button = Button(frame_left, text="Choose ...", height=2, width=40, bg="#F3C007", command=self.onButton)
        self.button.pack()
        self.input_left.place(x=20, y=20)
        self.input_left.pack()

        # file path & init
        self.file_path = "images/susan_input1.png"

        # seconde frame
        # save the right image
        # canvas for image
        # width and the hight of canvas
        self.savedImage=""
        self.widthRightFrame=500
        self.heightRightFrame=450
        self.input_right = Label(frame_right, text="output image", font=("Helvetica", 12))
        self.label_right = Label(frame_right)
        self.canvas_right = Canvas(frame_right, width=self.widthRightFrame, height=self.heightRightFrame)
        self.canvas_right.grid(row=1, column=3)
        self.input_right.grid(row=3, column=3)
        self.image_right = PhotoImage(file="")

        # set first image on canvas
        self.image_on_canvas_right = self.canvas_right.create_image((self.widthRightFrame / 2), (self.heightRightFrame / 2), anchor=CENTER, image=self.image_right)
        self.saveButton = Button(frame_right, text="Save", height=2, width=20, bg="#F3C007",command=self.saveImageOnHard)
        self.saveButton.grid(row=2, column=3)
        frame_left.pack(side=LEFT, padx=100, pady=5)
        frame_right.pack(side=RIGHT, padx=50, pady=5)

        ## filtre pass haut or hight filter
        self.menuFiltreHaut()

        ## low filter menu
        self.passBas()

        ## bruit menu or blur menu save
        self.bruitMenu()

        ## operation elementaire or additional operation
        self.transElem()

        ## morph Maths
        self.morphologyMaths()

        ## susan
        self.edges()

        ## Fast Fourier Transform FFT
        self.fft()

    def onButton(self):
        self.callToSelect()
        self.canvas.itemconfig(self.image_on_canvas, image=self.image)

    def show_values(self):
        img = self.read()
        new = BrightnessContrast(img,self.w1.get(),self.w2.get())
        self.saveToRight(new)
    # read image and return it
    def read(self):
        path = self.file_path
        imgcv = cv2.imread(path, 1)
        imgcv = cv2.cvtColor(imgcv, cv2.COLOR_BGR2GRAY)
        height, width = 400, 450
        imgcvr = cv2.resize(imgcv, (round(width), round(height)), interpolation=cv2.INTER_AREA)
        return imgcvr

    def saveToRight(self, imagecv):
        imagecv = cv2.resize(imagecv, (round(self.widthRightFrame), round(self.heightRightFrame)), interpolation=cv2.INTER_AREA)
        img = Image.fromarray(imagecv)
        self.savedImage = imagecv # in case of saved image on your hard with open cv goto saveImageOnHard() function
        img = ImageTk.PhotoImage(img)
        self.image_right = img
        self.canvas_right.itemconfig(self.image_on_canvas_right, image=self.image_right)

    def callToSelect(self):
        width = self.widthLeftFrame
        height = self.heightLeftFrame
        filepath = filedialog.askopenfilenames(
            title="Choose a file",
            filetypes=[
                ('image files', '.png')
            ])
        self.file_path = filepath [0]
        img_right = Image.open(filepath [0])
        img_right = img_right.resize((width, height), Image.ANTIALIAS)
        photoImg_right = ImageTk.PhotoImage(img_right)
        self.image = photoImg_right
    
    def save(self):
        print("salam")
    
    def saveImageOnHard(self):
        img= self.savedImage
        cv2.imwrite("output/yourImageSaved.png",img)


    ### -------------------------------- high pass filtres------------------------------##
    def menuFiltreHaut(self):
        menuFiltre2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Filtre pass haut", menu=menuFiltre2)
        menuFiltre2.add_command(label="Gradient", command=self.gradient)
        menuFiltre2.add_command(label="Laplacian", command=self.laplacian)
        menuFiltre2.add_command(label="Kirsch", command=self.kirsch)
        menuFiltre2.add_command(label="Sobel", command=self.sobel)
        menuFiltre2.add_command(label="Prewitt", command=self.prewitt)
        menuFiltre2.add_command(label="Poberts", command=self.roberts)
        menuFiltre2.add_command(label="Canny", command=self.canny)

    def gradient(self):
        img = self.read()
        newImg = cv2.Sobel(np.float32(img), cv2.CV_8U, 1, 1, ksize=1)
        self.saveToRight(newImg)

    def laplacian(self):
        img = self.read()
        kernel = np.array(
            [
                [0, 1, 0],
                [1, -4, 1],
                [0, 1, 0]
            ])
        laplacian = ndimage.convolve(img, kernel)
        #laplacian = cv2.Laplacian(img, cv2.CV_64F) #with opencv
        self.saveToRight(laplacian)

    def kirsch(self):
        img = self.read()
        kernel = np.array(
            [
                [-3, -3, -3],
                [5, 0, -3],
                [5, 5, -3]
            ])
        kirsh = ndimage.convolve(img, kernel)
        self.saveToRight(kirsh)

    def SP(self,c):
        img = self.read()

        hs1 = np.array(
            [
                [1, c, 1],
                [0, 0, 0],
                [-1, -c, -1]
            ])
        hs2 = np.array(
            [
                [1, 0, 1],
                [c, 0, c],
                [1, 0, 1]
            ])
        abs1 = np.abs(ndimage.convolve(img, hs1))
        abs2 = np.abs(ndimage.convolve(img, hs2))
        image = abs1 + abs2
        self.saveToRight(image)
    def sobel(self):
        self.SP(2)

    def prewitt(self):
        self.SP(1)

    def roberts(self):
        img = self.read()

        hs1 = np.array(
            [
                [0, -1],
                [1, 0]
            ])
        hs2 = np.array(
            [
                [-1, 0],
                [0, 1]
            ])
        abs1 = np.abs(ndimage.convolve(img, hs1))
        abs2 = np.abs(ndimage.convolve(img, hs2))
        image = abs1 + abs2
        self.saveToRight(image)

    def canny(self):
        img = self.read()
        edges = cv2.Canny(img, 100, 200)
        self.saveToRight(edges)
        ### -------------------------------- low pass filters------------------------------##
    def passBas(self):
        menuFiltre1 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Filtre pass bas", menu=menuFiltre1)
        menuFiltre1.add_cascade(label="Bilateral Filter", command=self.bilaterale)
        menuFiltre1.add_command(label="Moyenneur", command=self.ImageMoyenne)
        menuFiltre1.add_command(label="Median", command=self.FiltreMedian)
        menuFiltre1.add_command(label="Gaussien 3x3", command=self.FGaussien)

    def FiltreMedian(self):
        img = self.read()
        temp = np.zeros(9)
        for i in range(1, img.shape [0] - 1):
            for j in range(1, img.shape [1] - 1):
                temp [0] = img [i - 1] [j - 1]
                temp [1] = img [i - 1] [j]
                temp [2] = img [i - 1] [j + 1]
                temp [3] = img [i] [j - 1]
                temp [4] = img [i] [j]
                temp [5] = img [i] [j + 1]
                temp [6] = img [i + 1] [j - 1]
                temp [7] = img [i + 1] [j]
                temp [8] = img [i + 1] [j + 1]
                img [i] [j] = self.trier(temp)
        self.saveToRight(img)

    def trier(self,t):
        for i in range(0, t.shape [0] - 1):
            for j in range(1, t.shape [0]):
                if (t [i] > t [j]):
                    f = t [i]
                    t [i] = t [j]
                    t [j] = f
        return t [4]

    def FGaussien(self):
        img = self.read()
        kernel = (1/16)*np.array(
            [
                [1, 2, 1],
                [2, 4, 2],
                [1, 2, 1]
            ])
        pass_3x3 = ndimage.convolve(img, kernel)
        self.saveToRight(pass_3x3)

    # filter average
    def ImageMoyenne(self):
        img = self.read()
        kernel = (1/9)*np.ones((3,3))
        print(kernel)
        lowpass_3x3 = ndimage.convolve(img, kernel)
        #newImg = cv2.blur(img, (3, 3)) with open cv
        self.saveToRight(lowpass_3x3)

    def bilaterale(self):
        img = self.read()
        blur = cv2.bilateralFilter(img, 9, 75, 75)
        self.saveToRight(blur)

    # ---------------------- some blur ----------------#
    def bruitMenu(self):
        menuBruit = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Bruit", menu=menuBruit)
        menuBruit.add_command(label="Poiver et sel ", command=self.poivreAndSel)
        menuBruit.add_command(label="Gaussien", command=self.gaussianNoise)

    def poivreAndSel(self):
        image = self.read()
        # row,col,ch = image.shape
        s_vs_p = 0.5
        amount = 0.04
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)  # prendre la partie entier
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        out [coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        out [coords] = 0
        self.saveToRight(out)

    def gaussianNoise(self):
        #img = self.read()
        img = cv2.imread(self.file_path, 1)
        img = cv2.resize(img, (400, 350))
        row, col, ch = img.shape
        mean = 0
        var = 0.1
        sigma = var ** 0.1
        gauss = np.random.normal(mean, sigma, img.shape)
        gauss = gauss.reshape(row, col, ch)
        noisyImage = img + gauss
        noisyImage = rgb2gray(noisyImage)
        self.saveToRight(noisyImage)

    # ------------------------------- transformation elementary ----------------+----------#
    def transElem(self):
        menuTransformation = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Transformation élémentaire", menu=menuTransformation)
        menuTransformation.add_command(label="Niveau de grais", command=self.NiveauGray)
        menuTransformation.add_command(label="seuillage ", command=self.seuillage3d)
        menuTransformation.add_command(label="Miroir Vertical", command=self.inverseParColon)
        menuTransformation.add_command(label="Miroir horizontal", command=self.inverseParLinge)
        menuTransformation.add_command(label="Histogramme", command=self.hist)

    # gray image
    def NiveauGray(self):
        image = self.read()
        self.saveToRight(image)

    def seuillage3d(self):
        img = self.read()
        img = cv2.split(img) [0]
        (retVal, newImg) = cv2.threshold(img, 147, 255, cv2.THRESH_BINARY)
        self.saveToRight(newImg)

    # mirror with column
    def inverseParColon(self):
        img = self.read()
        flipVertical = cv2.flip(img, 0)
        self.saveToRight(flipVertical)

    # mirror with line
    def inverseParLinge(self):
        img = self.read()
        img_rotate_90_counterclockwise = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.saveToRight(img_rotate_90_counterclockwise)

    def hist(self):
        img = cv2.imread(self.file_path, 1)
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(histr, color=col)
            plt.xlim([0, 256])
        plt.savefig("toto.png")
        img = cv2.imread("toto.png")
        self.saveToRight(img)
        plt.close()

    def convertColor(self):
        img = self.read()
        convertedImage = 255 - img
        self.saveToRight(convertedImage)
        
    # ------------------------------------- morphology Mathematics ------------------------------#
    def morphologyMaths(self):
        Morphologie = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Morphologie mathématiques", menu=Morphologie)
        Morphologie.add_command(label="Erosion", command=self.erosion)
        Morphologie.add_command(label="Dilatation", command=self.delation)
        Morphologie.add_command(label="Ouverture", command=self.ouverture)
        Morphologie.add_command(label="Fermeture", command=self.fermeture)
        Morphologie.add_command(label="white top hat", command=self.whiteTopHat)
        Morphologie.add_command(label="Black top Hat", command=self.blackTopHat)
        Morphologie.add_command(label="Gradien Morphplogy", command=self.gradientMorph)
        Morphologie.add_command(label="Conteur interieur", command=self.contorIn)
        Morphologie.add_command(label="Conteur exterieur", command=self.contorEx)

    def erosion(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(img, kernel, iterations=1)
        self.saveToRight(img_erosion)

    def delation(self):
        img = self.read()
        # Taking a matrix of size 5 as the kernel 
        kernel = np.ones((5, 5), np.uint8)
        img_dilation = cv2.dilate(img, kernel, iterations=1)
        self.saveToRight(img_dilation)

    # opening
    def ouverture(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_dilation = cv2.dilate(img, kernel, iterations=1)
        img_erosion = cv2.erode(img_dilation, kernel, iterations=1)
        self.saveToRight(img_erosion)

    # closing
    def fermeture(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(img, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=1)
        self.saveToRight(img_dilation)

    def whiteTopHat(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_dilation = cv2.dilate(img, kernel, iterations=1)
        ouverture = cv2.erode(img_dilation, kernel, iterations=1)
        imageWhileTopHat = img - ouverture
        self.saveToRight(imageWhileTopHat)

    def blackTopHat(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(img, kernel, iterations=1)
        fermeture = cv2.dilate(img_erosion, kernel, iterations=1)
        imageBlackTopHat = fermeture - img
        self.saveToRight(imageBlackTopHat)

    def gradientMorph(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
        self.saveToRight(gradient)

    # inside contor
    def contorIn(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_erosion = cv2.erode(img, kernel, iterations=1)
        conteurIn = img - img_erosion
        self.saveToRight(conteurIn)

    # Outside contor
    def contorEx(self):
        img = self.read()
        kernel = np.ones((5, 5), np.uint8)
        img_dilation = cv2.dilate(img, kernel, iterations=1)
        conteurIn = img_dilation - img
        self.saveToRight(conteurIn)

    # ---------------------------------------detection of susan  ----------------------------#
    def edges(self):
        detection = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Detection edge", menu=detection)
        detection.add_command(label="Susan", command=self.susanFunction)
        detection.add_command(label="Hariss", command=self.harris)


    def susanFunction(self):
        s = Susan(self.file_path)
        img = s.call()
        self.saveToRight(img)

    def harris(self):
        filename = self.file_path
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        # result is dilated for marking the corners, not important
        dst = cv2.dilate(dst, None)
        # Threshold for an optimal value, it may vary depending on the image.
        img [dst > 0.01 * dst.max()] = [0, 0, 255]
        self.saveToRight(img)

    # --------------------------------------TFF---------------------------------------------#
    def fft(self):
        fft = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="FFT", menu=fft)
        fft.add_command(label="Magnitude Spectru", command=self.mangnitudeSpec)
        fft.add_command(label="High Pass Filter (HPF)", command=self.fftHighPass)
        fft.add_command(label="Low Pass Filter (LPF)", command=self.LowPass)
        fft.add_command(label="Band Pass Filter (BPF)", command=self.bondPass)

    def mangnitudeSpec(self):
        img = self.read()
        f = np.fft.fft2(img)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift))
        self.saveToRight(magnitude_spectrum)

    def fftHighPass(self):
        f = Fourier(self.file_path)
        f.highPass()

    def LowPass(self):
        f = Fourier(self.file_path)
        f.lowPass()

    def bondPass(self):
        f = Fourier(self.file_path)
        f.bondPass()

    # ----------------------------------------------------------------------


root = Tk()
MainWindow(root)
root.mainloop()
