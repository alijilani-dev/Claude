Running the Calculator

  Start the calculator:
  uv run python -m calculator

  You should see:
  Welcome to Calculator! Enter expressions like '5 + 3' or type 'quit' to exit.
  >

  Performing Operations

  The calculator accepts input in the format: <number> <operator> <number>

  Important: Always use spaces between the numbers and operator!

  Basic Operations

  Addition:
  > 5 + 3
  8

  > 100 + 50
  150

  Subtraction:
  > 10 - 4
  6

  > 50 - 75
  -25

  Multiplication:
  > 6 * 7
  42

  > 12 * 5
  60

  Division:
  > 20 / 4
  5

  > 10 / 3
  3.3333333333

  Decimal Numbers

  > 5.5 + 2.3
  7.8

  > 10.0 / 3.0
  3.3333333333

  > 7.5 * 2.0
  15

  Negative Numbers

  > -5 + 3
  -2

  > -6 * -7
  42

  > -20 / 4
  -5

  > 10 - 15
  -5

  Error Handling

  Division by zero:
  > 5 / 0
  Error: Division by zero is not allowed

  Invalid numbers:
  > abc + 5
  Error: Invalid input - please enter valid numbers

  Invalid operators:
  > 10 $ 5
  Error: Invalid operator - use +, -, *, or /

  Incomplete input:
  > 5 +
  Error: Please provide two numbers and an operator

  Exiting the Calculator

  Type either quit or exit (case-insensitive):

  > quit
  Goodbye!

  or

  > EXIT
  Goodbye!

  Complete Example Session

  $ uv run python -m calculator
  Welcome to Calculator! Enter expressions like '5 + 3' or type 'quit' to exit.
  > 5 + 3
  8
  > 10 - 4
  6
  > 6 * 7
  42
  > 20 / 4
  5
  > 5.5 + 2.3
  7.8
  > -6 * -7
  42
  > 10 / 0
  Error: Division by zero is not allowed
  > 100 + 50
  150
  > quit
  Goodbye!

  Important Rules

  ✅ DO:
  - Use spaces: 5 + 3 ✓
  - Use any of these operators: +, -, *, /
  - Use decimals: 5.5 + 2.3 ✓
  - Use negatives: -5 + 3 ✓

  ❌ DON'T:
  - Skip spaces: 5+3 ✗
  - Use words: 5 plus 3 ✗
  - Chain operations: 2 + 3 + 4 ✗
  - Use parentheses: (5 + 3) * 2 ✗

  Tips

  1. The calculator keeps running - After an error, you can just enter a new calculation     
  2. One operation at a time - Calculate 3 * 4 first, then add 2 separately
  3. Decimal precision - Results show up to 10 decimal places with trailing zeros removed    
  4. Case-insensitive exit - quit, QUIT, exit, EXIT all work

  Try it out now! Run uv run python -m calculator and start calculating! 🧮