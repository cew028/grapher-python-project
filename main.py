class ZeroCoefficientError(Exception):
    """Raised if you try to assign 0 to the dth coefficient of a degree d polynomial."""
    pass
    
class DegreeSignError(Exception):
    """Raised when the degree is negative."""
    pass

class EndpointOrderError(Exception):
    """Raised when the left endpoint is to the right of the right endpoint."""
    pass

def ask_for_coefficients():
    """This function prompts the user to enter the degree and coefficients of a polynomial."""
    while True:
        try:
            degree = int(input("What is the degree of your polynomial? "))
            if degree < 0: 
                # The degree of a polynomial cannot be negative.
                raise DegreeSignError
        except (ValueError, DegreeSignError):
            print("The degree should be a positive integer.")
            continue
        else:
            break
    # We keep track of a polynomial by putting its coefficients in a list, ordered by increasing power.
    coefficient_array = []
    for i in range(degree+1):
        while True:
            try:
                coefficient_i = float(input(f"What is the {ordinal(i)} coefficient? "))
                if i != 0 and i == degree and coefficient_i == 0:
                    # By definition, a degree d polynomial cannot have a coefficient of 0 on the x^d term.
                    raise ZeroCoefficientError
            except ValueError:
                print("That is not a valid coefficient.")
                continue
            except ZeroCoefficientError:
                print("The dth coefficient of a degree d polynomial cannot be 0.")
                continue
            else:
                break
        # Add the valid coefficient to the list:
        coefficient_array.append(coefficient_i)
    return coefficient_array

def create_a_polynomial(array):
    """This function creates an algebraic polynomial out of a list of coefficients."""
    def f(x):
        return sum(coefficient*x**power for power, coefficient in enumerate(array))
    return f

def grapher(
    f,
    x_number_of_steps = 200,
    y_number_of_steps = 50,
    background = "."
    ):
    """This function takes a polynomial and graphs it in the command prompt."""
    while True:
        try:
            x_min = float(input("What is your leftmost endpoint? "))
        except ValueError:
            print("Please enter a number.")
            continue
        else:
            break
    while True:
        try:
            x_max = float(input("What is your rightmost endpoint? "))
            if x_max <= x_min:
                # The left endpoint cannot be right of the right endpoint.
                raise EndpointOrderError
        except ValueError:
            print("Please enter a number.")
            continue
        except EndpointOrderError:
            print("Your right endpoint must occur after your left endpoint.")
            continue
        else:
            break
    # Next, we want to choose an appropriate y-scale to view the function.
    # Start by initializing the highest and lowest the y-values ever go at 0.
    y_min = 0
    y_max = 0
    x_step_size = (x_max - x_min)/x_number_of_steps
    for x in range(x_number_of_steps): # We evaluate our polynomial over our entire domain.
        x_coord = x_min+x*x_step_size
        if f(x_coord) > y_max:
            # If the function value is larger than the largest one so far, set y_max to be that value.
            y_max = f(x_coord)
        elif f(x_coord) < y_min:
            # If the function value is smaller than the smallest one so far, set y_min to be that value.
            y_min = f(x_coord)
    y_step_size = (y_max - y_min)/y_number_of_steps
    for y in range(y_number_of_steps):
        y_coord = y_max-y*y_step_size # The graph is drawn from top down, hence the need to subtract y*y_step_size.
        line = ""
        for x in range(x_number_of_steps):
            x_coord = x_min+x*x_step_size
            if round(f(x_coord)) == round(y_coord):
                line += "*"
            elif round(x_coord) == 0 and round(y_coord) == 0:
                line += "+"
            elif round(x_coord) == 0 and round(y_coord) != 0:
                line += "|"
            elif round(x_coord) != 0 and round(y_coord) == 0:
                line += "—"
            else:
                line += background
        print(line)
    
def ordinal(integer):
    match integer:
        case 1:
            return f"{integer}st"
        case 2:
            return f"{integer}nd"
        case 3:
            return f"{integer}rd"
        case _:
            return f"{integer}th"

def convert_to_plaintext(array):
    """Takes an inputted coefficient list and expresses it as an algebraic expression."""
    plaintext_polynomial = ""
    power = 0
    if len(array) == 1 and array[0] == 0:
        # Edge case: your polynomial is f(x) = 0.
        plaintext_polynomial = "0"
    else:
        for coefficient in array:
            if coefficient == 0:
                # Don't write a term if the coefficient is 0.
                plaintext_polynomial += ""
            else:
                if coefficient % 1 == 0:
                    # If the coefficient is an integer, convert the float to an int.
                    j = int(coefficient)
                else:
                    # If it's not, leave it alone.
                    j = coefficient
                if power == 0:
                    # Don't write Cx^0, just write C.
                    plaintext_polynomial += f"{j}"
                elif power == 1:
                    # Don't write Cx^1, just write Cx.
                    if j == 1:
                        # Don't write the coefficient if it is 1.
                        plaintext_polynomial += "x"
                    else:
                        plaintext_polynomial += f"{j}x"
                else:
                    if j == 1:
                        # Don't write the coefficient if it is 1.
                        plaintext_polynomial += f"x^{power}"
                    else:
                        plaintext_polynomial += f"{j}x^{power}"
            if power != len(array)-1 and coefficient != 0:
                # Add a plus sign, as long as you're not at the end of the polynomial or you just came from a 0 term.
                plaintext_polynomial += " + "
            power += 1
    return print(f"Your polynomial is f(x) = {plaintext_polynomial}.")

# for i in range(10000):
    # os.system("cls") # Windows
    # print(i)

if __name__ == "__main__":
    print("For best results, full screen your command prompt.")
    coefficients = ask_for_coefficients()
    polynomial = create_a_polynomial(coefficients)
    convert_to_plaintext(coefficients)
    grapher(polynomial,)