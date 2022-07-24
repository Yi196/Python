class Car :
    def __init__(self,car_no,car_type):
        self.car_no=car_no
        self.car_type=car_type
    def star(self):
        pass
    def end(self):
        pass

class Taxi(Car):
    def __init__(self,no,type,company):
        super().__init__(no,type)
        self.company=company
    def star(self):
        print(f"欢迎乘坐{self.car_no},{self.company}为你服务，祝你旅途愉快！")
    def end(self):
        print(f"{self.company}公司期待你的下次乘坐！")

class Family_car(Car):
    def __init__(self,no,type,name):
        super().__init__(no,type)
        self.name=name
    def star(self):
        print(f"我是{self.name},我要开着我的{self.car_type}带家人去兜风了。")
    def end(self):
        print("孩子们玩的开心！")

if __name__ == '__main__':
    a=Taxi("豫S A682","福特","嘀嘀打车")
    b=Family_car("鄂A 7883","特斯拉","张三")
    a.star()
    a.end()
    b.star()
    b.end()