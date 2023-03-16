CREATE TABLE IF NOT EXISTS starboard(
    RootMessageID integer PRIMARY KEY,
    StarMessageID integer,
    Stars integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS mutes (
    UserID integer PRIMARY KEY,
    RoleIDs text,
    EndTime text
);

CREATE TABLE IF NOT EXISTS tickets (
    TicketID integer,
    ReactID integer,
    ChannelNum integer,
    UserID integer
);

CREATE TABLE IF NOT EXISTS reminder (
    UserID integer,
    Remind_Message text,
    Remind_Time float
);

CREATE TABLE IF NOT EXISTS requestatc (
    UserID integer,
    bool text
);

CREATE TABLE IF NOT EXISTS onlineatc (
    CallSign text,
    TimeOnline integer,
    Bool text
);
