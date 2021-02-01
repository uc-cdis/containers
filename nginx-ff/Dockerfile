FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
STOPSIGNAL SIGTERM
CMD nginx -g 'daemon off;'
