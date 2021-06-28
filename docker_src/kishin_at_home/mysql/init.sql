drop
    database if exists kishin_service;

create
    database kishin_service;


use kishin_service;

create TABLE Boards
(
    board_id          int primary key auto_increment,
    board             varchar(200),
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
    set search_id =
            (
                select board_id
                from Boards
                where _board = Boards.board
            );

    if count(search_id) = 0 then
        -- 存在しなければ未解析レコードとして両テーブルに新規追加
        insert into Boards(board, analyzed_datetime, eval_score, opinion)
            value (_board, null, null, null);

        insert into requests(user_id,
                             board_id,
                             request_datetime,
                             requested_time,
                             requested_node,
                             requested_depth)
            value (
                   _user_id,
                   LAST_INSERT_ID(),
                   NOW(),
                   _requested_time,
                   _requested_node,
                   _requested_depth
            );

    elseif count(search_id) = 1 then
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

