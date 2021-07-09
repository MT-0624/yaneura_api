FROM mysql:8.0.25


#COPY ./my.cnf /etc/mysql/my.cnf
COPY ./init.sql /docker-entrypoint-initdb.d
COPY ./src /src

#
#CMD ["sudo","chmod","+x" ,"/src/create_user.sh"]
#CMD ["/src/create_user.sh"]

#CMD ["sudo","chmod","+x" ,"/src/python_setup.sh"]
#RUN "/src/python_setup.sh"


EXPOSE 3306
