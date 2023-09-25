low = 0
high = 100
guess = (low + high)/2.0
loop_check = True

print("Please think of a number between " + str(low) + " and " + str(high) +".")

while loop_check:
    print("Is your secret number " + str(int(guess)) + "?")
    while True:
        inp = input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")
        if inp == "l" or inp == "c" or inp == "h":
                break
        else:
            print("Sorry, I did not understand your input.")
    if inp == "c":
        print("Game over. Your secret number was: " +str(guess))
        loop_check = False
        break
    elif inp == "h":
        high = guess
    elif inp == "l":
        low = guess
    guess = int((high + low)/2.0)

        
