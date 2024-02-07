def num_gpa_calc(type, grade, weight=True):
    gpa = 0
    if grade >= 90:
        gpa = 4.0
    elif grade >= 80:
        gpa = 3.0
    elif grade >= 70:
        gpa = 2.0
    elif grade >= 60:
        gpa = 1.0
    else:
        gpa = 0.0
    
    if weight:
        if type == "Standard": add=0
        elif type == "Honors": add=0.5
        elif "AP" in type: add=1
        gpa += add
    return gpa

def total_num_gpa_calc(grades):
    sum = 0
    for g in grades:
        sum += g
    sum = sum/len(grades)
    return sum
    