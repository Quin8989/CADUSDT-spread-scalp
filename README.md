# CADUSDT-spread-scalp
Scalps trades across a relatively stable trading pair on a specific exchange, flipping back and fourth from buy/ sell sides. The Idea being able to profit from the spread whenever somebody makes market orders.

General strategy:

1. Place a limit buy order just above the current most attractive buy order.
2. Constantly refresh limit order so it stays most attractive- as long as spread is still sufficciently large enough.
3. Limit Buy fills from somebody's market sell, flip to sell side and constantly refresh.
4. Limit sell order fills, repeat step 1.

UPDATE: 
With an initial investment of $50 and running my program in the background, I have been earning the equivalent of a part- time wage before the native exchange shut down all automated trading for my account. This was a fun learning experience in applying a simple trading strategy using some code.


