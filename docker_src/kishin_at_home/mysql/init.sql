drop
    database if exists kishin_service;

create
    database kishin_service;


use kishin_service;

create TABLE Boards
(
    board_id          int primary key,
    board             varchar(200),
    analyzer_id       int,
    request_datetime  datetime,
    analyzed_datetime datetime,
    eval_score        varchar(20),
    opinion           varchar(200)
);

create TABLE requests
(
    request_id       int primary key auto_increment,
    user_id          int,
    board_id         int,
    request_datetime datetime,
    required_time    int,
    required_node    int,
    required_depth   int,
    foreign key key_board_id (board_id) references Boards (board_id)
);

delimiter //


create procedure insert_request(
    IN _user_id int,
    IN _board varchar(200),
    IN _required_time int,
    IN _required_node int,
    IN _required_depth int
)

begin
    DECLARE
        search_id int;
    DECLARE
        new_id int;

    set
        search_id =
                (
                    select count(*)
                    from Boards
                    where _board = Boards.board
                );


    if
        search_id = 0 then
        -- 存在しなければ未解析レコードとして両テーブルに新規追加
        set new_id = (select count(*) from Boards)
            + 1;

        select concat("search_id:", search_id),
               concat("new_id:", new_id);

        insert into Boards(board_id,
                           board,
                           analyzer_id,
                           request_datetime,
                           analyzed_datetime,
                           eval_score,
                           opinion)
            value (
                   new_id,
                   _board,
                   null,
                   NOW(),
                   null,
                   null,
                   null
            );

        insert into requests(user_id,
                             board_id,
                             request_datetime,
                             required_time,
                             required_node,
                             required_depth)
            value (
                   _user_id,
                   new_id,
                   NOW(),
                   _required_time,
                   _required_node,
                   _required_depth
            );

    elseif
        search_id = 1 then
        -- すでに解析済みレコードが存在すれば解析済み
        insert into requests(user_id,
                             board_id,
                             request_datetime,
                             required_time,
                             required_node,
                             required_depth)
            value (
                   _user_id,
                   search_id,
                   NOW(),
                   _required_time,
                   _required_node,
                   _required_depth
            );

    end if;

end;
//
delimiter ;

delimiter //


create function task_mapper(
    _analyzer_id int
)
    returns varchar(200)

begin
    declare
        b_id int;

    select @b_id := board_id,
           @board_text := cast(board as char)
    from Boards
    where analyzer_id is null
    order by request_datetime desc
    limit 1;
    select b_id;

    if
        b_id is not null then
        update Boards
        set analyzer_id = _analyzer_id
        where board_id = b_id;
    end if;

    return @board_text;
end;
//
delimiter ;


create
    user 'analyzer'@'%' identified by "$(USI_ENGINE_PASSWORD)";
create
    user 'api'@'%' identified by "$(API_SERVICE_PASSWORD)";

grant execute on procedure kishin_service.insert_request to
    'api'@'%';
grant
    select,
        update
        on kishin_service.Boards to 'analyzer'@'%';