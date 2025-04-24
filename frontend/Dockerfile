FROM nginx:alpine

# 删除默认配置文件
RUN rm /etc/nginx/conf.d/default.conf

# 拷贝自定义配置和静态文件
COPY nginx.conf /etc/nginx/nginx.conf
COPY dist/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

