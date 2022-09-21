
# 创建Docker镜像
# 指定基础镜像
FROM python:3.8-slim

# 指定之后所有命令的工作路径(没有会创建)
WORKDIR /app

# COPY <本地路径> <目标路径> 将文件拷贝到docker镜像中的路径(/app)
COPY . .

# RUN 在创建镜像时运行的shell命令
RUN pip install -r requirements.txt


# 运行Docker镜像
# CMD["可执行文件","参数1","参数2"...] 指定Docker容器运行起来后执行的命令
CMD ["python", "-m", "test.py"]




# 可使用以下命令创建Docker镜像
# docker build -t docker_test:python .
             # -t 指定镜像名称     . dockelfile所在目录
# docker run --name test_container -p 80:5000 -d docker_test:python
           # --name 指定容器名称     -p 将主机端口80 映射到docker容器端口5000  -d 后台运行  镜像名称(在哪个镜像的基础上创建容器) --rm 容器终止后直接删除

# 进入正在运行的容器
# docker exec -it [container ID] bash

# 创建数据卷保存容器中的数据
# docker volume create docker_test_data
# docker run -p 80:5000 -v docker_test_data:/etc/docker_test_data -d docker_test
                      # -v  指定将数据卷docker_test_data挂载到/etc/docke_test_data


# 导出容器
# docker export [container ID] > ubuntu.tar(文件名)
# 导入容器
# cat ubuntu.tar | docker import - test/ubuntu:v1.0