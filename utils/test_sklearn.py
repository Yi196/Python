# from sklearn import linear_model
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import PolynomialFeatures
#
#
# epoch = [30,30,100,100,30,100,30,30,30,30,30,50,100,100,30,50,100,50,30,30,100,60,30,60,30,30,30,200,100,10,100,50, 100,100, 100, 100 , 70, 100,99,10,20,10,5,20,30,20,100,300,100]
# image_num = [25,25,346,24,42,24,24,42,4289,42,30,201,577,4289,4289,201,577,201,42,577,7,7,25,25,25,25,4289,10000,10000,5000,35,100, 250,250,250, 500, 314, 30,30,100,100,100,50,30,50,97,5000,5000,5000]
# image_quality = [1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1, 1, 1,1, 1, 1, 1,1,1,1,1,1,1,1,1,1,1,1,1]
# time = [3,3,11,4,3,5,3,4,120, 4,3, 6, 45, 118,120,6,43,5,5,47,4,4,4,4,2,2,118,420, 240, 30, 4,7, 14,13,14, 26, 13, 5, 6,2,3,2,2,2,3, 4, 135,380, 140]
# # print(len(epoch), len(image_num), len(time))
#
# x = [[i,j,z] for i,j,z in zip(epoch, image_num, image_quality)]
# y = [[i] for i in time]
#
# # 线性回归
# model = linear_model.LinearRegression()
# model.fit(x, y)
#
# x_ = [[100, 500, 1]]
# y_pred = model.predict(x_)
#
# print('线性回归 y_pred:', y_pred)
#
# # 查看w和b的
# print("w值为:", model.coef_)
# print("b截距值为:", model.intercept_)
#
# print('*****************************************************************')
# print()
# # 多项式回归
# poly_reg = Pipeline([
#     ("poly", PolynomialFeatures(degree=2)),
#     ("std_sclar", StandardScaler()),
#     ("lin_reg", LinearRegression())
# ])
#
# poly_reg.fit(x, y)
# y_predict = poly_reg.predict(x_)
# print('多项式回归 y_predict:', y_predict)
#
#
# print('########################################################################')
# print()
# # 非线性回归
# # 变为 y = theta0 + theta1 * x + theta2 * x^2 + theta3 * x^3
# poly_reg = PolynomialFeatures(degree=2)
# # 特征处理
# x_ploy = poly_reg.fit_transform(x)  # 这个方法实质是把非线性的模型转为线性模型进行处理，
# print(poly_reg.fit_transform([[3,7,11]]))
# # 处理方法就是把多项式每项的样本数据根据幂次数计算出相应的样本值
#
# # 训练线性模型（其本质是非线性模型，是由非线性模型转换而来）
# lin_reg_model = LinearRegression()
# lin_reg_model.fit(x_ploy, y)
# print(lin_reg_model.coef_)
# print(lin_reg_model.intercept_)
#
# y_predict = lin_reg_model.predict(poly_reg.fit_transform(x_))
# print('非线性回归 y_predict:', y_predict)
#
# import joblib
# #lr是一个LogisticRegression模型
# joblib.dump(lin_reg_model, 'lr.model')
#
#
#
# import joblib
# import numpy as np
# from sklearn.preprocessing import PolynomialFeatures
#
# def predict_train_time(epoch, img_num, img_quality=1):
#     x_ = np.asarray([[epoch, img_num, img_quality]])
#     lr = joblib.load('lr.model')
#     poly_reg = PolynomialFeatures(degree=2)
#     y_pred = lr.predict(poly_reg.fit_transform(x_))[0][0]
#     print(y_pred)
#     y_pred = 4 if y_pred < 4 else y_pred
#     return np.ceil(y_pred)
#
# if __name__ == '__main__':
#     print(predict_train_time(100, 500))

e = 100  # 训练轮次epoch
n = 5000  # 图片数量img_num
q = 1    # 图片质量1、2... 默认为1

y = 1 * 0 + e * (-4.28922271e-03) + n * (-4.06531023e-02) + q * (1.76087713e-04) + e*e * (1.30815437e-03) + e*n * (1.53243277e-04) + e*q * (-1.48524680e-01) + n*n * (-1.20842533e-06) + n*q * (6.09495083e-02) + q*q * (5.28263140e-04) + 5.73113943
print(y)