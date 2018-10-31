(define (problem peg-solitaire-problem)
	(:domain peg-solitaire-domain)
	(:objects 				loc0
						loc1 	loc2
					loc3 	loc4 	loc5
				loc6 	loc7 	loc8 	loc9
			loc10 	loc11	loc12 	loc13 	loc14
	)

	(:init
		(empty loc0)
		(full loc1)(full loc2)
		(full loc3)(full loc4)(full loc5)
		(full loc6)(full loc7)(full loc8)(full loc9)
		(full loc10)(full loc11)(full loc12)(full loc13)(full loc14)

		(transition loc0 loc1 loc3)
		(transition loc0 loc2 loc5)

		(transition loc1 loc3 loc6)
		(transition loc1 loc4 loc8)

		(transition loc2 loc4 loc7)
		(transition loc2 loc5 loc9)

		(transition loc3 loc4 loc5)
		(transition loc3 loc6 loc10)
		(transition loc3 loc7 loc12)

		(transition loc4 loc7 loc11)
		(transition loc4 loc8 loc13)

		(transition loc5 loc8 loc12)
		(transition loc5 loc9 loc14)

		(transition loc6 loc7 loc8)
		(transition loc7 loc8 loc9)

		(transition loc10 loc11 loc12)
		(transition loc11 loc12 loc13)
		(transition loc12 loc13 loc14)
	)

	(:goal
		(and
			(full loc0)
			(empty loc1)
			(empty loc2)
			(empty loc3)
			(empty loc4)
			(empty loc5)
			(empty loc6)
			(empty loc7)
			(empty loc8)
			(empty loc9)
			(empty loc10)
			(empty loc11)
			(empty loc12)
			(empty loc13)
			(empty loc14)
		)
	)
)