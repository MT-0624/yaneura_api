mysql -uroot -p$MYSQL_ROOT_PASSWORD --skip-column-names <<EOF
create
    user 'analyzer'@'%' identified by '${ENGINE_USER_PASSWORD}';
create
    user 'api'@'%' identified by '${API_USER_PASSWORD}';


grant execute on procedure kishin_service.insert_request to
    'api'@'%';
grant
    select,
        update
        on kishin_service.Boards to 'analyzer'@'%';
EOF