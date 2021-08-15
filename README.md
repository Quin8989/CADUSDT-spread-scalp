# CADUSDT-spread-scalp
Scalps across a relatively stable trading pair, flipping back and fourth from buy/ sell sides. The Idea being able to profit from the spread whenever somebody makes market orders.

Strategy:

1. Place a limit buy order just above the current most attractive buy order.
2. Constantly refresh limit order so it stays most attractive- as long as spread is still sufficciently large enough.
3. Limit Buy fills from somebody's market sell, flip to sell side and constantly refresh.
4. Limit sell order fills, repeat step 1.


