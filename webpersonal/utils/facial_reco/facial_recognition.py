import numpy as np
import mediapipe as mp
import cv2
import os
from statistics import mode

class facialRecognition:

    def __init__(self, dataPath) -> None:
        self.dataPath = dataPath
        try:
            self.dir_list = os.listdir(self.dataPath) #Carpetas dentro del path (usuarios)
        except:
            os.makedirs(self.dataPath)
            self.dir_list = os.listdir(self.dataPath) 
        print(self.dir_list)


    #Funcion para eliminar los archivos pares de los usuarios
    def removeFiles(self, user):
        ruta = f'{self.dataPath}/{user}'
        direccion = os.listdir(ruta)
        # Iterar sobre los archivos y eliminar los pares
        print(f'Eliminando algunos archivos de {user}...')
        for archivo in direccion:
            # Comprobamos si el archivo es un archivo de imagen y si su número es par
            if archivo.startswith(user) and archivo.endswith('.jpg') and archivo[len(user):-4].isdigit() and int(archivo[len(user):-4]) % 2 == 0:
                ruta_completa = os.path.join(ruta, archivo)
                os.remove(ruta_completa)


    #Metodo para generar imagenes de los rostros de los usuarios
    def recognize(self, num_fotos=200, user='user'):
        print("Hay un total de ", len(self.dir_list), " usuarios registrados")

        #Verificamos que no haya mas de 3 usuarios registrados para reducir procesamiento
        if len(self.dir_list) >= 3:
            print('Ha alcanzado el limite de usuarios registrados')
            eliminate = self.dir_list[2:]
            for user in eliminate:
                self.removedUser = user
                print('Eliminando usuario: ', user)
                for imagen in os.listdir(f'{self.dataPath}/{user}'):
                    os.remove(f'{self.dataPath}/{user}/{imagen}')
                os.rmdir(f'{self.dataPath}/{user}')
            return False

        mp_face_detection = mp.solutions.face_detection #Para detectar rostros
        output_folder = f'{self.dataPath}/{user}'

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        counter = 1

        # Inicializamos la camara
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        with mp_face_detection.FaceDetection(
            min_detection_confidence=0.5) as face_detection:

            while counter <= num_fotos:
                #Leemos la imagen de la camara: ret = True si se leyo correctamente y frame es la imagen
                ret, frame = cap.read()
                if ret == False: 
                    break
                frame = cv2.flip(frame, 1) #Volteamos la imagen horizontalmente
                height, width, _ = frame.shape # _ se usa para ignorar el color
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convertimos la imagen a RGB
                results = face_detection.process(frame_rgb) #Procesamos la imagen, usando un modelo para detectar caras

                if results.detections is not None: #Detectamos caritas
                    for detection in results.detections:
                        #Coordenadas de la carita detectada
                        #anchura minima del fotograma donde se detecta la cara, y se multiplica por el ancho de la imagen
                        xmin = int(detection.location_data.relative_bounding_box.xmin * width) 
                        ymin = int(detection.location_data.relative_bounding_box.ymin * height) #idem pa la altura
                        #anchura y altura de la cara detectada
                        w = int(detection.location_data.relative_bounding_box.width * width)
                        h = int(detection.location_data.relative_bounding_box.height * height)
                        if xmin < 0 and ymin < 0: #A veces xmin y ymin son negativos, no se por que pasa esto
                            continue
                        #Crea una rectangulo alrededor de la cara detectada, de color verde y de grosor 5
                        cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 5)
                        #Creamos una imagen con la cara detectada (dentro del rectangulo que detecta la cara)
                        face_image = frame[ymin : ymin + h, xmin : xmin + w]
                        #Si no se detecta la cara, continuamos para evitar que de error
                        if face_image.size == 0:
                            continue
                        #Convertimos la imagen a escala de grises(reducir el procesamiento de la imagen) y la redimensionamos a 72x72 pixeles
                        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                        face_image = cv2.resize(face_image, (72, 72), interpolation=cv2.INTER_CUBIC)
                        cv2.putText(frame, "loading... {}%".format(round(counter/(num_fotos/100))), (xmin, ymin - 5), 1, 1.3, (0, 255, 0), 1, cv2.LINE_AA)
                        #cv2.imshow("Face", face_image) #Mostramos la imagen redimensionada, en blanco y negro
                        
                        img = f'{user}{counter}.jpg'
                        ruta_imagen = os.path.join(output_folder, img)
                        cv2.imwrite(ruta_imagen, face_image)

                        counter += 1

                cv2.imshow("Frame", frame)
                k = cv2.waitKey(1)
                if k == 27: #Si le damos al escape (Esc) salimos del programa
                    break

        cap.release()
        cv2.destroyAllWindows()

        self.user = user

        return True
        


    #Metodo para entrenar las imagenes de los usuarios, utilizando un modelo (LBPHFaceRecognizer)
    def train(self):
        print("Lista archivos:", self.dir_list)

        labels = [] #Etiquetas asignadas a las imagenes
        facesData = [] #Rostros detectados
        label = 0 

        for name_dir in self.dir_list:
            dir_path = self.dataPath + "/" + name_dir
            
            for file_name in os.listdir(dir_path):
                image_path = dir_path + "/" + file_name
                #print(image_path)
                image = cv2.imread(image_path, 0)
                #cv2.imshow("Image", image)  #Para mostrar la imagen
                #cv2.waitKey(10) #Delay de 10 ms

                facesData.append(image)
                labels.append(label)
            label += 1

        for i in range(len(self.dir_list)):
            if np.count_nonzero(np.array(labels) == i) > 200:
                self.removeFiles(self.dir_list[i])
            print(self.dir_list[i] + ": ", np.count_nonzero(np.array(labels) == i)) #Numero de imagenes por usuario

        # LBPH FaceRecognizer
        face_reco = cv2.face.LBPHFaceRecognizer_create()

        # Eigen FaceRecognizer
        #face_reco = cv2.face.EigenFaceRecognizer_create()

        # Fisher FaceRecognizer
        #face_reco = cv2.face.FisherFaceRecognizer_create()

        # Entrenamiento
        print("Entrenando...")
        face_reco.train(facesData, np.array(labels))

        # Almacenar modelo
        face_reco.write("webpersonal/utils/facial_reco/LBPHFaceModel.xml")
        #face_reco.write("facial_reco/eigenFaceModel.xml")
        #face_reco.write("facial_reco/fisherFaceModel.xml")
        print("Modelo almacenado")


    
    def predict(self):
        mp_face_detection = mp.solutions.face_detection #Para detectar rostros
        LABELS = self.dir_list #usuarios que hemos entrenado

        # Leemos el modelo
        face_reco = cv2.face.LBPHFaceRecognizer_create()
        face_reco.read("webpersonal/utils/facial_reco/LBPHFaceModel.xml")


        #face_reco = cv2.face.EigenFaceRecognizer_create()
        #face_reco.read("facial_reco/eigenFaceModel.xml")

        #face_reco = cv2.face.FisherFaceRecognizer_create()
        #face_reco.read("facial_reco/fisherFaceModel.xml")

        # Inicializamos la camara
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        moda = [] # Futura lista con la que obtendremos la moda de los resultados del reconocimiento facial

        with mp_face_detection.FaceDetection(
            min_detection_confidence=0.5) as face_detection:

            while True:
                #Leemos la imagen de la camara: ret = True si se leyo correctamente y frame es la imagen
                ret, frame = cap.read()
                if ret == False: 
                    break
                frame = cv2.flip(frame, 1) #Volteamos la imagen horizontalmente
                height, width, _ = frame.shape # _ se usa para ignorar el color
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Convertimos la imagen a RGB
                results = face_detection.process(frame_rgb) #Procesamos la imagen, usando un modelo para detectar caras

                if results.detections is not None: #Detectamos caritas
                    for detection in results.detections:
                        #Coordenadas de la carita detectada
                        #anchura minima del fotograma donde se detecta la cara, y se multiplica por el ancho de la imagen
                        xmin = int(detection.location_data.relative_bounding_box.xmin * width) 
                        ymin = int(detection.location_data.relative_bounding_box.ymin * height) #idem pa la altura
                        #anchura y altura de la cara detectada
                        w = int(detection.location_data.relative_bounding_box.width * width)
                        h = int(detection.location_data.relative_bounding_box.height * height)
                        if xmin < 0 and ymin < 0: #A veces xmin y ymin son negativos, no se por que pasa esto
                            continue
                        #Crea una rectangulo alrededor de la cara detectada, de color verde y de grosor 5
                        #cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 5)
                        #Creamos una imagen con la cara detectada (dentro del rectangulo que detecta la cara)
                        face_image = frame[ymin : ymin + h, xmin : xmin + w]
                        #Si no se detecta la cara, continuamos para evitar que de error
                        if face_image.size == 0:
                            continue
                        #Convertimos la imagen a escala de grises(reducir el procesamiento de la imagen) y la redimensionamos a 72x72 pixeles
                        face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
                        face_image = cv2.resize(face_image, (72, 72), interpolation=cv2.INTER_CUBIC)
                        #cv2.imshow("Face", face_image) #Mostramos la imagen redimensionada, en blanco y negro

                        #Predecimos la imagen, para verificar al usuario
                        result = face_reco.predict(face_image)
                        #Ponemos texto alrededor del rectangulo, con el resultado de la prediccion
                        cv2.putText(frame, "{}".format(result), (xmin, ymin - 5), 1, 1.3, (210, 124, 176), 1, cv2.LINE_AA)
                        
                        #verde si detectamos al usuario y rojo si no 
                        if result[1] <= 140:
                            try:
                                color = (0, 255, 0) 
                                usuario = LABELS[result[0]]
                                print(usuario)
                                #ser.write(b'1')
                            except:
                                continue                              
                        else:
                            color = (0, 0, 255)
                            usuario = 'Desconocido'
                            #ser.write(b'2')

                        cv2.putText(frame, f"{usuario}", (xmin, ymin - 15), 2, 1, color, 1, cv2.LINE_AA) #Mostramos el usuario
                        cv2.rectangle(frame, (xmin, ymin), (xmin + w, ymin + h), color, 2) #Mostramos el rectangulo que detecta la cara
                        moda.append(usuario)

                cv2.imshow("Frame", frame)
                k = cv2.waitKey(1)
                if k == 27: #Si le damos al escape (Esc) salimos del programa
                    break

        cap.release()
        cv2.destroyAllWindows()
        #ser.close() #Cerramos el puerto serial

        self.prediction = mode(moda) #Obtenemos la moda de los resultados del reconocimiento facial



    def getPrediction(self):
        return self.prediction
    

    def getRemovedUser(self):
        return self.removedUser


'''
facialReco = facialRecognition("webpersonal/utils/facial_reco/DatasetFaces")
facialReco.recognize()
#facialReco.train()
facialReco.predict()
print(facialReco.getPrediction())
'''