#!/usr/bin/env Rscript
f <- file("stdin")
open(f)
previous <- NA
increases <- 0
while(length(line <- readLines(f,n=1, warn=FALSE)) > 0) {
  value <- strtoi(line)
  if (!is.na(previous) && value > previous) {
    increases <- increases + 1
  }
  previous <- value
}
print(increases)