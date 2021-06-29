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
    requested_time   int,
    requested_node   int,
    requested_depth  int,
    foreign key key_board_id (board_id) references Boards (board_id)
);

delimiter //


create procedure insert_request(
    IN _user_id int,
    IN _board varchar(200),
    IN _requested_time int,
    IN _requested_node int,
    IN _requested_depth int
)

begin
    DECLARE search_id int;
    DECLARE new_id int;

    set search_id =
            (
                select count(*)
                from Boards
                where _board = Boards.board
            );


    if search_id = 0 then
        -- 存在しなければ未解析レコードとして両テーブルに新規追加
        set new_id = (select count(*) from Boards)
            + 1;

        select concat("search_id:", search_id),
               concat("new_id:", new_id);

        insert into Boards(board_id,
                           board, analyzer_id,
                           request_datetime,
                           analyzed_datetime,
                           eval_score,
                           opinion)
            value (new_id,
                   _board,
                   NOW(),
                   null,
                   null,
                   null,
                   null
            );

        insert into requests(user_id,
                             board_id,
                             request_datetime,
                             requested_time,
                             requested_node,
                             requested_depth)
            value (
                   _user_id,
                   new_id,
                   NOW(),
                   _requested_time,
                   _requested_node,
                   _requested_depth
            );

    elseif search_id = 1 then
        -- すでに解析済みレコードが存在すれば解析済み
        insert into requests(user_id,
                             board_id,
                             request_datetime,
                             requested_time,
                             requested_node,
                             requested_depth)
            value (
                   _user_id,
                   search_id,
                   NOW(),
                   _requested_time,
                   _requested_node,
                   _requested_depth
            );

    end if;

end;
//
delimiter ;

delimiter //


create function task_mapper(
    IN _analyzer_id int
)
    returns varchar(200)

begin
    declare b_id int;
    declare _bd varchar(200);

    select b_id := board_id,
           _bd := board
    from Boards
    where analyzer_id is null
    order by request_datetime desc
    limit 1;
    select b_id;

    if b_id is not null then
        update Boards
        set analyzer_id = _analyzer_id
        where board_id = b_id;
    end if;
    return _bd;


end;
//
delimiter ;


create user 'analyzer'@'engine' identified by 'analyze';
create user 'api'@'service_api' identified by 'api';

grant execute on procedure kishin_service.insert_request to 'api'@'service_api';
grant select , update on kishin_service.Boards to 'analyzer'@'engine';