x1 = int(input("Enter value of x1: "))
x2 = int(input("Enter value of x2: "))
y1 = int(input("Enter value of y1: "))
y2 = int(input("Enter value of y2: "))

dy = y2 - y1
dx = x2 - x1

z = dy / dx
i = dy * dx 
print("The difference in your curtesian plain is:", z. i)

def f(x):
    return x ** 2

x1 = float(input("Enter value of x1: "))
delta_x = float(input("Enter initial value for delta x (for approximation): "))

derative_approx = (f(x1 + delta_x) - f(x1)) / delta_x

print(f"Approximated derivative at x = {x1} using delta x = {delta_x}: {derative_approx}")

new_delta_x = delta_x / 10
improved_derivative_approx = (f(x1 + new_delta_x) - f(x1)) / new_delta_x
print(f"Improved approximation for derivative at x = {x1} using smaller delta x = {new_delta_x}: {improved_derivative_approx}")
