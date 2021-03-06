drop
    database if exists kishin_service;

create
    database kishin_service;

SET GLOBAL log_bin_trust_function_creators = 1;

use kishin_service;
create table engines
(
    engine_id int primary key,
    nickname  varchar(50)
);

create TABLE Boards
(
    board_id          int primary key,
    board             varchar(200),
    engine_id         int,
    request_datetime  datetime,
    analyzed_datetime datetime,
    eval_score        varchar(20),
    opinion           varchar(200),
    depth        varchar(20),
    nps        varchar(20),
    nodes        varchar(20),
    foreign key engine_key (engine_id) references engines (engine_id)
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



insert into engines(engine_id, nickname) VALUE (1, 'Ayane');

create function get_eval(sfen varchar(200)) returns VARCHAR(200)
return (
    select eval_score
    from Boards
    where board = sfen
    )
;

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

        insert into Boards(board_id,
                           board,
                           engine_id,
                           request_datetime,
                           analyzed_datetime,
                           eval_score,
                           opinion)
            value (
                   new_id,
                   _board,
                   1,
                   NOW(),
                   null,
                   'unanalyzed',
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


