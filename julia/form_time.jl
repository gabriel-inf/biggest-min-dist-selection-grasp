using GLPKMathProgInterface
using JuMP

FILE_NAME = "instances/mdmt39.112.A.ins"




# PARSING FILE

f = open(FILE_NAME);
inst = read(f, String)
close(f)

splitted_inst = split(inst)


n = map(x->parse(Float64,x),splitted_inst)
splitted_inst = map(x->trunc(Int, x), n)

M = splitted_inst[1]
L = splitted_inst[2]
l = splitted_inst[3]

println(M)
println(L)

D = zeros(Int, M, L)


# Cria a matriz de distâncias
for i = 1:M
    for j = 1:L 
        D[i,j] =  splitted_inst[3+i*j]
    end
end



model = Model(solver=GLPKSolverMIP())

@variable(model, x[1:L], Bin)
@variable(model, d[1:M], Int)

@objective(model, Max, sum(d[i] for i=1:M))



@constraints(model, begin
    sum(x[j] for j = 1:L) == l
    [i = 1:M, j = 1:L], d[i] <= x[j]*D[i,j] + ((1-x[j]) * 999) 
    [i = 1:M], d[i] >= 0
end)

println()

initial_time = now()
while(solve(model))
    println("Testeeee") 
    current_time = now()
    if Dates.minute(Dates.Dates.epochms2datetime(current-initial_time)) >= 1
        println("Partial solution: $(getobjectivevalue(model)).")
        initial_time = now()
    end
end

println("Sol otima $(getobjectivevalue(model)).")


# @variable(model, )
# @variable(model, )