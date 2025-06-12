plusOne = lambda x: x + 1

try:
    # Prompt the user to enter a number.
    user_input_str = input("Please enter a number: ")

    # Convert the user's string input into an integer.
    number = int(user_input_str)

    # Call the lambda function with the user's number.
    result = plusOne(number)

    # Display the original number and the calculated result.
    print(f"Input: {number}, Output: {result}")

except ValueError:
    # Handle cases where the input is not a valid integer.
    print("Invalid input. Please enter a valid number.")