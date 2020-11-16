import shelve,pickle
player_database = shelve.open("test_database") 
player1_net = player_database["test"]
f = open("Trained_AI.obj", 'wb') 
pickle.dump(player1_net, f)
f.close()