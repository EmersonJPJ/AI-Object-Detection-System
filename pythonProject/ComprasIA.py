#Importar librerias
import cv2
from ultralytics import YOLO
import math

class TiendaIA:
    #Funcion Init
    def init(self):
        # VideoCapture
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 640)
        self.cap.set(4, 480)


        ObjectModel = YOLO('models/yolov8l.pt')
        self.ObjectModel = ObjectModel

        billModel = YOLO('models/billBank2.pt')
        self.billModel = billModel

        # CLASES:
        # Objects
        # clsObject = ObjectModel.names
        clsObject = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                     'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
                     'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard',
                     'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle',
                     'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
                     'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
                     'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
                     'scissors', 'teddy bear', 'hair drier', 'toothbrush']
        self.clsObject = clsObject

        # Bills Bank
        clsBillBank = ['Billete10', 'Billete20', 'Billete50']
        self.clsBillBank = clsBillBank

        # Total balance
        total_balance = 0
        self.total_balance = total_balance
        self.pay = ''

        return self.cap


    # Funcion del área
    def area(self,frame, xi, yi, xf, yf):
        # Informacion
        al,an,c= frame.shape

        # Coordenadas
        xi, yi = int(xi * an), int(yi * al)
        xf, yf = int(xf * an), int(yf * al)

        return xi, yi, xf, yf

    def linea_area(self, frame, color, xi, yi, xf, yf):
        img = cv2.rectangle(frame, (xi,yi), (xf, yf), color, 1, 1)
        return img

    def linea_texto(self, img, color, texto, xi, yi,tamanyo, grosor, back = False):
        tamanyo_texto = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, tamanyo, grosor)
        dim = tamanyo_texto[0]
        baseline = tamanyo_texto[1]
        if back == True:
            img = cv2.rectangle(img, (xi, yi - dim[1] - baseline), (xi + dim[0], yi + baseline - 7),(0,0,0), cv2.FILLED)

        img = cv2.putText(img, texto, (xi, yi - 5), cv2.FONT_HERSHEY_SIMPLEX, tamanyo, color, grosor)
        return img


    def lista_compras(self, frame, objeto):
        lista_productos = {'handbag': 30000, 'sports ball': 10000, 'bottle': 50000, 'cup': 30000, 'fork': 5000, 'knife': 5000, 'spoon': 5000,
                         'banana': 1000, 'apple': 1000, 'orange': 1000, 'broccoli': 500, 'carrot': 1000, 'mouse': 60000, 'keyboard': 100000,
                         'book': 40000, 'clock': 50000, 'scissors': 15000, 'toothbrush': 8000}

        lista_area_xi, lista_area_yi, lista_area_xf, lista_area_yf = self.area(frame, 0.7739, 0.6250, 0.9649, 0.9444)
        tamanyo_tienda, grosor_tienda = 0.60, 1

        if objeto == 'scissors' not in [item[0] for item in self.compra_lista]:
            precio = lista_productos['scissors']
            self.compra_lista.append([objeto, precio])

            #Mostrarlo en pantalla
            texto = f'{objeto} --> ${precio}'
            frame = self.linea_texto(frame, (0,128,255), texto, lista_area_xi + 10,
                                     lista_area_yi + (40 + (self.posicion_productos * 20)),
                                     tamanyo_tienda, grosor_tienda, back = False)
            self.posicion_productos += 1

            # Precio
            self.precio_acumulado = self.precio_acumulado + precio

        if objeto == 'fork' not in [item[0] for item in self.compra_lista]:
            precio = lista_productos['fork']
            self.compra_lista.append([objeto, precio])

            #Mostrarlo en pantalla
            texto = f'{objeto} --> ${precio}'
            frame = self.linea_texto(frame, (0,128,255), texto, lista_area_xi + 10,
                                     lista_area_yi + (40 + (self.posicion_productos * 20)),
                                     tamanyo_tienda, grosor_tienda, back = False)
            self.posicion_productos += 1

            # Precio
            self.precio_acumulado = self.precio_acumulado + precio
        return frame

    def proceso_balance(self, billete):
        if billete == 'Billete10':
            self.balance = 10000
        elif billete == 'Billete20':
            self.balance = 20000
        elif billete == 'Billete50':
            self.balance = 50000

    def proceso_pagar(self, precio_acumulado, balance_acumulado):
        pago = balance_acumulado - precio_acumulado
        print(pago)
        if pago < 0:
            texto = f'Falta cancelar {abs(pago)}$'
        elif pago > 0:
            texto = f'Su cambio es de {abs(pago)}$'
            self.precio_acumulado = 0
            self.total_balance = 0
        elif pago == 0:
            texto = f'Gracias por su compra'
            self.precio_acumulado = 0
            self.total_balance = 0
        return texto


    def predecir_modelo(self, frame_claro, frame, modelo, clase):
        bbox = []
        cls = 0
        conf = 0

        # Inferencia
        resultados = modelo(frame_claro, stream = True, verbose = False)
        for res in resultados:
            # Box
            boxes = res.boxes
            for box in boxes:
                # Extraer coordenadas
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Error < 0
                if x1 < 0:
                    x1 = 0
                if y1 < 0:
                    y1 = 0
                if x2 < 0:
                    x2 = 0
                if y2 < 0:
                    y2 = 0

                bbox = [x1, y1, x2, y2]

                # Clase
                cls = int(box.cls[0])

                conf = math.ceil(box.conf[0])

                if clase == 0:
                    objeto = self.clsObject[cls]
                    texto_objeto = f'{self.clsObject[cls]} {int(conf * 100)}'

                    tamanyo_objeto, grosor_objeto = 0.75, 1
                    frame = self.linea_texto(frame, (0,128,255), texto_objeto, x1, y1,tamanyo_objeto, grosor_objeto, back=True)
                    frame = self.linea_area(frame, (0,128,255), x1, y1, x2,y2)

                    # Lista de compras
                    frame = self.lista_compras(frame, objeto)

                if clase == 1:
                    billete = self.clsBillBank[cls]
                    texto_billete = f'{self.clsBillBank[cls]} {int(conf * 100)}'

                    tamanyo_billete, grosor_billete = 0.75, 1
                    frame = self.linea_texto(frame, (0,128,255), texto_billete, x1, y1,tamanyo_billete, grosor_billete, back=True)
                    frame = self.linea_area(frame, (0,128,255), x1, y1, x2,y2)

                    # Balance de saldo
                    self.proceso_balance(billete)

            return frame


    # Funcion principal
    def tiendaIA(self, cap):
        while True:
            ret, frame = cap.read()

            frame_claro = frame.copy()

            compra_lista = []
            self.compra_lista = compra_lista

            posicion_productos = 1
            self.posicion_productos = posicion_productos

            precio_acumulado = 0
            self.precio_acumulado = precio_acumulado

            balance = 0
            self.balance = balance

            #Areas en la pantalla
            #Area de compras
            tienda_area_xi,tienda_area_yi,tienda_area_xf,tienda_area_yf = self.area(frame, 0.0351, 0.0486, 0.7539, 0.9444)

            #Lineas de interfaz
            color = (0,128,255)
            texto_compras = 'Area de compras'
            tamanyo_tienda, grosor_tienda = 0.75, 1
            frame = self.linea_area(frame, color,tienda_area_xi,tienda_area_yi,tienda_area_xf,tienda_area_yf)
            frame = self.linea_texto(frame, color, texto_compras, tienda_area_xi, tienda_area_yi, tamanyo_tienda, grosor_tienda, back = True)

            #Área de pago
            pago_area_xi,pago_area_yi,pago_area_xf,pago_area_yf = self.area(frame, 0.7739, 0.0486, 0.9649, 0.6050)
            texto_pago = 'Area de pago'
            frame = self.linea_area(frame, color,pago_area_xi,pago_area_yi,pago_area_xf,pago_area_yf)
            frame = self.linea_texto(frame, color, texto_pago, pago_area_xi, pago_area_yi, tamanyo_tienda, grosor_tienda, back = True)


            #Área de lista
            lista_area_xi, lista_area_yi, lista_area_xf, lista_area_yf = self.area(frame, 0.7739, 0.6250, 0.9649, 0.9444)
            texto_lista = 'Lista de compras'
            frame = self.linea_area(frame, color, lista_area_xi, lista_area_yi, lista_area_xf, lista_area_yf,)
            frame = self.linea_texto(frame, color, texto_lista, lista_area_xi + 5, lista_area_yi + 30, tamanyo_tienda, grosor_tienda, back = True)

            # Predecir Objeto
            frame = self.predecir_modelo(frame_claro,frame, self.ObjectModel, clase = 0)
            # Predecir Billete
            frame = self.predecir_modelo(frame_claro,frame, self.billModel, clase = 1)


            # Mostrar precio acumulado
            texto_precio = f'Compra total: {self.precio_acumulado}$'
            frame = self.linea_texto(frame, (0,128,255), texto_precio, lista_area_xi + 10, lista_area_yf, 0.60, 1, back = True)

            # Mostrar Balance
            texto_balance = f'Saldo total: {self.total_balance}$'
            frame = self.linea_texto(frame, (0,128,255), texto_balance, lista_area_xi + 10, lista_area_yf + 30, 0.60, 1, back = True)

            # Pago
            frame = self.linea_texto(frame, (0,128,255), self.pay, lista_area_xi + - 300, lista_area_yi + 30, 0.60, 1, back = True)





            cv2.imshow('Compras IA', frame)

            # Leer teclas

            t = cv2.waitKey(5)

            # Balance
            if t == 8 or t == 115:
                self.total_balance = self.total_balance + self.balance
                self.balance = 0

            # Pago
            if t == 80 or t == 112:
                self.pay = self.proceso_pagar(self.precio_acumulado, self.total_balance)

            if t == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()






























