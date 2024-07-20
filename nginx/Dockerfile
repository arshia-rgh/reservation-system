# Fetching the latest nginx image
FROM nginx

# Removing default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

# Copying new conf.d into conf.d nginx image
COPY nginx.conf /etc/nginx/conf.d