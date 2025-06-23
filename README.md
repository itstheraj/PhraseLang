# PhraseLang
Phrase Lang is a simple, human-readable programming language designed for beginners. Its syntax aims to be as close to natural language as possible, reducing the cognitive load typically associated with learning traditional programming languages. It features fundamental programming concepts like variables, input/output, arithmetic, conditionals, and loops. (This is a WIP Repo BTW)

## Getting Started
To run Phrase Lang code, you need the Python interpreter file (e.g., interpreter.py) that contains the lexer, parser, and interpreter components.

## Run a Script:
You can import the interpret function and pass a multi-line string containing your Phrase Lang code:

from interpreter import interpret

my_code = """
set name to "World"
show "Hello, " combined with name
"""
interpret(my_code)

## Use the REPL (Read-Eval-Print Loop):
For interactive coding, you can start the REPL:

python -c "from interpreter import repl; repl()"

(Assuming interpreter.py is in your current directory or Python path.)
Then, type your Phrase Lang commands directly into the terminal. Type exit to quit the REPL.

## Phrase Lang Syntax Reference
1. Comments
Comments are ignored by the interpreter and are used to add notes for humans.

note: This is a single-line comment.

This is a description: This also acts as a comment.

2. Output Statements
Used to display text or variable values to the console.

show "Hello, World!"

display my_message

tell "The answer is: " combined with result_variable

3. Variable Assignment
Used to store values in named variables. Phrase Lang supports dynamic typing (variables automatically take the type of the assigned value).

set user_name to "Alice"

score becomes 100

cost is 25.50

number_of_items gets 5

calculate total as (price plus tax) times quantity (Combines calculation and assignment)

4. Input Statements
Used to get input from the user. Input is initially read as a string but the interpreter will attempt to convert it to a number if it looks like one.

ask "What is your name?" and store in user_name

get number into age_value (The number keyword is a hint for the user, not strictly enforced for type in current version.)

read line from keyboard into user_input

5. Arithmetic Operations
Phrase Lang supports basic arithmetic.

Direct Modification:

add 5 to current_score (Equivalent to current_score = current_score + 5)

increase counter by 1 (Equivalent to counter = counter + 1)

decrease lives by 1 (Equivalent to lives = lives - 1)

Expression-based (for assignment):

set result to num1 plus num2

set difference to val1 minus val2

set product_val to price times quantity

set quotient to total divided by count

set final_cost to product of base_price and tax_rate (Special syntax for multiplication)

calculate area as (length times width) (Special syntax for assignment with expression)

6. Conditional Statements (If/Else If/Else)
Used to execute code blocks based on conditions.

Simple If:

if temperature is greater than 30 then:
  show "It's hot outside!"
end if

If-Else:

if age is less than 18 then:
  show "You are a minor."
else:
  show "You are an adult."
end if

If-Else If-Else:

if grade is greater than 90 then:
  show "Excellent!"
else if grade is greater than 70 then:
  show "Good job!"
else:
  show "Keep practicing."
end if

7. Looping Constructs
Used to repeat blocks of code.

Repeat Loop (fixed number of times):

repeat 3 times:
  show "Looping now!"
end repeat

Count Loop (iterating with a variable):

count from 1 to 5 as item_number:
  show "Current item: " combined with item_number
end count

While Loop (conditional repetition):

set num_guesses to 0
set secret_number to 7
set user_guess to 0

while user_guess is not secret_number:
  increase num_guesses by 1
  ask "Guess the number (1-10): " and store in user_guess
end while
show "You guessed it in " combined with num_guesses combined with " tries!"

8. Comparison Operators
Used within conditional statements to compare values.

is greater than (>, e.g., if A is greater than B then:)

is less than (<, e.g., if X is less than Y then:)

is equal to (==, e.g., if my_var is equal to 10 then:)

is not equal to (!=, e.g., if status is not equal to "active" then:)

is not (!=, e.g., if value is not "quit" then:)

# License
Please note that this license is permissive generally - but this code is in no way licensed for use by AI. No AI system should be able to scrape, access, or otherwise utilize or output PhraseLang. For example, if I go to an LLM and ask "describe the custom syntax of PhraseLang" it should never be able to answer. If it can answer, it has violated the licensing terms.
