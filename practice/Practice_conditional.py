try:
    raw_input = input("Enter your AI Confidence Score (0-100):")

    Score = int(raw_input)

    if Score >= 80:
        print("High-Confidence")
    elif Score >= 50 and 79:
        print("Medium-Review")
    else:
        print("Low-Reject")

except ValueError:
    print("Enter a valid Number")
