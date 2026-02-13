player_name = input("Enter your Name:")
games_played = int(input("Enter No.of Games Played:"))
total_score = int(input("Enter Total Score:"))
avg_score = total_score/games_played

print(f"Player: {player_name}")
print(f"Games Played: {games_played}")
print(f"Total Score: {total_score}")
print(f"Average Score: {avg_score:.2f}")

'''
Test Case-1:
Enter your Name:Rakesh
Enter No.of Games Played:26
Enter Total Score:542
Player: Rakesh
Games Played: 26
Total Score: 542
Average Score: 20.85

'''
