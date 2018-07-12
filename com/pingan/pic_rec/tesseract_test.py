import pytesseract
from PIL import Image
import cv2



def resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    h, w = img.shape[:2]
    if width is None and height is None:
        return img
    if width is None:
        r = height / height
        dim = (int(w * r), height)
    else:
        r = width / w
        dim = (width, int(h * r))

    resized = cv2.resize(img, dim, interpolation=inter)
    return resized


if __name__ == '__main__':

    pic_file = r'./template/e24345d5f8df9bb699a817d64a79347d239818.jpg'

    img_source = cv2.imread(pic_file)
    img_source = resize(img_source, 800)

    img_gray = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.GaussianBlur(img_gray, (3,3), 1.5)
    _, img_threshold = cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY)

    # img_threshold = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,3,2)

    cv2.imshow('source', img_source)
    cv2.imshow('img_threshold', img_threshold)

    img = Image.fromarray(img_threshold)

    # text = pytesseract.image_to_string(img, 'chi_sim')

    # print(text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()