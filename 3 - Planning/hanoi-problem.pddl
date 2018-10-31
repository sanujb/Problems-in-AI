(define (problem hanoi-problem)
	(:domain hanoi-domain)
	(:objects p1 p2 p3 d1 d2 d3 )
	(:init 
		(disk d1)(disk d2)(disk d3)

		(smaller d1 p1)(smaller d1 p2)(smaller d1 p3)
		(smaller d2 p1)(smaller d2 p2)(smaller d2 p3)
		(smaller d3 p1)(smaller d3 p2)(smaller d3 p3)

		(smaller d1 d2)(smaller d2 d3)(smaller d1 d3)

		(on d1 d2)(on d2 d3)(on d3 p1)
		(top p3)(top p2)(top d1)
	)
	(:goal 
		(and (on d1 d2)(on d2 d3)(on d3 p3) )
	)
)