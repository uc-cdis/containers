FROM quay.io/cdis/nginx:1.17.6-ctds-1.0.1
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
STOPSIGNAL SIGTERM
CMD nginx-debug -g 'daemon off;'
