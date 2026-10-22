# Graduated hints

Try the problem before opening each hint. Stop when you can continue independently.

## Hint 1

Think about maintaining a set of strictly non-overlapping intervals.

## Hint 2

When a new interval arrives, which existing intervals can it intersect with? Can you find them efficiently using binary search?

## Hint 3

Every time an existing interval overlaps, remove it from the total count, merge its boundaries into the new interval, and erase it from the data structure. Finally, insert the merged interval.

