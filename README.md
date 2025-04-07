# csp-test


Usage: 

1) `main.py <ticker>` and select option expiration date 
2) or `main.py <ticker> -e <option expiration date>`

ex 1) `main.py AAPL`

```
Available expiration dates:
1. 2025-04-11
2. 2025-04-17
3. 2025-04-25
4. 2025-05-02
5. 2025-05-09
6. 2025-05-16
7. 2025-05-23
8. 2025-06-20
9. 2025-07-18
10. 2025-08-15
11. 2025-09-19
12. 2025-10-17
13. 2025-12-19
14. 2026-01-16
15. 2026-03-20
16. 2026-06-18
17. 2026-12-18
18. 2027-01-15
19. 2027-06-17
20. 2027-12-17

Select a date (enter the number):
```

ex 2) `main.py AAPL -e 2025-04-11` 


---

TODO: yfinance does not have option greek values. Find alternative source or calculate greeks.