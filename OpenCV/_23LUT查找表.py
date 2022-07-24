import cv2 as cv
import numpy as np

# 使用opencv提供的所有颜色查找表进行颜色变换
cv2_luts = [lut for lut in dir(cv) if lut.startswith("COLORMAP_")]
print(f"opencv lut colormap number: {len(cv2_luts)}")
print(f"opencv luts colormap: {cv2_luts}")


print("cv.COLORMAP_COOL", type("cv.COLORMAP_COOL",))
print(eval("cv.COLORMAP_COOL"), type(eval("cv.COLORMAP_COOL")))


image = cv.imread('./image/005.jpg')
all_lut_imgs = [(lut, cv.applyColorMap(image, eval("cv."+lut))) for lut in cv2_luts]


add_text_imgs = [cv.putText(lut_img[1], lut_img[0], (20, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) for lut_img in all_lut_imgs]


col1 = np.vstack(tuple(add_text_imgs[0:11]))
col2 = np.vstack(tuple(add_text_imgs[11:22]))
result = np.hstack((col1, col2))
# cv.imwrite("lut_result.jpg", result)
cv.imshow("result", result)
cv.waitKey(0)


# 使用查找表给灰度图添加为彩色
image = cv.imread("./image/002.jpg")
print(image.shape)
image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
print(image.shape)
# cv.imwrite("canjian_gray.png", image)
color_image = cv.applyColorMap(image, cv.COLORMAP_JET)
cv.imshow("image", image)
cv.imshow("color_image", color_image)
cv.waitKey(0)
cv.destroyAllWindows()