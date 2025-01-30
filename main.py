# name=input("Enter your name: ")
# print("hello",name)
# today="Monday"

llista_missatges_si = ["Correctooo", "Yes", "Good"]
llista_missatges_no = ["No!", "Wrong answer", "You're wrong"]

def print_random_answer(llista_missatges):
    import numpy
    random_number = numpy.random.randint(low=0,high=3)
    result=llista_missatges[random_number]
    return result

def question(today):
    print("Which day is today?")
    day=input()
    print("You said that today is",day)
  
    if day==today:
        correct_message=print_random_answer(llista_missatges_si)
        print(correct_message)
   
    else:
        incorrect_message=print_random_answer(llista_missatges_no)
        print(incorrect_message)
        print("Today is",today)
    return day

today=question("Monday")