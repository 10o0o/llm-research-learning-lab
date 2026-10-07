# MIT 18.05 Spring 2022: R Tutorial A, supplied examples
# Source: https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/r-tutorial-a-basics/
# Authors: Jeremy Orloff and Jennifer French Kamrin, MIT OpenCourseWare
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/
# Adaptation: tutorial commands; prompts and outputs omitted;
# explicit printing added for vector arithmetic in scripts; source correction noted below.
# 공식 예시를 한 줄씩 실행하세요. 자신의 변형은 my-variants.R에 작성하세요.

# R as a Calculator
2+3
2*3
2/3
2^3
2*(3+1)^2

# Using Variables
x = 2+3
print(x)
y = 1+2
print(x*y)
z = x^y
print(z)
x <- 3
print(x)
x <- 5.412
print(x)

# Vectors
x = c(1.1, 0.0, 3.14, 2.718)
print(x)
x <- c(2,4,6)
print(x)
x = 1:4
print(x)
x = 3:10
print(x)
x = 9:2
print(x)
x = 1:40
print(x)

# Vector Arithmetic
# Source correction: the first example uses x + 7.1 and then print(y),
# without assigning that result to y. Print the expression's result directly.
x = c(1,3,5)
print(x + 7.1)

x = c(1,3,5)
print(7*x)
print(x/7)
print(7/x)
print(x^6)
print(x^7)
print(7^x)

x = c(1, 2, 3)
y = c(4, 5, 6)
print(x + y)
print(x - y)
z = x*y
print(z)
z = x/y
print(z)
print(x^y)

# Accessing entries in a vector
x = c(2, 4, 6, 8, 10)
print(x[1])
print(x[2])
print(x[3])
print(x[4])

x = 2*c(1, 2, 3, 4, 5, 6, 7, 8)
print(x)
y = x[c(1,2)]
print(y)
y = x[c(1,3,5)]
print(y)
y = x[c(2,2,2,1)]
print(y)
y = x[2:5]
print(y)

# Functions on Vectors
x = sin(1)
print(x)
x = sin(1.4)
print(x)
x = sin(3)
print(x)
print(pi)
print(sin(pi/2))
x = exp(0)
print(x)
x = exp(1)
print(x)

x = c(1, 2, 3, 4)
print(x)
y = sin(x)
print(y)
x = c(1, 2, 3, 4)
y = exp(x)
print(y)

x = 1:6
print(x)
s = sum(x)
print(s)
m = mean(x)
print(m)
x = 1:1024
s = sum(x)
print(s)
s = sum(1:1024)
print(s)

# A few more examples with powers
x = 1:1024
s = sum(x^2)
print(s)
s = sum((1:1024)^2)
print(s)

# Matrices
x = 1:10
print(x)
y = matrix(x,nrow=2,ncol=5)
print(y)
z = matrix(x,nrow=5,ncol=2)
print(z)
z = matrix(x,nrow=2,ncol=5, byrow = TRUE)
print(z)

# Accessing Entries in Matrices
x = 1:10
y = matrix(x, nrow=2, ncol=5)
print(y)
print(y[1,1])
print(y[2,3])

# Sums and Means on Matrices
x = 1:10
y = matrix(x, nrow=2, ncol=5)
print(y)
print(y)
s = colSums(y)
print(s)
s = rowSums(y)
print(s)
m = rowMeans(y)
print(m)
m = colMeans(y)
print(m)

# Getting Help
?mean
