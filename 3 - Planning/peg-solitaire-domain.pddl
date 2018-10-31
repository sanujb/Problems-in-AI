(define (domain peg-solitaire-domain)
	(:predicates
		(transition ?loc1 ?loc2 ?loc3)
		(full ?loc)
		(empty ?loc)
	)

	(:action MOVE-FORWARDS
		:parameters (?loc1 ?loc2 ?loc3)
		:precondition
			(and 
				(transition ?loc1 ?loc2 ?loc3)
				(full ?loc1)
				(full ?loc2)
				(empty ?loc3)
			)
		:effect
			(and
				(empty ?loc1)(not (full ?loc1))
				(empty ?loc2)(not (full ?loc2))
				(full ?loc3)(not (empty ?loc3))
			)
	)

	(:action MOVE-BACKWARDS
		:parameters (?loc1 ?loc2 ?loc3)
		:precondition
			(and
				(transition ?loc1 ?loc2 ?loc3)
				(empty ?loc1)
				(full ?loc2)
				(full ?loc3)
			)
		:effect
			(and
				(full ?loc1) (not (empty ?loc1))
				(empty ?loc2) (not (full ?loc2))
				(empty ?loc3) (not (full ?loc3))
			)
	)
)