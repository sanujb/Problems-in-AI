(define (domain hanoi-domain)
	(:requirements :equality)
	(:predicates (disk ?x) (smaller ?x ?y) (on ?x ?y) (top ?x))
	(:action move-disk
		:parameters (?disk ?from ?to)
		:precondition
			(and 
				(disk ?disk)
				(smaller ?disk ?to)
				(on ?disk ?from)
				(top ?disk)
				(top ?to)
			)
		:effect 
			(and 
				(top ?from)
				(on ?disk ?to)
				(not (on ?disk ?from))
				(not (top ?to))
			)
	)
)