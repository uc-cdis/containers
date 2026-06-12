FROM nginx:1.31.1-trixie
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
STOPSIGNAL SIGTERM
CMD nginx -g 'daemon off;'
