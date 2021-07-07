FROM mysql:8.0.25


#COPY ./my.cnf /etc/mysql/my.cnf
COPY ./init.sql /docker-entrypoint-initdb.d
COPY ./src /src

WORKDIR "/src"
CMD ["chmod","+x" ,"./src/create_user.sh"]
CMD ["./src/create_user.sh"]

EXPOSE 3306
