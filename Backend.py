lettered_grade_list={
    " A+ " : 4.00,
    " A " : 4.00,
    " A- " : 3.75,
    " B+ " : 3.5 ,
    " B " : 3.00,
    " B- " : 2.75,
    " C+ " : 2.5 ,
    " C " : 2.00,
    " D " : 1.75,
    " F " : 1.00,
}
courses=[]
mark=[]
lettered_mark=[]
credits=[]
GPA=[]

def acceptMark(Numcourses):
    for i in range(1, Numcourses+1):
        course_input=input(f"Name the courses {i}? ")
        mark_input=int(input("Write your mark out of 100? "))
        credit_input= float(input("Courses credit hour"))
        courses.append(course_input)
        mark.append(mark_input)
        credits.append(credit_input)
        print("--------------------- \n")
    return

def calculateAvgMark(mark):
    sum=0
    for i in mark:
        sum = sum + i
    return sum/len(mark)

def calculateAvgGPA(mark, credits):
    sum=0
    TotalCredit=0
    for i in mark:
        for j in credits:
            sum += (i * j)
            TotalCredit += j 
    return sum/TotalCredit

def MarkToScale(mark, lettered_mark) -> None:
    for i in mark:
        if i >= 95:
            lettered_mark.append(" A+ ")
        elif i>= 85:
            lettered_mark.append(" A ")
        elif i>= 80:
            lettered_mark.append(" A- ")
        elif i>= 75:
            lettered_mark.append(" B+ ")
        elif i>=65:
            lettered_mark.append(" B ")
        elif i>=60:
            lettered_mark.append(" B- ")
        elif i>=55:
            lettered_mark.append(" C+ ")
        elif i>=50:
            lettered_mark.append(" C ")
        elif i>=45:
            lettered_mark.append(" D ")
        else: lettered_mark.append(" F ")

def ScaleToGpa(lettered_grade_list, lettered_mark, GPA):
    for i in lettered_mark:
        GPA.append(lettered_grade_list[i])
    return GPA