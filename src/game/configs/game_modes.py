def only_bots(app):
    map = app.map

    p1_pos = (1, 1)
    p1 = app.player_manager.create_bot(map, p1_pos, 1, "Bluey")
    p1.face_to_dir(1,0)

    p2_pos = (map.width-2, map.height-2)
    p2 = app.player_manager.create_bot(map, p2_pos, 2, "Redy")
    p2.face_to_dir(-1,0)

    p3_pos = (1, map.height-2)
    p3 = app.player_manager.create_bot(map, p3_pos, 3, "Yellowy")
    p3.face_to_dir(1,0)

    p4_pos = (map.width-2, 1)
    p4 = app.player_manager.create_bot(map, p4_pos, 4, "Cyany")
    p4.face_to_dir(-1,0)

def single_player(app):
    map = app.map

    p1_pos = (1, 1)
    p1 = app.player_manager.create_player(map, p1_pos, 1, "Bluey")
    p1.face_to_dir(1,0)

    p2_pos = (map.width-2, map.height-2)
    p2 = app.player_manager.create_bot(map, p2_pos, 2, "Redy")
    p2.face_to_dir(-1,0)

    p3_pos = (1, map.height-2)
    p3 = app.player_manager.create_bot(map, p3_pos, 3, "Yellowy")
    p3.face_to_dir(1,0)

    p4_pos = (map.width-2, 1)
    p4 = app.player_manager.create_bot(map, p4_pos, 4, "Cyany")
    p4.face_to_dir(-1,0)

def local(app):
    map = app.map

    p1_pos = (1, 1)
    p1 = app.player_manager.create_player(map, p1_pos, 1, "Bluey")
    p1.face_to_dir(1,0)

    p2_pos = (map.width-2, map.height-2)
    p2 = app.player_manager.create_player(map, p2_pos, 2, "Redy")
    p2.face_to_dir(-1,0)

    p3_pos = (1, map.height-2)
    p3 = app.player_manager.create_bot(map, p3_pos, 3, "Yellowy")
    p3.face_to_dir(1,0)

    p4_pos = (map.width-2, 1)
    p4 = app.player_manager.create_bot(map, p4_pos, 4, "Cyany")
    p4.face_to_dir(-1,0)