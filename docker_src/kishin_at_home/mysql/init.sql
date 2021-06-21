drop
database if exists kishin_service;

create
database kishin_service;


USE
kishin_service;

create TABLE Boards
(
    board_id          int primary key,
    analyzed_type     char(10),
    board             varchar(200),
    analyzed_datetime datetime,
    eval_score        varchar(20),
    opinion           varchar(200)
);

create TABLE requests
(
    request_id       int primary key,
    user_id          int,
    board_id         int,
    request_datetime datetime,
    requested_time   int,
    requested_node   int,
    requested_depth  int,
    foreign key key_board_id(board_id) references Boards(board_id)
);
delimiter
//
create procedure insert_request(
    _user_id int,
    _board int,
    _requested_time int,
    _requested_node int,
    _requested_depth int
    );
begin

end
//