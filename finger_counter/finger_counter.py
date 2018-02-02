from keras.models import load_model
import numpy as np
import cv2


class FingerCounter:

    def __init__(self, model='finger_counter/model_6cat.h5', show_binary=False):
        self._model = load_model(model)
        self._classes = [None, 1, 2, 3, 4, 5]
        self._show_binary = show_binary

    def _binary_mask(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.uint8(img)
        img = cv2.GaussianBlur(img, (7, 7), 3)
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        ret, new = cv2.threshold(img, 25, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return new

    def count(self, img):
        """Count number of fingers in an image."""
        y0 = 100
        x0 = 100
        width = 300
        img = img[y0:y0 + width, x0:x0 + width]
        img = self._binary_mask(img)
        img = np.float32(img) / 255  # Normalize
        img = np.expand_dims(img, axis=0)
        img = np.expand_dims(img, axis=-1)
        if self._show_binary:
            cv2.imshow("WINDOW 3", img[0, ..., 0])
        prediction = self._classes[np.argmax(self._model.predict(img)[0])]
        return prediction
