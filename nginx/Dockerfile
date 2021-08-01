FROM nginx:1.21.1-alpine
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/
COPY ${SSL_KEY} /etc/ssl/capstone-np-selfsigned.key
COPY ${SSL_CRT} /etc/ssl/capstone-np-selfsigned.crt
