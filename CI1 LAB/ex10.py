SP: Area of Circle

(defun AreaOfCircle()
        (terpri)
        (princ "Enter Radius: ")
        (setq radius (read))
        (setq area (* 3.1416 radius radius))
        (format t "Radius: = ~F~% Area = ~F" radius area)
)


CL-USER 1 > (AreaOfCircle)

Enter Radius: 5
Radius: = 5.0
 Area = 78.53999
NIL

LISP: Factorial

(defun fact2(n)
        (if(= n 0) 1
                (* n (fact2(- n 1)))
        )
)

CL-USER 1 > (fact2 6)
720


LISP: Fibonacci

(defun fib2(n)
        (cond
                ((= n 0) 0)
                ((= n 1) 1)
                ((> n 1)(+ (fib2 (- n 1)) ( fib2 (- n 2))))
        )
)


CL-USER 1 > (fib2 5)
5

CL-USER 2 > (fib2 7)
13


LISP: Palindrome

(defun palin(str)
  (equal str (coerce (reverse (coerce str 'list)) 'string)))

CL-USER 1 > (palin "madam")
T

CL-USER 2 > (palin "harish")
NIL