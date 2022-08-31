
# 创建Docker镜像
# 指定基础镜像
FROM python:3.8-slim-buster

# 指定之后所有命令的工作路径(没有会创建)
WORKDIR /app

# COPY <本地路径> <目标路径> 将文件拷贝到docker镜像中的路径(/app)
COPY . .

# RUN 在创建镜像时运行的shell命令
RUN pip install -r requirements.txt


# 运行Docker镜像
# CMD["可执行文件","参数1","参数2"...] 指定Docker容器运行起来后执行的命令
CMD ['python', '-m', 'test.py']




# 可使用以下命令创建Docker镜像
# docker build -t docker_test .
             # -t 指定名称     . dockelfile目录
# docker run -p 80:5000 -d docker_test
           # -p 将主机端口80 映射到docker容器端口5000  -d 后台运行  容器名称

# 创建数据卷保存容器中的数据
# docker volume create docker_test_data
# docker run -p 80:5000 -v docker_test_data:/etc/docker_test_data -d docker_test
                      # -v  指定将数据卷docker_test_data挂载到/etc/docke_test_data
