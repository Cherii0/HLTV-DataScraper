
CREATE TABLE [matches] (
  [id] integer PRIMARY KEY,
  [date] date,
  [type] varchar(max),
  [tournament_id] integer,
  [teamA_id] integer,
  [teamB_id] integer,
  [score_won] integer,
  [score_lost] integer,
  [teamA_bans] varchar(max),
  [teamB_bans] varchar(max),
  [mvp] int,

  CONSTRAINT FK_tournament FOREIGN KEY (tournament_id) REFERENCES [tournaments](id),
  CONSTRAINT FK_teamA_details FOREIGN KEY (teamA_id) REFERENCES [teams](id),
  CONSTRAINT FK_teamB_details FOREIGN KEY (teamB_id) REFERENCES [teams](id),
  CONSTRAINT FK_mvp_details FOREIGN KEY (mvp) REFERENCES [player_details](id)

)


CREATE TABLE [maps_stats] (
  [id] integer PRIMARY KEY,
  [match_id] integer,
  [map] varchar(max),
  [seq_row] int,
  [picked_by] varchar(max),
  [teamA_firsthalf_score] int,
  [teamB_firsthalf_score] int,
  [teamA_secondhalf_score] int,
  [teamB_secondhalf_score] int,
  [teamA_end_score] int,
  [teamB_end_score] int,
  
  CONSTRAINT FK_match FOREIGN KEY (match_id) REFERENCES [matches](id)
  
)


CREATE TABLE [player_stats] (
  [id] integer PRIMARY KEY,
  [map_id] int,
  [player_id] varchar(max),
  [kills] int,
  [deaths] int,
  [adr] int

  CONSTRAINT FK_map FOREIGN KEY (map_id) REFERENCES [maps_stats](id)

)


CREATE TABLE [teams] (
  [id] integer PRIMARY KEY,
  [name] varchar(max),
  [country] varchar(max),
  [ranking] int,
  [best_map] varchar(max),
  [worst_map] varchar(max),
  [player1_id] int,
  [player2_id] int,
  [player3_id] int,
  [player4_id] int,
  [player5_id] int,

  CONSTRAINT player1_id FOREIGN KEY (player1_id) REFERENCES [player_details](id),
  CONSTRAINT player2_id FOREIGN KEY (player2_id) REFERENCES [player_details](id),
  CONSTRAINT player3_id FOREIGN KEY (player3_id) REFERENCES [player_details](id),
  CONSTRAINT player4_id FOREIGN KEY (player4_id) REFERENCES [player_details](id),
  CONSTRAINT player5_id FOREIGN KEY (player5_id) REFERENCES [player_details](id)

)


CREATE TABLE [player_details] (
  [id] integer PRIMARY KEY,
  [name] varchar(max),
  [country] varchar(max),
  [full_name] varchar(max),
  [age] int
)


CREATE TABLE [tournaments] (
  [id] integer PRIMARY KEY,
  [name] varchar(max),
  [type] varchar(max),
  [date] date,
  [tier] int,
  [place] varchar(max),
  [team_won_id] int,
  [teams_attended] int,
  [price_pool] int
)

