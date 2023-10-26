import random
import sys
import os

# 'convo' is the variable in which the chat's history is stored.
convo = "Duck: Hi! I am the duck you will be now talking to. Tell me anything you like now!\n"
print(convo, end="")

# Defining some logic on how the duck should respond when different elements are present in the user's input.
def generate_response(user_input:str) -> str:
    # Lists of responses to return in different situations.
    gen_responses = ["Alright.", "That's fine.", "OK.", "Continue..", "I see...", "Cool!"]
    question_responses = ["Sure!", "Why not..", "Yes.", "No.", "I agree.", "I disagree.", "I think so."]
    exclamation_responses = ["That's amazing!", "Wow!", "How wonderful!", "Interesting!", "Nice!"]
    if "" == user_input:
        return "[awkward silence]"
    # Checking if the user wants to save or exit the conversation, and only doing so if their input is relatively small, to avoid (most) unintended actions.
    if not ("bye" in user_input.lower() and len(user_input) <= 25) and not ("save" in user_input.lower() and len(user_input) <= 25):
        # ...otherwise, check for special elements in the input, and if any, return a more optimized/specific response.
        if "?" in user_input:
            return "Duck: " + random.choice(question_responses)
        if "!" in user_input:
            return "Duck: " + random.choice(exclamation_responses)
        else:
            return "Duck: " + random.choice(gen_responses)
    # In case we get here, the user does not await a response, but is giving a command. Check it and do the appropriate actions.
    elif "bye" in user_input.lower():
        print("Duck: Bye!")
        sys.exit(0)
    # If they did not ask to end the conversation, they can only want to save it.
    else:
        with open(os.path.join(os.getcwd(), "RubberDuck", "result.txt"), "a") as f:
            f.write(convo + "--------------------------------------------------------------------------------------------\n")
        return "Duck: Saved the current conversation!"

# Eternally responding to the user's input, until they want to stop, by including "bye" in a short phrase/period.
while True:
    user_input = input("You: ")
    response = generate_response(user_input)
    print(response)
    convo += "You: " + user_input + "\n" + response + "\n"
