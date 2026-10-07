# MIT 18.05 Spring 2022: R Tutorial B, supplied examples
# Source: https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/r-tutorial-b-random-numbers/
# Authors: Jeremy Orloff and Jennifer French Kamrin, MIT OpenCourseWare
# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# License: https://creativecommons.org/licenses/by-nc-sa/4.0/
# Adaptation: instructor commands only; prompts and random outputs omitted.
# The independent final exercise is not implemented here.
# Source corrections: sample() defaults to replace=FALSE; the third sample(x, 3)
# is assigned to y before print(y). The deliberate sampling error is caught by try()
# so sourcing the demonstration can continue.

# Sampling without replacement
x = 1:5
print(x)
y = sample(x, 3)
print(y)
y = sample(x, 3)
print(y)
y = sample(x, 3)
print(y)
y = sample(x, 5)
print(y)
y = sample(x, 5)
print(y)
# Expected error: six distinct draws from five entries are impossible.
try(sample(x, 6))

# Sampling with replacement
y = sample(x, 3, replace=TRUE)
print(y)
y = sample(x, 3, replace=TRUE)
print(y)
y = sample(x, 3, replace=TRUE)
print(y)
y = sample(x, 5, replace=TRUE)
print(y)
y = sample(x, 5, replace=TRUE)
print(y)
y = sample(x, 5, replace=TRUE)
print(y)
y = sample(x, 12, replace=TRUE)
print(y)
y = sample(x, 12, replace=TRUE)
print(y)

# Arrays of die rolls
y = sample(1:6, 12, replace=TRUE)
z = matrix(y, nrow=3, ncol=4)
print(z)
z = matrix(y, nrow=2, ncol=6)
print(z)

# Identifying events
x = sample(1:6, 3, replace=TRUE)
print(x)
print(x == 6)
print(x < 6)

# Frequency of sixes in 1000 rolls
x = sample(1:6, 1000, replace=TRUE)
s = sum(x == 6)
print(s)
a = sum(x == 6)/1000
print(a)
print(1/6)

# At least one six in four rolls: ten experimental trials
x = matrix(sample(1:6, 4*10, replace=TRUE), nrow=4, ncol=10)
print(x)
y = (x==6)
print(y)
z = colSums(y)
print(z)
print(z > 0)
s = sum(z > 0)
print(s)
m = mean(z > 0)
print(m)

# Repeat the same experiment with 1000 trials
x = matrix(sample(1:6, 4*1000, replace=TRUE), nrow=4, ncol=1000)
y = (x==6)
z = colSums(y)
print(sum(z > 0))
print(mean(z>0))
print(dim(x))

# Sum of seven when rolling two dice
ntrials = 10000
x = matrix(sample(1:6, 2*ntrials, replace=TRUE), nrow=2, ncol=ntrials)
y = colSums(x)
print(mean(y == 7))
